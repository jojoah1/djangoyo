# models.py
from django.db import models
import os
import uuid


def image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('images', unique_filename)


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=image_upload_path)
    size = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    # Явно определяем менеджер объектов
    objects = models.Manager()

    def save(self, *args, **kwargs):
        if self.image:
            self.size = self.image.size
        if not self.name and self.image:
            self.name = self.image.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name