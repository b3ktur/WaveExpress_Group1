"""
URL configuration for WaveExpress_Ao project.
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.landing_page, name='landing'),
    path('home/', account_views.home_view, name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('ferry/', include('ferry_system.urls', namespace='ferry_system')),
]
