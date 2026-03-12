#####################
# URL CONFIGURATION
#####################
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # DJANGO BUILT-IN ADMIN (MUST BE FIRST)
    path('django-admin/', admin.site.urls),

    # YOUR CUSTOM ADMIN
    path('admin/', include('adminview.routes')),

    # CORE APP
    path('', include('core.routes')),
]

#####################
# STATIC AND MEDIA SERVING
#####################
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)