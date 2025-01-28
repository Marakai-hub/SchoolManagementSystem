from django.contrib import admin
from .models import Payment, Ledger
from academics.models import Enrollment
from admissions.models import Student
from datetime import datetime
from django.utils.html import format_html
from import_export.admin import ExportMixin, ImportMixin
from decimal import Decimal


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('get_student_name', 'get_student_course', 'get_student_year_semester', 'payment_type', 'amount', 'date')
    search_fields = ('enrollment__student__first_name', 'enrollment__student__last_name', 'payment_type')
    list_filter = ('payment_type', 'date')
    readonly_fields = ('ledger_view', 'form_data_view', 'payment_history_view')

    fieldsets = [
        ('Form', {
            'classes': ('collapse',),
            'fields': ('enrollment', 'payment_type', 'amount',),
        }),
        ('Student General Ledger', {
            'classes': ('collapse',),
            'fields': ('ledger_view',),
        }),
        ('Student Form Data', {
            'classes': ('collapse',),
            'fields': ('form_data_view',),
        }),
        ('Payment History', {
            'classes': ('collapse',),
            'fields': ('payment_history_view',),
        }),
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related('enrollment__student', 'enrollment__academic_year', 'enrollment__semester')
        return queryset

    def get_student_name(self, obj):
        if obj.enrollment and obj.enrollment.student:
            return f"{obj.enrollment.student.first_name} {obj.enrollment.student.last_name}"
        return "No student assigned"

    get_student_name.short_description = 'Student Name'

    def get_student_course(self, obj):
        if obj.enrollment and obj.enrollment.student and obj.enrollment.student.course:
            return obj.enrollment.student.course.name
        return "No course assigned"

    get_student_course.short_description = 'Course'

    def get_student_year_semester(self, obj):
        if obj.enrollment and obj.enrollment.academic_year and obj.enrollment.semester:
            return f"{obj.enrollment.academic_year.year} - {obj.enrollment.semester.semester}"
        return "Year/Semester not assigned"

    get_student_year_semester.short_description = 'Year & Semester'

    def ledger_view(self, obj):
        if not obj or not obj.enrollment or not obj.enrollment.student:
            return "No ledger available."

        student = obj.enrollment.student
        full_name = f"{student.first_name} {student.last_name}"
        course = student.course.name if student.course else "No course assigned"
        image_url = student.passport_photo.url if student.passport_photo else None
        payments = Payment.objects.filter(enrollment__student=student).order_by('date')
        total_paid = Decimal(0)  # Initialize total_paid as Decimal
        ledger = Ledger.objects.filter(student=student).first()
        required_amount = ledger.required_amount if ledger else Decimal(1000000.0)  # Convert to Decimal

        grouped_payments = {}
        for payment in payments:
            year_semester = f"{payment.enrollment.academic_year.year} - {payment.enrollment.semester.semester}"
            if year_semester not in grouped_payments:
                grouped_payments[year_semester] = []
            grouped_payments[year_semester].append(payment)

        ledger = """
            <div style="font-family: Arial, sans-serif; border: 1px solid #ddd; padding: 20px; width: 1200px; position:relative;">
                <div style="text-align: center;">
                    <h2 style="color: #0056b3; margin-bottom: 5px; padding-left:30px; position:absolute; top:-22px; font-weight:3000; background:#ffffff;">Student Payment Ledger</h2>
                    <p style="margin: 0; font-size: 14px; color: #555;">Generated on: {}</p>
                </div>
                <div style="display: flex; margin-top: 20px;">
                    <div style="flex: 0 0 auto; margin-right: 20px;">
                        {}
                    </div>
                    <div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
                        <h4 style="margin: 0; font-size: 20px;">Student Details</h4>
                        <p style="margin: 0; font-size: 14px; color: #555;"><strong>Name:</strong> {}</p>
                        <p style="margin: 0; font-size: 14px; color: #555;"><strong>Course:</strong> {}</p>
                    </div>
                </div>
        """.format(
            datetime.now().strftime('%Y-%m-%d'),
            f'<img src="{image_url}" alt="{full_name}" style="max-height: 150px; max-width: 150px; margin-bottom: 10px; border-radius: 10px;">'
            if image_url else "",
            full_name,
            course,
        )

        for year_semester, payments_in_group in grouped_payments.items():
            ledger += f"""
                <h3 style="color: #333; margin-top: 20px;">{year_semester}</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background-color: #f2f2f2;">
                            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Date of Payment</th>
                            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Payment Type</th>
                            <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">Amount</th>
                        </tr>
                    </thead>
                    <tbody>
            """

            group_total_paid = Decimal(0)
            for payment in payments_in_group:
                ledger += format_html(
                    """
                        <tr>
                            <td style="border: 1px solid #ddd; padding: 8px;">{}</td>
                            <td style="border: 1px solid #ddd; padding: 8px;">{}</td>
                            <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">{}</td>
                        </tr>
                    """,
                    payment.date.strftime('%Y-%m-%d'),
                    payment.payment_type,
                    f"{payment.amount:,.2f}",
                )
                group_total_paid += payment.amount
                total_paid += payment.amount

            # Now calculate the balance correctly
            balance = required_amount - total_paid

            ledger += format_html(
                """
                    </tbody>
                    <tfoot>
                        <tr>
                            <th colspan="2" style="border: 1px solid #ddd; padding: 8px; text-align: right;">Total Paid:</th>
                            <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">{}</td>
                        </tr>
                        <tr>
                            <th colspan="2" style="border: 1px solid #ddd; padding: 8px; text-align: right;">Balance:</th>
                            <td style="border: 1px solid #ddd; padding: 8px; text-align: right; color: {}">{}</td>
                        </tr>
                    </tfoot>
                </table>
            """,
            f"{group_total_paid:,.2f}",
            "red" if balance > 0 else "green",
            f"{balance:,.2f}"
            )

        ledger += """
                <div style="text-align: center; margin-top: 20px;">
                    <p style="font-size: 14px; color: #888;">Thank you for your payment.</p>
                </div>
            </div>
        """

        return format_html(ledger)

    ledger_view.short_description = ""

    def form_data_view(self, obj):
        if not obj or not obj.enrollment or not obj.enrollment.student:
            return "No form data available."
        
        student = obj.enrollment.student
        return format_html(
            """
            <div style="margin-top: 10px;">
                <h4>Student Form Data:</h4>
                <p><strong>First Name:</strong> {}</p>
                <p><strong>Last Name:</strong> {}</p>
                <p><strong>Admission Number:</strong> {}</p>
            </div>
            """,
            student.first_name,
            student.last_name,
            student.admission_number
        )

    form_data_view.short_description = "Form Data"

    def payment_history_view(self, obj):
        if not obj or not obj.enrollment or not obj.enrollment.student:
            return "No payment history available."

        payments = Payment.objects.filter(enrollment__student=obj.enrollment.student).order_by('-date')
        history = """
            <table style="border: 1px solid #ddd; border-collapse: collapse; width: 100%; margin-top: 10px;">
                <thead>
                    <tr style="background-color: #f2f2f2; text-align: left;">
                        <th style="border: 1px solid #ddd; padding: 8px;">Date</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Amount</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Payment Type</th>
                    </tr>
                </thead>
                <tbody>
        """

        for payment in payments:
            history += format_html(
                """
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">{}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{}</td>
                    </tr>
                """,
                payment.date.strftime('%Y-%m-%d'),
                f"{payment.amount:,.2f}",
                payment.payment_type,
            )

        history += """
                </tbody>
            </table>
        """

        return format_html(history)

    payment_history_view.short_description = "Payment History"


from django.utils.html import format_html
from django import forms
from django.contrib import admin
from .models import PaymentType, PaymentTypeBreakdown, Ledger, Payment
from academics.models import Enrollment, Student
from decimal import Decimal
from datetime import datetime
from django.db.models import Sum

@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('name',)

class PaymentTypeBreakdownAdminForm(forms.ModelForm):
    class Meta:
        model = PaymentTypeBreakdown
        fields = ['ledger', 'payment_type', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['ledger'].queryset = Ledger.objects.all()

@admin.register(PaymentTypeBreakdown)
class PaymentTypeBreakdownAdmin(admin.ModelAdmin):
    form = PaymentTypeBreakdownAdminForm
    list_display = ('ledger', 'payment_type', 'amount')
    search_fields = ('ledger__student__first_name', 'ledger__student__last_name', 'payment_type__name')
    list_filter = ('ledger', 'payment_type', 'ledger__academic_year', 'ledger__semester')

    def save_model(self, request, obj, form, change):
        # Ensure the PaymentTypeBreakdown is correctly linked to the Ledger
        if not obj.ledger:
            raise ValueError("Ledger must be associated with this payment breakdown.")

        # Recalculate the required_amount for the Ledger based on all breakdowns
        obj.ledger.required_amount = obj.ledger.payment_type_breakdowns.aggregate(
            total=Sum('amount'))['total'] or Decimal('0.00')
        obj.ledger.save()

        # Save the breakdown record
        super().save_model(request, obj, form, change)

        # Recalculate the balance after saving the breakdown
        self.update_balance(obj.ledger)

    def update_balance(self, ledger):
        # Calculate the total paid from payments
        total_paid = Payment.objects.filter(
            enrollment__student=ledger.student,
            enrollment__academic_year=ledger.academic_year,
            enrollment__semester=ledger.semester
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

        # Update the balance
        balance = ledger.required_amount - total_paid
        ledger.balance = balance
        ledger.save()

    def get_queryset(self, request):
        return super().get_queryset(request)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

from django import forms
from django.contrib import admin
from django.utils.html import format_html
from decimal import Decimal
from django.urls import reverse
from .models import Ledger, Payment, Enrollment, Student
from datetime import datetime
from django.http import HttpResponse


class LedgerAdminForm(forms.ModelForm):
    class Meta:
        model = Ledger
        fields = ['student', 'academic_year', 'semester', 'required_amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        academic_year = self.initial.get('academic_year') or getattr(self.instance, 'academic_year', None)
        semester = self.initial.get('semester') or getattr(self.instance, 'semester', None)

        if academic_year and semester:
            self.fields['student'].queryset = Enrollment.objects.filter(
                academic_year=academic_year,
                semester=semester
            ).values_list('student', flat=True)
            self.fields['student'].queryset = Student.objects.filter(id__in=self.fields['student'].queryset)


@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    form = LedgerAdminForm
    list_display = ('student', 'ledger_number', 'academic_year', 'semester', 'required_amount', 'total_paid_display', 'balance_display', 'generated_on', 'print_button')
    search_fields = ('student__first_name', 'student__last_name', 'ledger_number', 'academic_year__year', 'semester__semester')
    list_filter = ('academic_year', 'semester')
    readonly_fields = ('ledger_details', 'total_paid', 'balance', 'generated_on')

    fieldsets = [
        ('Ledger Details', {
            'classes': ('collapse', 'wide',),
            'fields': ('ledger_details',),
        }),
        ('Ledger Summary', {
            'classes': ('collapse',),
            'fields': ('student', 'academic_year', 'semester', 'total_paid', 'required_amount', 'balance', 'generated_on'),
        }),
    ]

    def total_paid_display(self, obj):
        payments = Payment.objects.filter(
            enrollment__student=obj.student,
            enrollment__academic_year=obj.academic_year,
            enrollment__semester=obj.semester
        )
        total_paid = sum(payment.amount for payment in payments)
        return format_html("{:,.2f}".format(total_paid))

    total_paid_display.short_description = 'Total Paid'

    def balance_display(self, obj):
        total_paid = Decimal(self.total_paid_display(obj).replace(",", ""))
        balance = obj.required_amount - total_paid
        return format_html(
            "<span style='color: {}; font-weight: bold;'>{}</span>".format(
                "green" if balance <= 0 else "red", "{:,.2f}".format(balance)
            )
        )

    balance_display.short_description = 'Balance'

    def ledger_details(self, obj):
        if not obj or not obj.student:
            return "No ledger details available."

        student = obj.student
        full_name = f"{student.first_name} {student.last_name}"
        course = student.course.name if student.course else "No course assigned"
        NSIN = student.NSIN if student.NSIN else "No NSIN assigned"
        image_url = student.passport_photo.url if student.passport_photo else None
        payments = Payment.objects.filter(
            enrollment__student=student,
            enrollment__academic_year=obj.academic_year,
            enrollment__semester=obj.semester
        ).order_by('date')

        total_paid = 0

        # Generate payment breakdown HTML
        payment_breakdowns_html = "<h4>Payment Breakdown</h4><table style='border: none; width:400px; font-size: 12px;'>"
        payment_breakdowns_html += "<thead><tr style='background-color: #f2f2f2;'><th style='border: 1px solid #ddd; padding: 5px;'>Payment Type</th><th style='border: 1px solid #ddd; padding: 5px;'>Amount</th></tr></thead><tbody>"
        payment_types = obj.payment_type_breakdowns.all()

        payment_balances = {}  # Dictionary to store balances for each payment type

        for breakdown in payment_types:
            payment_type_name = breakdown.payment_type.name
            amount = breakdown.amount
            payment_balances[payment_type_name] = payment_balances.get(payment_type_name, 0) + amount
            payment_breakdowns_html += f"<tr><td style='border: 1px solid #ddd; padding: 5px;'>{payment_type_name}</td><td style='border: 1px solid #ddd; padding: 5px; text-align: right;'>{amount:,.2f}</td></tr>"

        payment_breakdowns_html += f"""
            <tr style='background-color: #f9f9f9; font-weight: bold;'>
                <td style='border: 1px solid #ddd; padding: 5px;'>Required Amount</td>
                <td style='border: 1px solid #ddd; padding: 5px; text-align: right;'>{obj.required_amount:,.2f}</td>
            </tr>
        """
        payment_breakdowns_html += "</tbody></table>"

        # Build the rest of the ledger HTML
        ledger_html = f"""
            <div style="text-align: center;">
                <button onclick="window.print();" style="padding: 10px 20px; background-color: #0056b3; color: white; border: none; cursor: pointer; margin-left:auto; margin-right:auto;">
                    Print Ledger
                </button>
            </div>
            <div id="ledger-printable-content" style="font-family: Arial, sans-serif; border: 1px solid #ddd; padding: 20px; width: 1200px;">
                <div style="text-align: center;">
                    <h2 style="color: #0056b3;">Student Ledger</h2>
                    <p style="color: #555; font-size: 14px;">Generated on: {datetime.now().strftime('%Y-%m-%d')}</p>
                </div>
                <div style="display: flex; margin-top: 20px;">
                    <div style="flex: 0 0 auto; margin-right: 20px;">
                        {'<img src="{}" alt="{}" style="max-height: 150px; max-width: 150px; border-radius: 10px;">'.format(image_url, full_name) if image_url else ''}
                    </div>
                    <div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
                        <h4 style="margin: 0; font-size: 18px;">STUDENT DETAILS</h4><hr>
                        <p style="margin: 5px 0; font-size: 14px;"><strong>Name:</strong> {full_name}</p>
                        <p style="margin: 5px 0; font-size: 14px;"><strong>Course:</strong> {course}</p>
                        <p style="margin: 5px 0; font-size: 14px;"><strong>NSIN:</strong> {NSIN}</p>
                    </div>
                    <div style="flex: 0 0 200px; margin-left: 20px;">
                        {payment_breakdowns_html}
                    </div>
                </div>
                <h4 style="margin-top: 20px;">Academic Year: {obj.academic_year.year}, Semester: {obj.semester.semester}</h4>
                <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                    <thead>
                        <tr style="background-color: #f2f2f2;">
                            <th style="border: 1px solid #ddd; padding: 8px;">Date</th>
                            <th style="border: 1px solid #ddd; padding: 8px;">Payment Type</th>
                            <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">Payment Type Amount</th>
                            <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">Amount Paid</th>
                          
                        </tr>
                    </thead>
                    <tbody>
        """

        for payment in payments:
            payment_type_amount = payment_balances.get(payment.payment_type.name, 0)
            balance_per_payment_type = payment_type_amount - payment.amount  # Subtract Amount Paid from Payment Type Amount
           
            ledger_html += format_html(
                """
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">{}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{}</td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">{}</td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">{}</td>
                    
                </tr>
                """,
                payment.date.strftime('%Y-%m-%d'),
                payment.payment_type,
                f"{payment_type_amount:,.2f}",
                f"{payment.amount:,.2f}",
                
                f"{balance_per_payment_type:,.2f}", 
            )
            total_paid += payment.amount

        balance = obj.required_amount - total_paid

        ledger_html += format_html(
            """
                    </tbody>
                    <tfoot>
                        <tr style="background-color: #f9f9f9; font-weight: bold;">
                            <td colspan="3" style="border: 1px solid #ddd; padding: 8px; text-align: right;">Total Paid:</td>
                            <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">{}</td>
                            
                        </tr>
                        <tr style="background-color: #f9f9f9; font-weight: bold;">
                            <td colspan="3" style="border: 1px solid #ddd; padding: 8px; text-align: right;">Balance:</td>
                            <td style="border: 1px solid #ddd; padding: 8px; text-align: right; color: {}">{}</td>
                            
                        </tr>
                    </tfoot>
                </table>
                <div style="text-align: center; margin-top: 20px;">
                    <p style="color: #888;">Thank you for your payment.</p>
                </div>
            </div>
            """,
        f"{total_paid:,.2f}",
        "green" if balance <= 0 else "red",
        f"{balance:,.2f}",
        )

        return format_html(ledger_html)

    # Add print action
    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path('print_ledger/<int:ledger_id>/', self.admin_site.admin_view(self.print_ledger), name='print_ledger'),
        ]
        return custom_urls + urls

    def print_ledger(self, request, ledger_id):
        ledger = Ledger.objects.get(id=ledger_id)
        ledger_html = self.ledger_details(ledger)
        return HttpResponse(ledger_html, content_type="text/html")

    # Add print button in the admin page
    def print_button(self, obj):
        return format_html(
            '<a href="{}" class="button" target="_blank">Print Ledger</a>',
            reverse('admin:print_ledger', args=[obj.id])
        )

    print_button.short_description = 'Print'

class Media:
    js = ('admin/js/vendor/jquery/jquery.js', 'admin/js/actions.js', 'js/print_ledger.js')
