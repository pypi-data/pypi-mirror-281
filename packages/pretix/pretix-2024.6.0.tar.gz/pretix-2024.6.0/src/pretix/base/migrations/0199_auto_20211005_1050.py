# Generated by Django 3.2.4 on 2021-10-05 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0198_invoice_sent_to_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='require_membership_hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='itemvariation',
            name='require_membership_hidden',
            field=models.BooleanField(default=False),
        ),
    ]
