from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', TemplateView.as_view(template_name='build/index.html')),
    path('', include('loader.urls')),
    path('api/comics/', include('Comics.urls.comics_urls')),
    path('api/chapters/', include('Comics.urls.chapters_urls')),
    path('api/users/', include('users.urls.user_urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="password_reset.html"), name="password_reset"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="reset.html"), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="reset_complete.html"), name="password_reset_complete"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
