# Generated by Django 5.1.5 on 2025-01-28 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0016_student_reporting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='NSIN',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='admission_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
