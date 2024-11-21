from django.contrib import admin
from django.urls import path, include
from apps.users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),
    path('users/', include('apps.users.urls')),
    path('core/', include('apps.core.urls')),
]

# Sirve archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
