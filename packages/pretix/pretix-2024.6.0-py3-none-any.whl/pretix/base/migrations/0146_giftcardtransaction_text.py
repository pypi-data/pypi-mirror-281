# Generated by Django 2.2.4 on 2020-03-02 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0145_auto_20200210_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftcardtransaction',
            name='text',
            field=models.TextField(null=True),
        ),
    ]
