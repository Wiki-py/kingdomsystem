"""
URL configuration for surveysystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from surveys.views import RoleBasedLoginView
from surveys.admin import super_admin_site

urlpatterns = [
    path('', include('surveys.urls')),  # Welcome screen is now the home page
    path('admin/', super_admin_site.urls),  # Only superusers can access Django admin
    path('admin-dashboard/', include('surveys.admin_urls')),
    path('accounts/login/', RoleBasedLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='surveys:welcome', template_name='registration/logged_out.html'), name='logout'),
]

# Custom error handlers for production
handler404 = 'surveys.views.custom_404'
handler500 = 'surveys.views.custom_404'  # Use same handler for 500 errors
