# Generated by Django 4.0.3 on 2024-08-02 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0004_alter_payslip_payroll'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payroll',
            name='deductions',
        ),
        migrations.AddField(
            model_name='payroll',
            name='income_tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='payroll',
            name='other_deductions',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='payroll',
            name='other_description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='payroll',
            name='social_security',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
