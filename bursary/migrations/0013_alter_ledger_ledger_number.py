# Generated by Django 5.1.5 on 2025-01-26 12:43

import bursary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bursary', '0012_alter_ledger_ledger_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger',
            name='ledger_number',
            field=models.CharField(default=bursary.models.Ledger.generate_ledger_number, editable=False, max_length=10, unique=True),
        ),
    ]
