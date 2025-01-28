from django.shortcuts import render
from .models import Enrollment, CourseUnit

def course_list(request):
    courses = CourseUnit.objects.all()
    return render(request, 'academics/course_list.html', {'courses': courses})
