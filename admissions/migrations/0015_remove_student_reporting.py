# Generated by Django 5.1.5 on 2025-01-28 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0014_alter_student_reporting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='reporting',
        ),
    ]
