from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from django.shortcuts import render
import json
from .models import Student, Document, Course

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1
    fields = ['name', 'file']
    max_num = 10

from django.utils.html import format_html

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Student Bio Data', {
            'fields': [
                'preview_passport_photo', 'passport_photo', 'first_name', 'middle_name',
                'last_name', 'date_of_birth', 'gender',
                'religion', 'nationality'
            ]
        }),
        ('Contact and Address Details', {
            'fields': [
                'birth_district', 'subcounty', 'parish',
                'village', 'phone', 'email'
            ]
        }),
        ('Parents Information', {
            'fields': [
                'father_name', 'father_phone',
                'mother_name', 'mother_phone'
            ]
        }),
        ('Sponsor Information', {
            'fields': ['sponsor_name']
        }),
        ('Previous School Information', {
            'fields': ['former_school', 'former_school_district']
        }),
        ('Academic Information', {
            'fields': ['course', 'admission_number', 'year_of_admission', 'reporting', 'NSIN']
        }),
    ]
    
    inlines = [DocumentInline]
    list_display = ['first_name', 'last_name', 'admission_number', 'course', 'year_of_admission', 'view_admission_form', 'print_admission_letter', 'enrollment_status']
    search_fields = ['first_name', 'last_name', 'admission_number']
    list_filter = ['course', 'year_of_admission']
    readonly_fields = ['admission_number', 'preview_passport_photo']

    def view_admission_form(self, obj):
        url = reverse('student_admission_form', args=[obj.id])
        return format_html('<a href="{}" target="_blank">Print Admission Letter</a>', url)

    view_admission_form.short_description = 'Print Admission Letter'

    def preview_passport_photo(self, obj):
        if obj.passport_photo:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.passport_photo.url)
        return "No photo uploaded"

    preview_passport_photo.short_description = "Passport Photo Preview"

    def print_admission_letter(self, obj):
        url = reverse('admission_letter', args=[obj.id])
        return format_html('<a href="{}" target="_blank">Download Admission Letter</a>', url)

    print_admission_letter.short_description = 'Download Admission Letter'

    def enrollment_status(self, obj):
        url = reverse('admission_letter', args=[obj.id])
        return format_html('<a href="{}" target="_blank">Enrollment Status</a>', url)

    print_admission_letter.short_description = 'Admission Letter'
    # Override changelist_view to add the graphical data
    # change_list_template = "admin/graphical_analysis.html"
    
    # def changelist_view(self, request, extra_context=None):
    #     # Prepare data for analysis (students per course and gender distribution)
    #     student_per_course = Course.objects.annotate(student_count=Count('student')).values('name', 'student_count')
    #     gender_distribution = Student.objects.values('gender').annotate(count=Count('id'))

    #     extra_context = extra_context or {}
    #     extra_context.update({
    #         'student_per_course': json.dumps(list(student_per_course)),
    #         'gender_distribution': json.dumps(list(gender_distribution)),
    #     })
    #     return super().changelist_view(request, extra_context=extra_context)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'duration']
    search_fields = ['name', 'short_name']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'student', 'uploaded_at']
    search_fields = ['name', 'student__first_name', 'student__last_name']
