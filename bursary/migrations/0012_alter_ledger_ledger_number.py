# Generated by Django 5.1.5 on 2025-01-26 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bursary', '0011_alter_ledger_required_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger',
            name='ledger_number',
            field=models.CharField(editable=False, max_length=10, unique=True),
        ),
    ]
