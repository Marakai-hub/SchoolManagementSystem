from django.contrib import admin
from .models import Department, Tutor

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'department', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('department',)
