# Generated by Django 3.2.12 on 2022-03-22 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0208_auto_20220214_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='info',
            field=models.JSONField(null=True),
        ),
    ]
