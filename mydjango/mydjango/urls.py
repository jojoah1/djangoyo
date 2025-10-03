from django.contrib import admin
from django.urls import path
from myapp1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', views.upload_image, name='upload_image'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),
    path('', views.upload_image, name='home'),
]

# Добавляем обработку медиа файлов в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)