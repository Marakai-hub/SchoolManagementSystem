# Generated by Django 5.1.5 on 2025-01-28 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0015_remove_student_reporting'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='reporting',
            field=models.DateField(blank=True, null=True),
        ),
    ]
