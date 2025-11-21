from django.urls import path
from .views import ImageUploadView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)