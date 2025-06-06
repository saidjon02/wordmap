# core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views
from .views import WordPairViewSet
from .views_login import CustomLoginView 
from django.shortcuts import render

router = DefaultRouter()
router.register('posts', WordPairViewSet, basename='post')

urlpatterns = [
    # 1) Asosiy sahifa
    path('', views.home, name='home'),

    # 2) So‘z qo‘shish
    path('add/', views.add_word, name='add_word'),

    # 3) Login (faqat CustomLoginView qoldirildi)
    path(
        'login/', 
        CustomLoginView.as_view(template_name='core/login.html'), 
        name='login'
    ),

    # 4) Logout (Django built-in LogoutView ishlatildi; next_page='login')
    path(
        'logout/', 
        auth_views.LogoutView.as_view(next_page='login'), 
        name='logout'
    ),

    # 5) Ro‘yxatdan o‘tish (signup)
    path('signup/', views.signup, name='signup'),

    # 6) Qidiruv takliflari (AJAX JSON)
    path('search_suggestions/', views.search_suggestions, name='search_suggestions'),

    # 7) So‘z natijasini olish (AJAX JSON)
    path('get_word_output/', views.get_word_output, name='get_word_output'),

    # 8) So‘z o‘chirish
    path('delete_word/<int:word_id>/', views.delete_word, name='delete_word'),

    # 9) So‘z tahrirlash
    path('word/edit/<int:word_id>/', views.edit_word, name='edit_word'),

    # 10) Parol o‘zgartirish
    path('settings/password/', views.change_password_view, name='change_password'),

    # 11) Products sahifasi (agar siz uni Product o‘rniga ishlatayotgan bo‘lsangiz, nomi change_products bo‘lgani ma’qul)
    path('settings/products/', views.change_products_view, name='change_products'),

    # 12) DRF API endpoint'lari
    path('api/', include(router.urls)),

    # 13) Likes Words sahifasi (statik)
    path(
        'likes_words/', 
        lambda request: render(request, 'core/likes_words.html'), 
        name='likes_words'
    ),

    # 14) Search History sahifasi (statik)
    path(
        'search_history/', 
        lambda request: render(request, 'core/search_history.html'), 
        name='search_history'
    ),
]
