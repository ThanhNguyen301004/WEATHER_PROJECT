from django.urls import path
from . import views
from .views import register

urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home_page, name='home'),  # Đường dẫn tới trang home
]

