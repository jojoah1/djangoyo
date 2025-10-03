from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from .models import Image
import os


class ImageViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        # Создаем тестовое изображение
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake_image_content',
            content_type='image/jpeg'
        )

        # Создаем тестовый объект Image
        self.image = Image.objects.create(
            name='test_image',
            image=self.test_image
        )

    def tearDown(self):

        # Удаляем файлы изображений """Очистка после тестов"""
        if self.image.image:
            if os.path.isfile(self.image.image.path):
                os.remove(self.image.image.path)

    def test_gallery_view_get(self):
        # """Тест GET запроса к gallery_view"""
        response = self.client.get(reverse('gallery'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery.html')
        self.assertIn('images', response.context)
        self.assertEqual(list(response.context['images']), [self.image])

    def test_gallery_view_with_multiple_images(self):

        # Создаем второе изображение  """Тест gallery_view с несколькими изображениями"""
        image2 = Image.objects.create(
            name='test_image2',
            image=self.test_image
        )

        response = self.client.get(reverse('gallery'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['images']), 2)
        # Проверяем порядок (по убыванию даты)
        self.assertEqual(response.context['images'][0], image2)

        # Очистка
        if os.path.isfile(image2.image.path):
            os.remove(image2.image.path)

    def test_delete_image_post(self):
        """Тест удаления изображения через POST"""
        response = self.client.post(reverse('delete_image', args=[self.image.id]))

        # Проверяем редирект
        self.assertRedirects(response, reverse('gallery'))

        # Проверяем, что изображение удалено
        self.assertFalse(Image.objects.filter(id=self.image.id).exists())

        # Проверяем сообщение об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Изображение "test_image" успешно удалено')

    def test_delete_image_nonexistent(self):
        """Тест удаления несуществующего изображения"""
        response = self.client.post(reverse('delete_image', args=[999]))

        self.assertRedirects(response, reverse('gallery'))

        # Проверяем сообщение об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Изображение не найдено')

    def test_delete_image_get_request(self):
        """Тест, что GET запрос не удаляет изображение"""
        initial_count = Image.objects.count()

        response = self.client.get(reverse('delete_image', args=[self.image.id]))

        # Должен быть редирект без удаления
        self.assertRedirects(response, reverse('gallery'))
        self.assertEqual(Image.objects.count(), initial_count)

    def test_upload_image_get(self):
        """Тест GET запроса к upload_image"""
        response = self.client.get(reverse('upload_image'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload.html')
        self.assertIn('images', response.context)
        # Проверяем, что возвращаются последние 6 изображений
        self.assertEqual(len(response.context['images']), 1)

    def test_upload_image_post_success(self):
        """Тест успешной загрузки изображения"""
        # Создаем тестовый файл для загрузки
        new_image = SimpleUploadedFile(
            name='new_test_image.jpg',
            content=b'new_fake_image_content',
            content_type='image/jpeg'
        )

        response = self.client.post(
            reverse('upload_image'),
            {'image': new_image}
        )

        # Проверяем редирект
        self.assertRedirects(response, reverse('gallery'))

        # Проверяем, что изображение создано
        self.assertTrue(Image.objects.filter(name='new_test_image.jpg').exists())

        # Проверяем сообщение об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Изображение "new_test_image.jpg" успешно загружено!', str(messages[0]))

        # Очистка
        new_img = Image.objects.get(name='new_test_image.jpg')
        if os.path.isfile(new_img.image.path):
            os.remove(new_img.image.path)

    def test_upload_image_post_no_file(self):
        # """Тест загрузки без файла"""
        response = self.client.post(reverse('upload_image'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload.html')

        # Проверяем сообщение об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Файл не выбран')

    def test_upload_image_context_with_many_images(self):
        # Создаем несколько изображений для теста
        for i in range(10):
            img = Image.objects.create(
                name=f'test_image_{i}',
                image=self.test_image
            )

        response = self.client.get(reverse('upload_image'))

        # Проверяем, что возвращаются только последние 6 изображений
        self.assertEqual(len(response.context['images']), 6)

        # Очистка дополнительных изображений
        for img in Image.objects.filter(name__startswith='test_image_'):
            if os.path.isfile(img.image.path):
                os.remove(img.image.path)
            img.delete()


class ImageModelTestCase(TestCase):
    """Тесты для модели Image"""

    def setUp(self):
        self.test_image = SimpleUploadedFile(
            name='model_test.jpg',
            content=b'model_test_content',
            content_type='image/jpeg'
        )

    def tearDown(self):
        # Очистка созданных файлов
        for image in Image.objects.all():
            if hasattr(image, 'image') and image.image:
                if os.path.isfile(image.image.path):
                    os.remove(image.image.path)
