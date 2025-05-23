from django.contrib import admin
from django.urls import path
from django.urls import include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Include the core app's URLs
]
