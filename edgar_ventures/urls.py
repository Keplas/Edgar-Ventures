from core.views import handler404, handler500, sitemap_xml, robots_txt

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap_xml),
    path('robots.txt', robots_txt),
    path('', include('core.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = handler404
handler500 = handler500
