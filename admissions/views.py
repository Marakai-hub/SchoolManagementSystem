from django.shortcuts import render
from .models import Student
from django.core.serializers.json import DjangoJSONEncoder
import json

def student_list(request):
    name = request.GET.get('name', '')
    admission_number = request.GET.get('admission_number', '')
    year_of_admission = request.GET.get('year_of_admission', '')

    students = Student.objects.select_related('course').all()

    if name:
        students = students.filter(first_name__icontains=name) | students.filter(last_name__icontains=name)
    if admission_number:
        students = students.filter(admission_number__icontains=admission_number)
    if year_of_admission:
        students = students.filter(year_of_admission=year_of_admission)

    # Serialize student data
    student_data = [
        {
            "first_name": student.first_name,
            "last_name": student.last_name,
            "admission_number": student.admission_number,
            "course": student.course.name,
            "year_of_admission": student.year_of_admission,
            "email": student.email,
            "phone": student.phone,

        }
        for student in students
    ]

    return render(request, 'admissions/student_list.html', {
        'students': students,
        'student_json': json.dumps(student_data, cls=DjangoJSONEncoder),
    })


def student_admission_form(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'admissions/admission_form.html', {'student': student})


from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from .models import Student

def admission_letter(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    # Generate the content for the admission letter
    context = {
        'student': student,
        # You can add other context data here
    }

    # Option 1: Render it as a PDF (using a library like ReportLab or WeasyPrint)
    # Option 2: Render it as HTML (for quick preview/print via browser)
    html_content = render_to_string('admission_letter_template.html', context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="admission_letter_{student.admission_number}.pdf"'

    # Generate PDF (using WeasyPrint for example, or just render HTML)
    # pdf = weasyprint.HTML(string=html_content).write_pdf()
    # response.write(pdf)

    # If rendering HTML for quick printing
    response.write(html_content)
    return response
