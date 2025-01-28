from django.contrib import admin
from .models import CourseUnit, AcademicYear, Enrollment, semester, Marks
from django.utils.html import format_html
from admissions.models import Student

# Admin for CourseUnit
# @admin.register(CourseUnit)
# class CourseUnitAdmin(admin.ModelAdmin):
#     list_display = ('name', 'code', 'tutor')
#     search_fields = ('name', 'code')
#     list_filter = ('tutor',)

# Admin for AcademicYear
@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year',)
    search_fields = ('year',)

# Admin for Semester
@admin.register(semester)  # Ensure class name is correctly capitalized (Semester instead of semester)
class semesterAdmin(admin.ModelAdmin):  # Corrected the class name for consistency
    list_display = ('semester',)
    search_fields = ('semester',)
    list_filter = ('semester',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('preview_passport_photo', 'student', 'academic_year', 'semester', 'student_phone', 'student_email')
    search_fields = ('student__first_name', 'student__last_name', 'academic_year__year')
    list_filter = ('academic_year', 'semester')

    def preview_passport_photo(self, obj):
        if obj.student.passport_photo:  # Accessing passport photo from the related Student model
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.student.passport_photo.url)
        return "No photo uploaded"
    
    preview_passport_photo.short_description = "Passport Photo Preview"

    def student_phone(self, obj):
        return obj.student.phone  # Accessing phone from the related Student model
    
    student_phone.short_description = "Phone"  # Custom column name for the phone field

    def student_email(self, obj):
        return obj.student.email  # Accessing phone from the related Student model
    
    student_email.short_description = "email"  # Custom column name for the phone field

# @admin.register(Marks)
# class MarksAdmin(admin.ModelAdmin):
#     list_display = ('enrollment', 'course_unit', 'test_marks', 'final_marks', 'total_marks')
#     search_fields = ('enrollment__student__first_name', 'enrollment__student__last_name', 'course_unit__name')