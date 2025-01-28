# Generated by Django 5.1.5 on 2025-01-19 09:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0004_student_academic_documents_student_former_school_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='academic_documents',
        ),
        migrations.RemoveField(
            model_name='student',
            name='is_married',
        ),
        migrations.RemoveField(
            model_name='student',
            name='marital_status',
        ),
        migrations.RemoveField(
            model_name='student',
            name='spouse_contact',
        ),
        migrations.RemoveField(
            model_name='student',
            name='spouse_name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='spouse_occupation',
        ),
        migrations.AddField(
            model_name='student',
            name='passport_photo',
            field=models.ImageField(blank=True, null=True, upload_to='passport_photos/'),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='student_documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='admissions.student')),
            ],
        ),
    ]
