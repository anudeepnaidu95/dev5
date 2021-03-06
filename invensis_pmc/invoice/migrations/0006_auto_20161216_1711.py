# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-16 11:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_invoicesetup_paymentterms_wiretransferinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChequeSetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_applicable', models.BooleanField(default=True)),
                ('company_name', models.CharField(max_length=255)),
                ('bank', models.CharField(max_length=255)),
                ('account_number', models.CharField(max_length=20)),
                ('addressline1', models.CharField(blank=True, max_length=255, null=True)),
                ('addressline2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'ChequeSetup',
                'verbose_name_plural': 'ChequeSetups',
            },
        ),
        migrations.CreateModel(
            name='PaymentModeSetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('AED', 'United Arab Emirates Dirham'), ('AFN', 'Afghanistan Afghani'), ('ALL', 'Albania Lek'), ('AMD', 'Armenia Dram'), ('ANG', 'Netherlands Antilles Guilder'), ('AOA', 'Angola Kwanza'), ('ARS', 'Argentina Peso'), ('AUD', 'Australia Dollar'), ('AWG', 'Aruba Guilder'), ('AZN', 'Azerbaijan New Manat'), ('BAM', 'Bosnia and Herzegovina Convertible Marka'), ('BBD', 'Barbados Dollar'), ('BDT', 'Bangladesh Taka'), ('BGN', 'Bulgaria Lev'), ('BHD', 'Bahrain Dinar'), ('BIF', 'Burundi Franc'), ('BMD', 'Bermuda Dollar'), ('BND', 'Brunei Darussalam Dollar'), ('BOB', 'Bolivia Bol\xedviano'), ('BRL', 'Brazil Real'), ('BSD', 'Bahamas Dollar'), ('BTN', 'Bhutan Ngultrum'), ('BWP', 'Botswana Pula'), ('BYN', 'Belarus Ruble'), ('BZD', 'Belize Dollar'), ('CAD', 'Canada Dollar'), ('CDF', 'Congo/Kinshasa Franc'), ('CHF', 'Switzerland Franc'), ('CLP', 'Chile Peso'), ('CNY', 'China Yuan Renminbi'), ('COP', 'Colombia Peso'), ('CRC', 'Costa Rica Colon'), ('CUC', 'Cuba Convertible Peso'), ('CUP', 'Cuba Peso'), ('CVE', 'Cape Verde Escudo'), ('CZK', 'Czech Republic Koruna'), ('DJF', 'Djibouti Franc'), ('DKK', 'Denmark Krone'), ('DOP', 'Dominican Republic Peso'), ('DZD', 'Algeria Dinar'), ('EGP', 'Egypt Pound'), ('ERN', 'Eritrea Nakfa'), ('ETB', 'Ethiopia Birr'), ('EUR', 'Euro Member Countries'), ('FJD', 'Fiji Dollar'), ('FKP', 'Falkland Islands (Malvinas) Pound'), ('GBP', 'United Kingdom Pound'), ('GEL', 'Georgia Lari'), ('GGP', 'Guernsey Pound'), ('GHS', 'Ghana Cedi'), ('GIP', 'Gibraltar Pound'), ('GMD', 'Gambia Dalasi'), ('GNF', 'Guinea Franc'), ('GTQ', 'Guatemala Quetzal'), ('GYD', 'Guyana Dollar'), ('HKD', 'Hong Kong Dollar'), ('HNL', 'Honduras Lempira'), ('HRK', 'Croatia Kuna'), ('HTG', 'Haiti Gourde'), ('HUF', 'Hungary Forint'), ('IDR', 'Indonesia Rupiah'), ('ILS', 'Israel Shekel'), ('IMP', 'Isle of Man Pound'), ('INR', 'India Rupee'), ('IQD', 'Iraq Dinar'), ('IRR', 'Iran Rial'), ('ISK', 'Iceland Krona'), ('JEP', 'Jersey Pound'), ('JMD', 'Jamaica Dollar'), ('JOD', 'Jordan Dinar'), ('JPY', 'Japan Yen'), ('KES', 'Kenya Shilling'), ('KGS', 'Kyrgyzstan Som'), ('KHR', 'Cambodia Riel'), ('KMF', 'Comoros Franc'), ('KPW', 'Korea (North) Won'), ('KRW', 'Korea (South) Won'), ('KWD', 'Kuwait Dinar'), ('KYD', 'Cayman Islands Dollar'), ('KZT', 'Kazakhstan Tenge'), ('LAK', 'Laos Kip'), ('LBP', 'Lebanon Pound'), ('LKR', 'Sri Lanka Rupee'), ('LRD', 'Liberia Dollar'), ('LSL', 'Lesotho Loti'), ('LYD', 'Libya Dinar'), ('MAD', 'Morocco Dirham'), ('MDL', 'Moldova Leu'), ('MGA', 'Madagascar Ariary'), ('MKD', 'Macedonia Denar'), ('MMK', 'Myanmar (Burma) Kyat'), ('MNT', 'Mongolia Tughrik'), ('MOP', 'Macau Pataca'), ('MRO', 'Mauritania Ouguiya'), ('MUR', 'Mauritius Rupee'), ('MVR', 'Maldives (Maldive Islands) Rufiyaa'), ('MWK', 'Malawi Kwacha'), ('MXN', 'Mexico Peso'), ('MYR', 'Malaysia Ringgit'), ('MZN', 'Mozambique Metical'), ('NAD', 'Namibia Dollar'), ('NGN', 'Nigeria Naira'), ('NIO', 'Nicaragua Cordoba'), ('NOK', 'Norway Krone'), ('NPR', 'Nepal Rupee'), ('NZD', 'New Zealand Dollar'), ('OMR', 'Oman Rial'), ('PAB', 'Panama Balboa'), ('PEN', 'Peru Sol'), ('PGK', 'Papua New Guinea Kina'), ('PHP', 'Philippines Peso'), ('PKR', 'Pakistan Rupee'), ('PLN', 'Poland Zloty'), ('PYG', 'Paraguay Guarani'), ('QAR', 'Qatar Riyal'), ('RON', 'Romania New Leu'), ('RSD', 'Serbia Dinar'), ('RUB', 'Russia Ruble'), ('RWF', 'Rwanda Franc'), ('SAR', 'Saudi Arabia Riyal'), ('SBD', 'Solomon Islands Dollar'), ('SCR', 'Seychelles Rupee'), ('SDG', 'Sudan Pound'), ('SEK', 'Sweden Krona'), ('SGD', 'Singapore Dollar'), ('SHP', 'Saint Helena Pound'), ('SLL', 'Sierra Leone Leone'), ('SOS', 'Somalia Shilling'), ('SPL', 'Seborga Luigino'), ('SRD', 'Suriname Dollar'), ('STD', 'S\xe3o Tom\xe9 and Pr\xedncipe Dobra'), ('SVC', 'El Salvador Colon'), ('SYP', 'Syria Pound'), ('SZL', 'Swaziland Lilangeni'), ('THB', 'Thailand Baht'), ('TJS', 'Tajikistan Somoni'), ('TMT', 'Turkmenistan Manat'), ('TND', 'Tunisia Dinar'), ('TOP', 'Tonga Paanga'), ('TRY', 'Turkey Lira'), ('TTD', 'Trinidad and Tobago Dollar'), ('TVD', 'Tuvalu Dollar'), ('TWD', 'Taiwan New Dollar'), ('TZS', 'Tanzania Shilling'), ('UAH', 'Ukraine Hryvnia'), ('UGX', 'Uganda Shilling'), ('USD', 'United States Dollar'), ('UYU', 'Uruguay Peso'), ('UZS', 'Uzbekistan Som'), ('VEF', 'Venezuela Bolivar'), ('VND', 'Viet Nam Dong'), ('VUV', 'Vanuatu Vatu'), ('WST', 'Samoa Tala'), ('XAF', 'Communaut\xe9 Financi\xe8re Africaine (BEAC) CFA Franc BEAC'), ('XCD', 'East Caribbean Dollar'), ('XDR', 'International Monetary Fund (IMF) Special Drawing Rights'), ('XOF', 'Communaut\xe9 Financi\xe8re Africaine (BCEAO) Franc'), ('XPF', 'Comptoirs Fran\xe7ais du Pacifique (CFP) Franc'), ('YER', 'Yemen Rial'), ('ZAR', 'South Africa Rand'), ('ZMW', 'Zambia Kwacha'), ('ZWD', 'Zimbabwe Dollar')], max_length=10)),
            ],
            options={
                'verbose_name': 'PaymentModeSetup',
                'verbose_name_plural': 'PaymentModeSetups',
            },
        ),
        migrations.CreateModel(
            name='PaypalSetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_applicable', models.BooleanField(default=True)),
                ('surcharge_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('payable_to_email', models.CharField(max_length=100)),
                ('payment_mode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='invoice.PaymentModeSetup')),
            ],
            options={
                'verbose_name': 'PaypalSetup',
                'verbose_name_plural': 'PaypalSetups',
            },
        ),
        migrations.CreateModel(
            name='WiretransferSetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_applicable', models.BooleanField(default=True)),
                ('show_only_beneficiary_details', models.BooleanField(default=False)),
                ('correspondent_bank_label', models.CharField(blank=True, max_length=255, null=True)),
                ('correspondent_bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('correspondent_bank_address', models.CharField(blank=True, max_length=255, null=True)),
                ('correspondent_bank_account_number', models.CharField(blank=True, max_length=30, null=True)),
                ('correspondent_bank_swift_code', models.CharField(blank=True, max_length=30, null=True)),
                ('beneficiary_banker_label', models.CharField(blank=True, max_length=255, null=True)),
                ('beneficiary_banker_name', models.CharField(blank=True, max_length=255, null=True)),
                ('beneficiary_banker_address', models.CharField(blank=True, max_length=255, null=True)),
                ('beneficiary_banker_swift_code', models.CharField(blank=True, max_length=30, null=True)),
                ('further_credit_to_label', models.CharField(blank=True, max_length=255, null=True)),
                ('further_credit_to_bank', models.CharField(blank=True, max_length=255, null=True)),
                ('further_credit_to_bank_address', models.CharField(blank=True, max_length=255, null=True)),
                ('beneficiary_label', models.CharField(blank=True, max_length=255, null=True)),
                ('beneficiary_name', models.CharField(max_length=255)),
                ('beneficiary_bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('beneficiary_bank_address', models.CharField(blank=True, max_length=255, null=True)),
                ('beneficiary_routing_number', models.CharField(blank=True, max_length=30, null=True)),
                ('beneficiary_account_number', models.CharField(blank=True, max_length=30, null=True)),
                ('beneficiary_swift_code', models.CharField(blank=True, max_length=30, null=True)),
                ('payment_mode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='invoice.PaymentModeSetup')),
            ],
            options={
                'verbose_name': 'WiretransferSetup',
                'verbose_name_plural': 'WiretransferSetups',
            },
        ),
        migrations.AddField(
            model_name='invoice',
            name='is_final',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chequesetup',
            name='payment_mode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='invoice.PaymentModeSetup'),
        ),
    ]
