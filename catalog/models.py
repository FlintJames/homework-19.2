from django.db import models
from django.utils import connection

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование категории")
    description = models.TextField(**NULLABLE, verbose_name="Описание категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE "{cls._meta.db_table}" RESTART IDENTITY CASCADE;')

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    picture = models.ImageField(
        upload_to="catalog/", **NULLABLE, verbose_name="Фотография"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )
    purchase_price = models.IntegerField(max_length=150, verbose_name="Цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    maker = models.ForeignKey(User, **NULLABLE, verbose_name="Производитель", on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.CharField(max_length=250, verbose_name="url")
    content = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(
        upload_to="catalog/", **NULLABLE, verbose_name="Изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    publication_sign = models.BooleanField(default=True, verbose_name="Публикация")
    number_of_views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    views_counter = models.PositiveIntegerField(verbose_name="Счётчик просмотров", default=0)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class Version(models.Model):
    product = models.ForeignKey(Product, verbose_name="Продукт",
                                on_delete=models.SET_NULL, **NULLABLE, )
    number_of_version = models.PositiveIntegerField(verbose_name="Номер версии продукта")
    name_of_versions = models.CharField(max_length=150, verbose_name="Название версии")
    is_active_version = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.is_active_version}'

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
