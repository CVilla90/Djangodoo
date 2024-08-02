# Portfolio\Djangodoo\payroll\forms.py

from django import forms
from .models import Payroll, Payslip
from employees.models import Employee
from datetime import date  # Import date class from datetime module

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = [
            'employee', 'date', 'gross_salary', 
            'income_tax', 'social_security', 
            'other_deductions', 'other_description'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today()  # Set the current server date
        if self.instance and self.instance.pk:
            self.fields['gross_salary'].initial = self.instance.employee.salary
        elif self.data.get('employee'):
            try:
                employee_id = int(self.data.get('employee'))
                employee = Employee.objects.get(pk=employee_id)
                self.fields['gross_salary'].initial = employee.salary
            except (ValueError, TypeError, Employee.DoesNotExist):
                pass

class PayslipForm(forms.ModelForm):
    class Meta:
        model = Payslip
        fields = ['payroll', 'details']
