#
# This file is part of pretix (Community Edition).
#
# Copyright (C) 2014-2020 Raphael Michel and contributors
# Copyright (C) 2020-2021 rami.io GmbH and contributors
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General
# Public License as published by the Free Software Foundation in version 3 of the License.
#
# ADDITIONAL TERMS APPLY: Pursuant to Section 7 of the GNU Affero General Public License, additional terms are
# applicable granting you additional permissions and placing additional restrictions on your usage of this software.
# Please refer to the pretix LICENSE file to obtain the full terms applicable to this work. If you did not receive
# this file, see <https://pretix.eu/about/en/license>.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see
# <https://www.gnu.org/licenses/>.
#
from datetime import timedelta

from celery.result import AsyncResult
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.utils.timezone import now
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.reverse import reverse

from pretix.api.pagination import TotalOrderingFilter
from pretix.api.serializers.exporters import (
    ExporterSerializer, JobRunSerializer, ScheduledEventExportSerializer,
    ScheduledOrganizerExportSerializer,
)
from pretix.base.exporter import OrganizerLevelExportMixin
from pretix.base.models import (
    CachedFile, Device, Event, ScheduledEventExport, ScheduledOrganizerExport,
    TeamAPIToken,
)
from pretix.base.services.export import export, multiexport
from pretix.base.signals import (
    register_data_exporters, register_multievent_data_exporters,
)
from pretix.helpers.http import ChunkBasedFileResponse


class ExportersMixin:
    def list(self, request, *args, **kwargs):
        res = ExporterSerializer(self.exporters, many=True)
        return Response({
            "count": len(self.exporters),
            "next": None,
            "previous": None,
            "results": res.data
        })

    def get_object(self):
        instances = [e for e in self.exporters if e.identifier == self.kwargs.get('pk')]
        if not instances:
            raise Http404()
        return instances[0]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ExporterSerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_name='download', url_path='download/(?P<asyncid>[^/]+)/(?P<cfid>[^/]+)')
    def download(self, *args, **kwargs):
        cf = get_object_or_404(CachedFile, id=kwargs['cfid'])
        if cf.file:
            resp = ChunkBasedFileResponse(cf.file.file, content_type=cf.type)
            resp['Content-Disposition'] = 'attachment; filename="{}"'.format(cf.filename).encode("ascii", "ignore")
            return resp
        elif not settings.HAS_CELERY:
            return Response(
                {'status': 'failed', 'message': 'Unknown file ID or export failed'},
                status=status.HTTP_410_GONE
            )

        res = AsyncResult(kwargs['asyncid'])
        if res.failed():
            if isinstance(res.info, dict) and res.info['exc_type'] == 'ExportError':
                msg = res.info['exc_message']
            else:
                msg = 'Internal error'
            return Response(
                {'status': 'failed', 'message': msg},
                status=status.HTTP_410_GONE
            )

        return Response(
            {
                'status': 'running' if res.state in ('PROGRESS', 'STARTED', 'SUCCESS') else 'waiting',
                'percentage': res.result.get('value', None) if res.result else None,
            },
            status=status.HTTP_409_CONFLICT
        )

    @action(detail=True, methods=['POST'])
    def run(self, *args, **kwargs):
        instance = self.get_object()
        serializer = JobRunSerializer(exporter=instance, data=self.request.data, **self.get_serializer_kwargs())
        serializer.is_valid(raise_exception=True)

        cf = CachedFile(web_download=False)
        cf.date = now()
        cf.expires = now() + timedelta(hours=24)
        cf.save()
        d = serializer.data
        for k, v in d.items():
            if isinstance(v, set):
                d[k] = list(v)
        async_result = self.do_export(cf, instance, d)

        url_kwargs = {
            'asyncid': str(async_result.id),
            'cfid': str(cf.id),
        }
        url_kwargs.update(self.kwargs)
        return Response({
            'download': reverse('api-v1:exporters-download', kwargs=url_kwargs, request=self.request)
        }, status=status.HTTP_202_ACCEPTED)


class EventExportersViewSet(ExportersMixin, viewsets.ViewSet):
    permission = 'can_view_orders'

    def get_serializer_kwargs(self):
        return {}

    @cached_property
    def exporters(self):
        exporters = []
        responses = register_data_exporters.send(self.request.event)
        raw_exporters = [response(self.request.event, self.request.organizer) for r, response in responses if response]
        raw_exporters = [
            ex for ex in raw_exporters
            if ex.available_for_user(self.request.user if self.request.user and self.request.user.is_authenticated else None)
        ]
        for ex in sorted(raw_exporters, key=lambda ex: str(ex.verbose_name)):
            ex._serializer = JobRunSerializer(exporter=ex)
            exporters.append(ex)
        return exporters

    def do_export(self, cf, instance, data):
        return export.apply_async(args=(self.request.event.id, str(cf.id), instance.identifier, data))


class OrganizerExportersViewSet(ExportersMixin, viewsets.ViewSet):
    permission = None

    @cached_property
    def exporters(self):
        exporters = []
        if isinstance(self.request.auth, (Device, TeamAPIToken)):
            perm_holder = self.request.auth
        else:
            perm_holder = self.request.user
        events = perm_holder.get_events_with_permission('can_view_orders', request=self.request).filter(
            organizer=self.request.organizer
        )
        responses = register_multievent_data_exporters.send(self.request.organizer)
        raw_exporters = [
            response(Event.objects.none() if issubclass(response, OrganizerLevelExportMixin) else events, self.request.organizer)
            for r, response in responses
            if response
        ]
        raw_exporters = [
            ex for ex in raw_exporters
            if (
                not isinstance(ex, OrganizerLevelExportMixin) or
                perm_holder.has_organizer_permission(self.request.organizer, ex.organizer_required_permission, self.request)
            ) and ex.available_for_user(self.request.user if self.request.user and self.request.user.is_authenticated else None)
        ]
        for ex in sorted(raw_exporters, key=lambda ex: str(ex.verbose_name)):
            ex._serializer = JobRunSerializer(exporter=ex, events=events)
            exporters.append(ex)
        return exporters

    def get_serializer_kwargs(self):
        if isinstance(self.request.auth, (Device, TeamAPIToken)):
            perm_holder = self.request.auth
        else:
            perm_holder = self.request.user
        return {
            'events': perm_holder.get_events_with_permission('can_view_orders', request=self.request).filter(
                organizer=self.request.organizer
            )
        }

    def do_export(self, cf, instance, data):
        return multiexport.apply_async(kwargs={
            'organizer': self.request.organizer.id,
            'user': self.request.user.id if self.request.user.is_authenticated else None,
            'token': self.request.auth.pk if isinstance(self.request.auth, TeamAPIToken) else None,
            'device': self.request.auth.pk if isinstance(self.request.auth, Device) else None,
            'fileid': str(cf.id),
            'provider': instance.identifier,
            'form_data': data
        })


class ScheduledExportersViewSet(viewsets.ModelViewSet):
    filter_backends = (TotalOrderingFilter,)
    ordering = ('id',)
    ordering_fields = ('id', 'export_identifier', 'schedule_next_run')


class ScheduledEventExportViewSet(ScheduledExportersViewSet):
    serializer_class = ScheduledEventExportSerializer
    queryset = ScheduledEventExport.objects.none()
    permission = 'can_view_orders'

    def get_queryset(self):
        perm_holder = self.request.auth if isinstance(self.request.auth, (TeamAPIToken, Device)) else self.request.user
        if not perm_holder.has_event_permission(self.request.organizer, self.request.event, 'can_change_event_settings',
                                                request=self.request):
            if self.request.user.is_authenticated:
                qs = self.request.event.scheduled_exports.filter(owner=self.request.user)
            else:
                raise PermissionDenied('Scheduled exports require either permission to change event settings or '
                                       'user-specific API access.')
        else:
            qs = self.request.event.scheduled_exports
        return qs.select_related("owner")

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied('Creation of exports requires user-specific API access.')
        serializer.save(event=self.request.event, owner=self.request.user)
        serializer.instance.compute_next_run()
        serializer.instance.save(update_fields=["schedule_next_run"])
        self.request.event.log_action(
            'pretix.event.export.schedule.added',
            user=self.request.user,
            auth=self.request.auth,
            data=self.request.data
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['event'] = self.request.event
        ctx['exporters'] = self.exporters
        return ctx

    @cached_property
    def exporters(self):
        responses = register_data_exporters.send(self.request.event)
        exporters = [response(self.request.event, self.request.organizer) for r, response in responses if response]
        return {e.identifier: e for e in exporters}

    def perform_update(self, serializer):
        serializer.save(event=self.request.event)
        serializer.instance.compute_next_run()
        serializer.instance.error_counter = 0
        serializer.instance.error_last_message = None
        serializer.instance.save(update_fields=["schedule_next_run", "error_counter", "error_last_message"])
        self.request.event.log_action(
            'pretix.event.export.schedule.changed',
            user=self.request.user,
            auth=self.request.auth,
            data=self.request.data
        )

    def perform_destroy(self, instance):
        self.request.event.log_action(
            'pretix.event.export.schedule.deleted',
            user=self.request.user,
            auth=self.request.auth,
        )
        super().perform_destroy(instance)


class ScheduledOrganizerExportViewSet(ScheduledExportersViewSet):
    serializer_class = ScheduledOrganizerExportSerializer
    queryset = ScheduledOrganizerExport.objects.none()
    permission = None

    def get_queryset(self):
        perm_holder = self.request.auth if isinstance(self.request.auth, (TeamAPIToken, Device)) else self.request.user
        if not perm_holder.has_organizer_permission(self.request.organizer, 'can_change_organizer_settings',
                                                    request=self.request):
            if self.request.user.is_authenticated:
                qs = self.request.organizer.scheduled_exports.filter(owner=self.request.user)
            else:
                raise PermissionDenied('Scheduled exports require either permission to change organizer settings or '
                                       'user-specific API access.')
        else:
            qs = self.request.organizer.scheduled_exports
        return qs.select_related("owner")

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied('Creation of exports requires user-specific API access.')
        serializer.save(organizer=self.request.organizer, owner=self.request.user)
        serializer.instance.compute_next_run()
        serializer.instance.save(update_fields=["schedule_next_run"])
        self.request.organizer.log_action(
            'pretix.organizer.export.schedule.added',
            user=self.request.user,
            auth=self.request.auth,
            data=self.request.data
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['organizer'] = self.request.organizer
        ctx['exporters'] = self.exporters
        return ctx

    @cached_property
    def events(self):
        if isinstance(self.request.auth, (TeamAPIToken, Device)):
            return self.request.auth.get_events_with_permission('can_view_orders')
        elif self.request.user.is_authenticated:
            return self.request.user.get_events_with_permission('can_view_orders', self.request).filter(
                organizer=self.request.organizer
            )

    @cached_property
    def exporters(self):
        responses = register_multievent_data_exporters.send(self.request.organizer)
        exporters = [
            response(Event.objects.none() if issubclass(response, OrganizerLevelExportMixin) else self.events,
                     self.request.organizer)
            for r, response in responses if response
        ]
        return {e.identifier: e for e in exporters}

    def perform_update(self, serializer):
        serializer.save(organizer=self.request.organizer)
        serializer.instance.compute_next_run()
        serializer.instance.error_counter = 0
        serializer.instance.error_last_message = None
        serializer.instance.save(update_fields=["schedule_next_run", "error_counter", "error_last_message"])
        self.request.organizer.log_action(
            'pretix.organizer.export.schedule.changed',
            user=self.request.user,
            auth=self.request.auth,
            data=self.request.data
        )

    def perform_destroy(self, instance):
        self.request.organizer.log_action(
            'pretix.organizer.export.schedule.deleted',
            user=self.request.user,
            auth=self.request.auth,
        )
        super().perform_destroy(instance)
