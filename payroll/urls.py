# Portfolio\Djangodoo\payroll\urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.payroll_list, name='payroll_list'),
    path('create/', views.payroll_create, name='payroll_create'),
    path('delete/<int:pk>/', views.payroll_delete, name='payroll_delete'),
    path('payslip/<int:pk>/', views.payslip_detail, name='payslip_detail'),
    path('get_employee_salary/', views.get_employee_salary, name='get_employee_salary'),
    path('payslip/<int:pk>/download/', views.download_payslip, name='download_payslip'),
]
