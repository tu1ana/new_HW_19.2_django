from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    photo = models.ImageField(upload_to='products/', **NULLABLE, verbose_name='Изображение(превью)')
    category = models.ForeignKey(Category, to_field='name', on_delete=models.CASCADE, verbose_name='Категория')
    price = models.FloatField(verbose_name='Цена')
    date_created = models.DateField(verbose_name='Дата создания')
    date_last_modified = models.DateField(verbose_name='Дата последнего изменения')

    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Авторизованный пользователь')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

        permissions = [
            ('set_published', 'Can publish products'),
            ('change_description', 'Can change description'),
            ('change_category', 'Can change category')
        ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    number = models.IntegerField(verbose_name='Номер версии')
    name = models.CharField(max_length=150, verbose_name='Название версии')
    is_active = models.BooleanField(default=True, verbose_name='Текущая версия')

    def __str__(self):
        return f'{self.product} версия {self.number} {self.name}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'


class BlogEntry(models.Model):
    heading = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)
    content = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog/', ** NULLABLE, verbose_name='Изображение(превью)')
    date_created = models.DateField(** NULLABLE, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.heading

    class Meta:
        verbose_name = 'запись блога'
        verbose_name_plural = 'записи блога'
