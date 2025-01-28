from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('student/admission-form/<int:student_id>/', views.student_admission_form, name='student_admission_form'),
    path('admission-letter/<int:student_id>/', views.admission_letter, name='admission_letter'),
]
