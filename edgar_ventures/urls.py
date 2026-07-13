from django.contrib import admin
from django.urls import path, include
from core.views import handler404, handler500

handler404 = handler404
handler500 = handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
