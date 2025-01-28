# Generated by Django 5.1.5 on 2025-01-22 06:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bursary', '0006_alter_payment_date_alter_payment_payment_type_ledger_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('default_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='LedgerPaymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ledger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_types', to='bursary.ledger')),
                ('payment_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bursary.paymenttype')),
            ],
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bursary.paymenttype'),
        ),
    ]
