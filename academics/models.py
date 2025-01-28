from django.db import models
from admissions.models import Student
from staff.models import Tutor
from django.apps import apps


class AcademicYear(models.Model):
    year = models.CharField(unique=True, max_length=4)

    def __str__(self):
        return str(self.year)


class semester(models.Model):
    semester = models.CharField(unique=True, max_length=4)

    def __str__(self):
        return str(self.semester)


class CourseUnit(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey(semester, on_delete=models.SET_NULL, null=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester = models.ForeignKey(semester, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.student} - {self.academic_year.year}"


from decimal import Decimal

class Marks(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    course_unit = models.ForeignKey(CourseUnit, on_delete=models.CASCADE)
    test_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    final_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def total_marks(self):
        """Calculate total marks (test + final)"""
        if self.test_marks is not None and self.final_marks is not None:
            # Convert the float to Decimal to avoid the TypeError
            test_weight = Decimal('0.30')
            final_weight = Decimal('0.70')

            total = (self.test_marks * test_weight) + (self.final_marks * final_weight)
            return total.quantize(Decimal('0.01'))  # Rounding to two decimal places
        return None

    def __str__(self):
        return f"{self.enrollment.student} - {self.course_unit.name} Marks"