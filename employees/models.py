# Portfolio\Djangodoo\employees\models.py

from django.db import models
from users.models import CustomUser

class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    bank_details = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else f"Employee {self.id}"
