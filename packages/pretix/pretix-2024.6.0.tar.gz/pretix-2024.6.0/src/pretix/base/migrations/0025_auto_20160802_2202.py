# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-02 22:02
from __future__ import unicode_literals

from django.db import migrations, models

import pretix.base.models.orders
import pretix.base.models.vouchers


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0024_auto_20160728_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='object_id',
            field=models.PositiveIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(db_index=True, max_length=16, verbose_name='Order code'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('n', 'pending'), ('p', 'paid'), ('e', 'expired'), ('c', 'cancelled'), ('r', 'refunded')], db_index=True, max_length=3, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='orderposition',
            name='secret',
            field=models.CharField(db_index=True, default="invalid", max_length=64),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='code',
            field=models.CharField(db_index=True, default=pretix.base.models.vouchers.generate_code, max_length=255, verbose_name='Voucher code'),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='tag',
            field=models.CharField(blank=True, db_index=True, help_text='You can use this field to group multiple vouchers together. If you enter the same value for multiple vouchers, you can get statistics on how many of them have been redeemed etc.', max_length=255, verbose_name='Tag'),
        ),
    ]
