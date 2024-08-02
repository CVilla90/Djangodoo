# Portfolio\Djangodoo\Djangodoo\views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from app_management.models import App
from django.db.models import Q


@login_required
def home(request):
    query = request.GET.get('q')
    if query:
        apps = App.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)).order_by('name')
    else:
        apps = App.objects.all().order_by('name')
    categories = App.CATEGORY_CHOICES
    categories = sorted([category[0] for category in categories])  # Alphabetically sorted categories
    return render(request, 'home.html', {'apps': apps, 'categories': categories})


@login_required
def filtered_apps(request, filter_type):
    if filter_type == 'official':
        apps = App.objects.filter(official=True).order_by('name')
    else:
        apps = App.objects.filter(official=False).order_by('name')
    categories = App.CATEGORY_CHOICES
    categories = sorted([category[0] for category in categories])
    return render(request, 'home.html', {'apps': apps, 'categories': categories})


@login_required
def filtered_apps_by_category(request, category):
    if category == 'All':
        apps = App.objects.all().order_by('name')
    else:
        apps = App.objects.filter(category=category).order_by('name')
    categories = App.CATEGORY_CHOICES
    categories = sorted([category[0] for category in categories])
    return render(request, 'home.html', {'apps': apps, 'categories': categories})


@login_required
def toggle_app_status(request, app_id):
    app = App.objects.get(id=app_id)
    app.active = not app.active
    app.save()
    return redirect('home')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
