# myproject/urls.py  (masalan, WordMap loyihasi)

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Health-check view
def health_check(request):
    return HttpResponse("OK", status=200)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Health-check endpoint
    path('health/', health_check),

    # Barcha core app yo‘llarini shu yerda qo‘shamiz
    path('', include('core.urls')),
]
