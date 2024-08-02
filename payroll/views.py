# payroll/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Payroll, Payslip
from .forms import PayrollForm
from employees.models import Employee

def payroll_list(request):
    payrolls = Payroll.objects.all()
    return render(request, 'payroll/payroll_list.html', {'payrolls': payrolls})

def payroll_create(request):
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            payroll = form.save(commit=False)
            payroll.net_salary = (
                payroll.gross_salary - payroll.income_tax - 
                payroll.social_security - payroll.other_deductions
            )
            payroll.save()
            Payslip.objects.create(
                payroll=payroll, 
                details=f"Payslip for {payroll.employee.first_name} {payroll.employee.last_name}"
            )
            return redirect('payroll_list')
    else:
        form = PayrollForm()
    return render(request, 'payroll/payroll_form.html', {'form': form})

def payroll_delete(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    if request.method == 'POST':
        payroll.delete()
        return redirect('payroll_list')
    return render(request, 'payroll/payroll_confirm_delete.html', {'payroll': payroll})

def payslip_detail(request, pk):
    payslip = get_object_or_404(Payslip, payroll__pk=pk)
    deductions = payslip.payroll.gross_salary - payslip.payroll.net_salary
    return render(request, 'payroll/payslip_detail.html', {
        'payslip': payslip,
        'deductions': deductions,
    })

def get_employee_salary(request):
    employee_id = request.GET.get('employee_id')
    try:
        employee = Employee.objects.get(pk=employee_id)
        data = {
            'salary': str(employee.salary)
        }
    except Employee.DoesNotExist:
        data = {
            'salary': ''
        }
    return JsonResponse(data)

def download_payslip(request, pk):
    payslip = get_object_or_404(Payslip, payroll_id=pk)
    
    html_string = render_to_string('payroll/payslip_pdf.html', {'payslip': payslip, 'deductions': payslip.payroll.income_tax + payslip.payroll.social_security + payslip.payroll.other_deductions})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{payslip.payroll.employee.first_name}_{payslip.payroll.date}.pdf"'
    
    HTML(string=html_string).write_pdf(response)
    
    return response
