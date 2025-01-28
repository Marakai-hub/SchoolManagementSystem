from django.db import models
from admissions.models import Student
from academics.models import Enrollment
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from django.db.models import Max
from decimal import Decimal


class PaymentType(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the payment type, e.g., "School Fees"
    
    def __str__(self):
        return self.name


class PaymentTypeBreakdown(models.Model):
    ledger = models.ForeignKey('Ledger', on_delete=models.CASCADE, related_name='payment_type_breakdowns')  # Link to the specific Ledger
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)  # Payment type for this breakdown
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Amount for this specific payment type

    def __str__(self):
        return f"{self.payment_type.name} - {self.amount}"


from decimal import Decimal

class Ledger(models.Model):
    def generate_ledger_number(self):
        last_ledger = Ledger.objects.aggregate(Max('id'))  # Get the last ledger ID
        next_ledger_id = last_ledger['id__max'] + 1 if last_ledger['id__max'] else 1
        ledger_number = f"LEDG-{next_ledger_id:04d}"  # Format as 'LEDG-0001', 'LEDG-0002', etc.
        return ledger_number

    ledger_number = models.CharField(max_length=10, unique=True, editable=False)  # Removed default

    student = models.ForeignKey('admissions.Student', on_delete=models.CASCADE, related_name="ledgers")
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE)
    semester = models.ForeignKey('academics.Semester', on_delete=models.CASCADE)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    required_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    generated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.academic_year.year} - {self.semester.semester} - Ledger No: {self.ledger_number}"

    def update_required_amount(self):
        total_breakdown = self.payment_type_breakdowns.aggregate(total=Sum('amount'))['total']
        self.required_amount = total_breakdown or Decimal('0.00')  # Ensure this is a Decimal value

    def save(self, *args, **kwargs):
        # Ensure primary key is assigned before generating ledger_number
        if not self.pk:
            super().save(*args, **kwargs)  # Save to generate primary key
        
        # Generate ledger number after primary key is set
        if not self.ledger_number:
            self.ledger_number = self.generate_ledger_number()

        self.update_required_amount()

        # Ensure the calculation is done with Decimal
        self.balance = self.required_amount - Decimal(self.total_paid)  # Convert total_paid to Decimal

        # Save the Ledger instance first
        super().save(*args, **kwargs)  # Save again to apply ledger_number and other updates

        # Now, ensure that PaymentTypeBreakdowns are correctly linked and saved
        # You must manually associate each breakdown with the Ledger instance after it is saved
        for breakdown in self.payment_type_breakdowns.all():
            breakdown.ledger = self  # Ensure breakdown is linked to this Ledger
            breakdown.save()  # Save the breakdown

        # Explicitly add the most recent breakdown after saving the Ledger
        if self.payment_type_breakdowns.exists():
            # Make sure the last breakdown is being added
            latest_breakdown = self.payment_type_breakdowns.last()
            latest_breakdown.ledger = self  # Link it with the current ledger
            latest_breakdown.save()  # Save the latest breakdown
            


class Payment(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, related_name="payments", null=True, blank=True)

    def __str__(self):
        return f"{self.payment_type.name} - {self.amount} - {self.date.strftime('%Y-%m-%d')}"
