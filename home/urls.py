from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('loader.urls', namespace='loader')),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('account/', include('django.contrib.auth.urls')),
    path('api/comics/', include('Comics.urls.comics_urls')),
    path('api/chapters/', include('Comics.urls.chapters_urls')),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
