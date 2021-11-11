from django.conf import settings
from django.contrib import admin
from django.urls import path ,include
from django.conf.urls.static import static


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('attendance/',include('attendance.urls'))

]

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

