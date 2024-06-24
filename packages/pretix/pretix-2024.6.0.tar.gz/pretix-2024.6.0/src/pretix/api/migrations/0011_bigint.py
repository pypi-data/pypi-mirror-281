# Generated by Django 4.2.4 on 2023-09-26 12:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pretixapi", "0010_webhook_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apicall",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="oauthaccesstoken",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="oauthapplication",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="oauthgrant",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="oauthidtoken",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="oauthrefreshtoken",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="webhook",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="webhookcall",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="webhookeventlistener",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False
            ),
        ),
    ]
