from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', lambda request: redirect('login'), name='redirect_to_login'),  # Chuyển hướng đến trang đăng nhập
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.index, name='index'), 
    path('logout/', views.user_logout, name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/<int:id>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:id>/delete/', views.user_delete, name='user_delete'),  
    path('home/khihau', views.khihau, name='khihau' ),
    path('home/khihau/<int:id>/chitiet', views.chitietkhihau, name='chitietkhihau'),
    path('home/khihau/<int:id>/chitiet/display_dpf', views.display_pdf,  name='display_pdf'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/add/', views.add_document, name='add_document'),
    path('documents/<int:id>/update/', views.update_document, name='update_document'),
    path('documents/<int:id>/delete/', views.delete_document, name='delete_document'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

