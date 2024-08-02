# payroll/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import Payroll, Payslip
from .forms import PayrollForm
from employees.models import Employee
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO

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

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def download_payslip(request, pk):
    payslip = get_object_or_404(Payslip, payroll_id=pk)
    deductions = payslip.payroll.gross_salary - payslip.payroll.net_salary
    context = {
        'payslip': payslip,
        'deductions': deductions,
    }
    pdf = render_to_pdf('payroll/payslip_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"payslip_{payslip.payroll.employee.first_name}_{payslip.payroll.date}.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
