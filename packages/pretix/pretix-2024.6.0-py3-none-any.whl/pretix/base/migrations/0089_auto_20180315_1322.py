# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-15 13:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0088_auto_20180328_1217'),
        ('pretixapi', '0001_initial')
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='shredded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invoice',
            name='shredded',
            field=models.BooleanField(default=False),
        ),
    ]
