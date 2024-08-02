from django.contrib import admin
from .models import App

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'official', 'category', 'active', 'url')
    search_fields = ('name', 'description')
    list_filter = ('official', 'category')