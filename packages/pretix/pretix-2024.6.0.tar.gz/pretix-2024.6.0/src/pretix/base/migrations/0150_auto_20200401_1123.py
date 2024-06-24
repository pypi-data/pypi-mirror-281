# Generated by Django 3.0.4 on 2020-04-01 11:24

import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0149_order_cancellation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartposition',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cartposition',
            name='company',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cartposition',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='cartposition',
            name='state',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cartposition',
            name='street',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='cartposition',
            name='zipcode',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='company',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='state',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='street',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='zipcode',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
