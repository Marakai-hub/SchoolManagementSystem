from django.db import models, transaction

class Course(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10, unique=True)  # e.g., CS for Computer Science
    duration = models.IntegerField(help_text="Duration in months")  # Course duration in months

    def __str__(self):
        return f"{self.name} ({self.short_name})"


class Student(models.Model):
    # Bio Data
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)  # Optional middle name
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=1, 
        choices=[('M', 'Male'), ('F', 'Female')],
        help_text="Select gender"
    )  # Gender choices
    religion = models.CharField(max_length=50)
    nationality = models.CharField(max_length=100)
    passport_photo = models.ImageField(upload_to='passport_photos/', blank=True, null=True)

    # Contact and Address Details
    birth_district = models.CharField(max_length=100)
    subcounty = models.CharField(max_length=100)
    parish = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    # Parents Information
    father_name = models.CharField(max_length=100)
    father_phone = models.CharField(max_length=15)
    mother_name = models.CharField(max_length=100)
    mother_phone = models.CharField(max_length=15)

    # Sponsor Information
    sponsor_name = models.CharField(max_length=100)

    # Previous School Information
    former_school = models.CharField(max_length=200, blank=True)
    former_school_district = models.CharField(max_length=100, blank=True)

    # Academic Information
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    admission_number = models.CharField(max_length=20, unique=True, blank=True)
    reporting = models.DateField( blank=True, null=True)
    year_of_admission = models.CharField(max_length=15)
    
    NSIN = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.admission_number:
            with transaction.atomic():
                count = Student.objects.filter(course=self.course).count() + 1
                proposed_admission_number = f"{str(count).zfill(3)}-{self.course.short_name}"

                # Ensure the admission number is unique
                while Student.objects.filter(admission_number=proposed_admission_number).exists():
                    count += 1
                    proposed_admission_number = f"{str(count).zfill(3)}-{self.course.short_name}"

                self.admission_number = proposed_admission_number
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.admission_number})"


class Document(models.Model):
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='documents'
    )
    name = models.CharField(max_length=200)  # Name or description of the document
    file = models.FileField(upload_to='student_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.student.first_name} {self.student.last_name}"
