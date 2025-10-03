from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Image



def gallery_view(request):
    """Простая страница галереи всех изображений"""
    images = Image.objects.all().order_by('-date')
    return render(request, 'gallery.html', {'images': images})


def delete_image(request, image_id):
    """Удаление изображения с сообщением"""
    if request.method == 'POST':
        try:
            image = Image.objects.get(id=image_id)
            image_name = image.name
            image.delete()
            messages.success(request, f'Изображение "{image_name}" успешно удалено')
        except Image.DoesNotExist:
            messages.error(request, 'Изображение не найдено')

    return redirect('gallery')


def upload_image(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image_file = request.FILES['image']

            try:
                # Создаем и сохраняем изображение
                image = Image(
                    name=image_file.name,
                    image=image_file
                )
                image.save()

                messages.success(request, f'Изображение "{image.name}" успешно загружено!')
                return redirect('gallery')

            except Exception as e:
                messages.error(request, f'Ошибка загрузки: {str(e)}')
        else:
            messages.error(request, 'Файл не выбран')

    # GET запрос - показать форму и последние изображения
    images = Image.objects.all().order_by('-date')[:6]  # Последние 6 изображений
    return render(request, 'upload.html', {'images': images})

