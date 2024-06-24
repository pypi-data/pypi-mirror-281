# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 13:32
from __future__ import unicode_literals

import django.core.validators
import django.db.migrations.operations.special
import django.db.models.deletion
import django_countries.fields
import i18nfield.fields
from django.core.cache import cache
from django.db import migrations, models
from i18nfield.strings import LazyI18nString

import pretix.base.models.base
import pretix.base.models.vouchers


def tax_rate_converter(app, schema_editor):
    EventSettingsStore = app.get_model('pretixbase', 'Event_SettingsStore')
    Item = app.get_model('pretixbase', 'Item')
    TaxRule = app.get_model('pretixbase', 'TaxRule')
    Order = app.get_model('pretixbase', 'Order')
    OrderPosition = app.get_model('pretixbase', 'OrderPosition')
    InvoiceLine = app.get_model('pretixbase', 'InvoiceLine')
    n = LazyI18nString({
        'en': 'VAT',
        'de': 'MwSt.',
        'de-informal': 'MwSt.'
    })

    for i in Item.objects.select_related('event').exclude(tax_rate=0):
        try:
            i.tax_rule = i.event.tax_rules.get(rate=i.tax_rate)
        except TaxRule.DoesNotExist:
            tr = i.event.tax_rules.create(rate=i.tax_rate, name=n)
            i.tax_rule = tr
        i.save()

    for o in Order.objects.select_related('event').exclude(payment_fee_tax_rate=0):
        try:
            o.payment_fee_tax_rule = o.event.tax_rules.get(rate=o.payment_fee_tax_rate)
        except TaxRule.DoesNotExist:
            tr = o.event.tax_rules.create(rate=o.payment_fee_tax_rate, name=n)
            o.tax_rule = tr
        o.save()

    for op in OrderPosition.objects.select_related('order', 'order__event').exclude(tax_rate=0):
        try:
            op.tax_rule = op.order.event.tax_rules.get(rate=op.tax_rate)
        except TaxRule.DoesNotExist:
            tr = op.order.event.tax_rules.create(rate=op.tax_rate, name=n)
            op.tax_rule = tr
        op.save()

    for il in InvoiceLine.objects.select_related('invoice', 'invoice__event').exclude(tax_rate=0):
        try:
            il.tax_name = il.invoice.event.tax_rules.get(rate=op.tax_rate).name
        except TaxRule.DoesNotExist:
            tr = il.invoice.event.tax_rules.create(rate=op.tax_rate, name=n)
            il.tax_name = tr.name
        il.save()

    for setting in EventSettingsStore.objects.filter(key='tax_rate_default'):
        try:
            tr = setting.object.tax_rules.get(rate=setting.value)
        except TaxRule.DoesNotExist:
            tr = setting.object.tax_rules.create(rate=setting.value, name=n)
        setting.value = tr.pk
        setting.save()
        cache.delete('hierarkey_{}_{}'.format('event', setting.object.pk))


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# pretix.base.migrations.0073_auto_20170716_1333

class Migration(migrations.Migration):

    replaces = [('pretixbase', '0071_auto_20170729_1616'), ('pretixbase', '0072_order_download_reminder_sent'), ('pretixbase', '0073_auto_20170716_1333'), ('pretixbase', '0074_auto_20170825_1258'), ('pretixbase', '0075_auto_20170828_0901')]

    dependencies = [
        ('pretixbase', '0070_auto_20170719_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='help_text',
            field=i18nfield.fields.I18nTextField(blank=True, help_text='If the question needs to be explained or clarified, do it here!', null=True, verbose_name='Help text'),
        ),
        migrations.AlterField(
            model_name='invoiceaddress',
            name='vat_id',
            field=models.CharField(blank=True, help_text='Only for business customers within the EU.', max_length=255, verbose_name='VAT ID'),
        ),
        migrations.AddField(
            model_name='order',
            name='download_reminder_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='TaxRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', i18nfield.fields.I18nCharField(help_text='Should be short, e.g. "VAT"', max_length=190, verbose_name='Name')),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Tax rate')),
                ('price_includes_tax', models.BooleanField(default=True, verbose_name='The configured product prices includes the tax amount')),
                ('eu_reverse_charge', models.BooleanField(default=False, help_text='Not recommended. Most events will NOT be qualified for reverse charge since the place of taxation is the location of the event. This option only enables reverse charge for business customers who entered a valid EU VAT ID. Only enable this option after consulting a tax counsel. No warranty given for correct tax calculation.', verbose_name='Use EU reverse charge taxation')),
                ('home_country', models.CharField(blank=True, choices=[('AT', 'Austria'), ('BE', 'Belgium'), ('BG', 'Bulgaria'), ('HR', 'Croatia'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('EE', 'Estonia'), ('FI', 'Finland'), ('FR', 'France'), ('DE', 'Germany'), ('GR', 'Greece'), ('HU', 'Hungary'), ('IE', 'Ireland'), ('IT', 'Italy'), ('LV', 'Latvia'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MT', 'Malta'), ('NL', 'Netherlands'), ('PL', 'Poland'), ('PT', 'Portugal'), ('RO', 'Romania'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('ES', 'Spain'), ('SE', 'Sweden'), ('UJ', 'United Kingdom')], help_text='Your country. Only relevant for EU reverse charge.', max_length=2, verbose_name='Merchant country')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tax_rules', to='pretixbase.Event')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='tax_rule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pretixbase.TaxRule', verbose_name='Sales tax'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_fee_tax_rule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pretixbase.TaxRule'),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='tax_rule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pretixbase.TaxRule'),
        ),
        migrations.RunPython(
            code=tax_rate_converter,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name='item',
            name='tax_rate',
        ),
        migrations.AddField(
            model_name='invoiceaddress',
            name='vat_id_validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='invoiceaddress',
            name='vat_id',
            field=models.CharField(blank=True, help_text='Only for business customers within the EU.', max_length=255, verbose_name='VAT ID'),
        ),
        migrations.AlterField(
            model_name='taxrule',
            name='home_country',
            field=django_countries.fields.CountryField(blank=True, help_text='Your country of residence. This is the country the EU reverse charge rule will not apply in, if configured above.', max_length=2, verbose_name='Merchant country'),
        ),
        migrations.AddField(
            model_name='cartposition',
            name='includes_tax',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='tax_name',
            field=models.CharField(default='', max_length=190),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='taxrule',
            name='eu_reverse_charge',
            field=models.BooleanField(default=False, help_text='Not recommended. Most events will NOT be qualified for reverse charge since the place of taxation is the location of the event. This option disables charging VAT for all customers outside the EU and for business customers in different EU countries that do not customers who entered a valid EU VAT ID. Only enable this option after consulting a tax counsel. No warranty given for correct tax calculation. USE AT YOUR OWN RISK.', verbose_name='Use EU reverse charge taxation rules'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='foreign_currency_display',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='foreign_currency_rate',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='foreign_currency_rate_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='checkin_attention',
            field=models.BooleanField(default=False, help_text='If you set this, the check-in app will show a visible warning that this ticket requires special attention. You can use this for example for student tickets to indicate to the person at check-in that the student ID card still needs to be checked.', verbose_name='Requires special attention'),
        ),
        migrations.AlterField(
            model_name='event',
            name='currency',
            field=models.CharField(choices=[('AED', 'AED - UAE Dirham'), ('AFN', 'AFN - Afghani'), ('ALL', 'ALL - Lek'), ('AMD', 'AMD - Armenian Dram'), ('ANG', 'ANG - Netherlands Antillean Guilder'), ('AOA', 'AOA - Kwanza'), ('ARS', 'ARS - Argentine Peso'), ('AUD', 'AUD - Australian Dollar'), ('AWG', 'AWG - Aruban Florin'), ('AZN', 'AZN - Azerbaijanian Manat'), ('BAM', 'BAM - Convertible Mark'), ('BBD', 'BBD - Barbados Dollar'), ('BDT', 'BDT - Taka'), ('BGN', 'BGN - Bulgarian Lev'), ('BHD', 'BHD - Bahraini Dinar'), ('BIF', 'BIF - Burundi Franc'), ('BMD', 'BMD - Bermudian Dollar'), ('BND', 'BND - Brunei Dollar'), ('BOB', 'BOB - Boliviano'), ('BRL', 'BRL - Brazilian Real'), ('BSD', 'BSD - Bahamian Dollar'), ('BTN', 'BTN - Ngultrum'), ('BWP', 'BWP - Pula'), ('BYN', 'BYN - Belarusian Ruble'), ('BZD', 'BZD - Belize Dollar'), ('CAD', 'CAD - Canadian Dollar'), ('CDF', 'CDF - Congolese Franc'), ('CHF', 'CHF - Swiss Franc'), ('CLP', 'CLP - Chilean Peso'), ('CNY', 'CNY - Yuan Renminbi'), ('COP', 'COP - Colombian Peso'), ('CRC', 'CRC - Costa Rican Colon'), ('CUC', 'CUC - Peso Convertible'), ('CUP', 'CUP - Cuban Peso'), ('CVE', 'CVE - Cabo Verde Escudo'), ('CZK', 'CZK - Czech Koruna'), ('DJF', 'DJF - Djibouti Franc'), ('DKK', 'DKK - Danish Krone'), ('DOP', 'DOP - Dominican Peso'), ('DZD', 'DZD - Algerian Dinar'), ('EGP', 'EGP - Egyptian Pound'), ('ERN', 'ERN - Nakfa'), ('ETB', 'ETB - Ethiopian Birr'), ('EUR', 'EUR - Euro'), ('FJD', 'FJD - Fiji Dollar'), ('FKP', 'FKP - Falkland Islands Pound'), ('GBP', 'GBP - Pound Sterling'), ('GEL', 'GEL - Lari'), ('GHS', 'GHS - Ghana Cedi'), ('GIP', 'GIP - Gibraltar Pound'), ('GMD', 'GMD - Dalasi'), ('GNF', 'GNF - Guinea Franc'), ('GTQ', 'GTQ - Quetzal'), ('GYD', 'GYD - Guyana Dollar'), ('HKD', 'HKD - Hong Kong Dollar'), ('HNL', 'HNL - Lempira'), ('HRK', 'HRK - Kuna'), ('HTG', 'HTG - Gourde'), ('HUF', 'HUF - Forint'), ('IDR', 'IDR - Rupiah'), ('ILS', 'ILS - New Israeli Sheqel'), ('INR', 'INR - Indian Rupee'), ('IQD', 'IQD - Iraqi Dinar'), ('IRR', 'IRR - Iranian Rial'), ('ISK', 'ISK - Iceland Krona'), ('JMD', 'JMD - Jamaican Dollar'), ('JOD', 'JOD - Jordanian Dinar'), ('JPY', 'JPY - Yen'), ('KES', 'KES - Kenyan Shilling'), ('KGS', 'KGS - Som'), ('KHR', 'KHR - Riel'), ('KMF', 'KMF - Comoro Franc'), ('KPW', 'KPW - North Korean Won'), ('KRW', 'KRW - Won'), ('KWD', 'KWD - Kuwaiti Dinar'), ('KYD', 'KYD - Cayman Islands Dollar'), ('KZT', 'KZT - Tenge'), ('LAK', 'LAK - Kip'), ('LBP', 'LBP - Lebanese Pound'), ('LKR', 'LKR - Sri Lanka Rupee'), ('LRD', 'LRD - Liberian Dollar'), ('LSL', 'LSL - Loti'), ('LYD', 'LYD - Libyan Dinar'), ('MAD', 'MAD - Moroccan Dirham'), ('MDL', 'MDL - Moldovan Leu'), ('MGA', 'MGA - Malagasy Ariary'), ('MKD', 'MKD - Denar'), ('MMK', 'MMK - Kyat'), ('MNT', 'MNT - Tugrik'), ('MOP', 'MOP - Pataca'), ('MRO', 'MRO - Ouguiya'), ('MUR', 'MUR - Mauritius Rupee'), ('MVR', 'MVR - Rufiyaa'), ('MWK', 'MWK - Malawi Kwacha'), ('MXN', 'MXN - Mexican Peso'), ('MYR', 'MYR - Malaysian Ringgit'), ('MZN', 'MZN - Mozambique Metical'), ('NAD', 'NAD - Namibia Dollar'), ('NGN', 'NGN - Naira'), ('NIO', 'NIO - Cordoba Oro'), ('NOK', 'NOK - Norwegian Krone'), ('NPR', 'NPR - Nepalese Rupee'), ('NZD', 'NZD - New Zealand Dollar'), ('OMR', 'OMR - Rial Omani'), ('PAB', 'PAB - Balboa'), ('PEN', 'PEN - Sol'), ('PGK', 'PGK - Kina'), ('PHP', 'PHP - Philippine Peso'), ('PKR', 'PKR - Pakistan Rupee'), ('PLN', 'PLN - Zloty'), ('PYG', 'PYG - Guarani'), ('QAR', 'QAR - Qatari Rial'), ('RON', 'RON - Romanian Leu'), ('RSD', 'RSD - Serbian Dinar'), ('RUB', 'RUB - Russian Ruble'), ('RWF', 'RWF - Rwanda Franc'), ('SAR', 'SAR - Saudi Riyal'), ('SBD', 'SBD - Solomon Islands Dollar'), ('SCR', 'SCR - Seychelles Rupee'), ('SDG', 'SDG - Sudanese Pound'), ('SEK', 'SEK - Swedish Krona'), ('SGD', 'SGD - Singapore Dollar'), ('SHP', 'SHP - Saint Helena Pound'), ('SLL', 'SLL - Leone'), ('SOS', 'SOS - Somali Shilling'), ('SRD', 'SRD - Surinam Dollar'), ('SSP', 'SSP - South Sudanese Pound'), ('STD', 'STD - Dobra'), ('SVC', 'SVC - El Salvador Colon'), ('SYP', 'SYP - Syrian Pound'), ('SZL', 'SZL - Lilangeni'), ('THB', 'THB - Baht'), ('TJS', 'TJS - Somoni'), ('TMT', 'TMT - Turkmenistan New Manat'), ('TND', 'TND - Tunisian Dinar'), ('TOP', 'TOP - Pa’anga'), ('TRY', 'TRY - Turkish Lira'), ('TTD', 'TTD - Trinidad and Tobago Dollar'), ('TWD', 'TWD - New Taiwan Dollar'), ('TZS', 'TZS - Tanzanian Shilling'), ('UAH', 'UAH - Hryvnia'), ('UGX', 'UGX - Uganda Shilling'), ('USD', 'USD - US Dollar'), ('UYU', 'UYU - Peso Uruguayo'), ('UZS', 'UZS - Uzbekistan Sum'), ('VEF', 'VEF - Bolívar'), ('VND', 'VND - Dong'), ('VUV', 'VUV - Vatu'), ('WST', 'WST - Tala'), ('XAF', 'XAF - CFA Franc BEAC'), ('XAG', 'XAG - Silver'), ('XAU', 'XAU - Gold'), ('XBA', 'XBA - Bond Markets Unit European Composite Unit (EURCO)'), ('XBB', 'XBB - Bond Markets Unit European Monetary Unit (E.M.U.-6)'), ('XBC', 'XBC - Bond Markets Unit European Unit of Account 9 (E.U.A.-9)'), ('XBD', 'XBD - Bond Markets Unit European Unit of Account 17 (E.U.A.-17)'), ('XCD', 'XCD - East Caribbean Dollar'), ('XDR', 'XDR - SDR (Special Drawing Right)'), ('XOF', 'XOF - CFA Franc BCEAO'), ('XPD', 'XPD - Palladium'), ('XPF', 'XPF - CFP Franc'), ('XPT', 'XPT - Platinum'), ('XSU', 'XSU - Sucre'), ('XTS', 'XTS - Codes specifically reserved for testing purposes'), ('XUA', 'XUA - ADB Unit of Account'), ('XXX', 'XXX - The codes assigned for transactions where no currency is involved'), ('YER', 'YER - Yemeni Rial'), ('ZAR', 'ZAR - Rand'), ('ZMW', 'ZMW - Zambian Kwacha'), ('ZWL', 'ZWL - Zimbabwe Dollar')], default='EUR', max_length=10, verbose_name='Event currency'),
        ),
        migrations.AlterField(
            model_name='taxrule',
            name='price_includes_tax',
            field=models.BooleanField(default=True, verbose_name='The configured product prices include the tax amount'),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='code',
            field=models.CharField(db_index=True, default=pretix.base.models.vouchers.generate_code, max_length=255, validators=[django.core.validators.MinLengthValidator(5)], verbose_name='Voucher code'),
        ),
        migrations.CreateModel(
            name='EventMetaProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Can not contain spaces or special characters execpt underscores', max_length=50, validators=[django.core.validators.RegexValidator(message='The property name may only contain letters, numbers and underscores.', regex='^[a-zA-Z0-9_]+$')], verbose_name='Name')),
                ('default', models.TextField()),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meta_properties', to='pretixbase.Organizer')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, pretix.base.models.base.LoggingMixin),
        ),
        migrations.CreateModel(
            name='EventMetaValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meta_values', to='pretixbase.Event')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_values', to='pretixbase.EventMetaProperty')),
            ],
            bases=(models.Model, pretix.base.models.base.LoggingMixin),
        ),
        migrations.CreateModel(
            name='SubEventMetaValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subevent_values', to='pretixbase.EventMetaProperty')),
                ('subevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meta_values', to='pretixbase.SubEvent')),
            ],
            bases=(models.Model, pretix.base.models.base.LoggingMixin),
        ),
        migrations.AlterUniqueTogether(
            name='subeventmetavalue',
            unique_together=set([('subevent', 'property')]),
        ),
        migrations.AlterUniqueTogether(
            name='eventmetavalue',
            unique_together=set([('event', 'property')]),
        ),
    ]
