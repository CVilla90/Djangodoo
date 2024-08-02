# Djangodoo/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Djangodoo import views as djangodoo_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('employees/', include('employees.urls')),
    path('payroll/', include('payroll.urls')),
    path('', djangodoo_views.home, name='home'),
    path('logout/', djangodoo_views.logout_view, name='logout'),
    path('filtered_apps/<str:filter_type>/', djangodoo_views.filtered_apps, name='filtered_apps'),
    path('filtered_apps_by_category/<str:category>/', djangodoo_views.filtered_apps_by_category, name='filtered_apps_by_category'),
    path('toggle_app_status/<int:app_id>/', djangodoo_views.toggle_app_status, name='toggle_app_status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
