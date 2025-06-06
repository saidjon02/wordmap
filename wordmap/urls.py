from django.contrib import admin
from django.urls import path
from django.urls import include
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK", status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
    path('', include('core.urls')),  # Include the core app's URLs
]
