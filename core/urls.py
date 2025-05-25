from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views
from .views import WordPairViewSet
from .views_login import CustomLoginView 
router = DefaultRouter()
router.register('posts', WordPairViewSet, basename='post')

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_word, name='add_word'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', CustomLoginView.as_view(template_name='core/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('search_suggestions/', views.search_suggestions, name='search_suggestions'),
    path('get_word_output/', views.get_word_output, name='get_word_output'),
    path('delete_word/<int:word_id>/', views.delete_word, name='delete_word'),
    path('word/edit/<int:word_id>/', views.edit_word, name='edit_word'),
    path('settings/password/', views.change_password_view, name='change_password'),
    path('settings/products/', views.change_products_view, name='change_products'),
    path('api/', include(router.urls)),
]