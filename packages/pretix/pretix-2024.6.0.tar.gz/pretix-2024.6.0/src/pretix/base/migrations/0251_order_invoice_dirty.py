# Generated by Django 4.2.4 on 2023-11-13 16:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pretixbase", "0250_eventmetaproperty_filter_public"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="invoice_dirty",
            field=models.BooleanField(default=False),
        ),
    ]
