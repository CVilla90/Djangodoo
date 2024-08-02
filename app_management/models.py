from django.db import models

class App(models.Model):
    CATEGORY_CHOICES = [
        ('Sales', 'Sales'),
        ('Services', 'Services'),
        ('Accounting', 'Accounting'),
        ('Inventory', 'Inventory'),
        ('Manufacturing', 'Manufacturing'),
        ('Human Resources', 'Human Resources'),
        # Add other categories as needed
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='app_icons/')
    official = models.BooleanField(default=False)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    active = models.BooleanField(default=False)
    url = models.CharField(max_length=100, default='#')

    def __str__(self):
        return self.name
