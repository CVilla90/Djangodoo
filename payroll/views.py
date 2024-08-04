# payroll/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import Payroll, Payslip
from .forms import PayrollForm
from employees.models import Employee
from fpdf import FPDF

def payroll_list(request):
    payrolls = Payroll.objects.all()
    for payroll in payrolls:
        payroll.deductions = payroll.gross_salary - payroll.net_salary  # Calculate deductions
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

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Payslip', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'C')

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_table(self, data):
        self.set_fill_color(200, 220, 255)
        self.set_font('Arial', 'B', 12)
        col_width = self.w / 2.5
        row_height = self.font_size * 1.5

        self.cell(col_width, row_height, "Description", border=1, fill=True, align='C')
        self.cell(col_width, row_height, "Amount", border=1, fill=True, align='C')
        self.ln(row_height)

        self.set_font('Arial', '', 12)

        for row in data:
            for item in row:
                self.cell(col_width, row_height, str(item), border=1)
            self.ln(row_height)

def generate_payslip_pdf(payslip):
    pdf = PDF()
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Payslip', 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Date: {payslip.payroll.date}', 0, 1, 'C')
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Employee: {payslip.payroll.employee.first_name} {payslip.payroll.employee.last_name}', 0, 1)
    
    pdf.ln(10)
    
    data = [
        ['Gross Salary', f'{payslip.payroll.gross_salary:.2f}'],
        ['Income Tax', f'{payslip.payroll.income_tax:.2f}'],
        ['Social Security', f'{payslip.payroll.social_security:.2f}'],
        ['Other Deductions', f'{payslip.payroll.other_deductions:.2f}'],
        ['Total Deductions', f'{payslip.payroll.gross_salary - payslip.payroll.net_salary:.2f}'],
        ['Net Salary', f'{payslip.payroll.net_salary:.2f}']
    ]

    pdf.add_table(data)
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Details: {payslip.details}', 0, 1)
    
    return pdf.output(dest='S').encode('latin1')

def download_payslip(request, pk):
    payslip = get_object_or_404(Payslip, payroll_id=pk)
    pdf = generate_payslip_pdf(payslip)
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f"payslip_{payslip.payroll.employee.first_name}_{payslip.payroll.date}.pdf"
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
