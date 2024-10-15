"""
URL configuration for weather_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from weather_app import views
from django.shortcuts import redirect
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('', lambda request: redirect('login'), name='redirect_to_login'),  # Chuyển hướng đến trang đăng nhập
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.index, name='index'),  # Thêm dòng này
    path('logout/', views.user_logout, name='logout'),
]

