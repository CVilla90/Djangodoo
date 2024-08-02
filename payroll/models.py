# Portfolio\Djangodoo\payroll\models.py

from django.db import models
from employees.models import Employee

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    income_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    social_security = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_description = models.TextField(blank=True)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_deductions(self):
        return self.income_tax + self.social_security + self.other_deductions

    def save(self, *args, **kwargs):
        self.net_salary = self.gross_salary - self.total_deductions
        super().save(*args, **kwargs)

class Payslip(models.Model):
    payroll = models.OneToOneField(Payroll, on_delete=models.CASCADE)
    details = models.TextField()
    date_issued = models.DateField(auto_now_add=True)
