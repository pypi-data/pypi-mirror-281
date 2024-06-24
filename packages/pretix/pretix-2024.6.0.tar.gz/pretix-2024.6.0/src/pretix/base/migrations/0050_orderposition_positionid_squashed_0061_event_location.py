# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-03 14:12
from __future__ import unicode_literals

import django.core.validators
import django.db.migrations.operations.special
import django.db.models.deletion
import django.utils.timezone
import i18nfield.fields
from django.conf import settings
from django.db import migrations, models

import pretix.base.models.event
import pretix.base.models.orders
import pretix.base.models.organizer
import pretix.base.validators


def forwards50(apps, schema_editor):
    Order = apps.get_model('pretixbase', 'Order')
    for o in Order.objects.all():
        for i, p in enumerate(o.positions.all()):
            p.positionid = i + 1
            p.save()


def invalidate_ticket_cache(apps, schema_editor):
    CachedTicket = apps.get_model('pretixbase', 'CachedTicket')
    for ct in CachedTicket.objects.all():
        try:
            if ct.cachedfile:
                ct.cachedfile.delete()
                if ct.cachedfile.file:
                    ct.cachedfile.file.delete(False)
        except models.Model.DoesNotExist:
            pass
        ct.delete()


def merge_names(apps, schema_editor):
    User = apps.get_model('pretixbase', 'User')
    for u in User.objects.all():
        if u.givenname:
            if u.familyname:
                u.fullname = u.givenname + " " + u.familyname
            else:
                u.fullname = u.givenname
        elif u.familyname:
            u.fullname = u.familyname
        u.save()


class Migration(migrations.Migration):

    replaces = [('pretixbase', '0050_orderposition_positionid'), ('pretixbase', '0051_auto_20161221_1720'), ('pretixbase', '0052_auto_20161231_1533'), ('pretixbase', '0053_auto_20170104_1252'), ('pretixbase', '0054_auto_20170107_1058'), ('pretixbase', '0055_organizerpermission_can_change_permissions'), ('pretixbase', '0056_auto_20170107_1251'), ('pretixbase', '0057_auto_20170107_1531'), ('pretixbase', '0058_auto_20170107_1533'), ('pretixbase', '0059_cachedcombinedticket'), ('pretixbase', '0060_auto_20170113_1438'), ('pretixbase', '0061_event_location')]

    dependencies = [
        ('pretixbase', '0049_checkin'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderposition',
            name='positionid',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.RunPython(
            code=forwards50,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.RunPython(
            code=invalidate_ticket_cache,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name='cachedticket',
            name='cachedfile',
        ),
        migrations.AddField(
            model_name='cachedticket',
            name='extension',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cachedticket',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=pretix.base.models.orders.cachedticket_name),
        ),
        migrations.AddField(
            model_name='cachedticket',
            name='type',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='checkin',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkins', to='pretixbase.OrderPosition'),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='price_mode',
            field=models.CharField(choices=[('none', 'No effect'), ('set', 'Set product price to'), ('subtract', 'Subtract from product price'), ('percent', 'Reduce product price by (%)')], default='none', max_length=100, verbose_name='Price mode'),
        ),
        migrations.CreateModel(
            name='RequiredAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('done', models.BooleanField(default=False)),
                ('action_type', models.CharField(max_length=255)),
                ('data', models.TextField(default='{}')),
            ],
            options={
                'ordering': ('datetime',),
            },
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.CharField(max_length=50, db_index=True, help_text='Should be short, only contain lowercase letters and numbers, and must be unique among your events. This will be used in order codes, invoice numbers, links and bank transfer references.', validators=[django.core.validators.RegexValidator(message='The slug may only contain letters, numbers, dots and dashes.', regex='^[a-zA-Z0-9.-]+$'), pretix.base.validators.EventSlugBanlistValidator()], verbose_name='Short form'),
        ),
        migrations.AddField(
            model_name='requiredaction',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pretixbase.Event'),
        ),
        migrations.AddField(
            model_name='requiredaction',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventpermission',
            name='invite_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='eventpermission',
            name='invite_token',
            field=models.CharField(blank=True, default=pretix.base.models.event.generate_invite_token, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='eventpermission',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_perms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organizerpermission',
            name='can_change_permissions',
            field=models.BooleanField(default=True, verbose_name='Can change permissions'),
        ),
        migrations.AddField(
            model_name='organizerpermission',
            name='invite_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='organizerpermission',
            name='invite_token',
            field=models.CharField(blank=True, default=pretix.base.models.organizer.generate_invite_token, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='organizerpermission',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organizer_perms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='fullname',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Full name'),
        ),
        migrations.AlterField(
            model_name='organizer',
            name='slug',
            field=models.CharField(max_length=50, db_index=True, help_text='Should be short, only contain lowercase letters and numbers, and must be unique among your events. This is being used in addresses and bank transfer references.', validators=[django.core.validators.RegexValidator(message='The slug may only contain letters, numbers, dots and dashes.', regex='^[a-zA-Z0-9.-]+$'), pretix.base.validators.OrganizerSlugBanlistValidator()], verbose_name='Short form'),
        ),
        migrations.RunPython(
            code=merge_names,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name='user',
            name='familyname',
        ),
        migrations.RemoveField(
            model_name='user',
            name='givenname',
        ),
        migrations.CreateModel(
            name='CachedCombinedTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('extension', models.CharField(max_length=255)),
                ('file', models.FileField(blank=True, null=True, upload_to=pretix.base.models.orders.cachedcombinedticket_name)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pretixbase.Order')),
                ('created', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='cachedticket',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=i18nfield.fields.I18nCharField(blank=True, max_length=200, null=True, verbose_name='Location'),
        ),
    ]
