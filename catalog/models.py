from django.db import models
from django.db.models import CharField

from users.models import User


class Category(models.Model):
    """Модель категории товаров."""

    name = models.CharField(
        max_length=100,
        verbose_name="Название категории",
        help_text="Введите название категории",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание категории",
        help_text="Введите описание категории",
    )

    class Meta:
        """Метаданные модели категории."""

        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> CharField:
        """Строковое представление категории."""
        return self.name


class Product(models.Model):
    """Модель продукта/товара."""

    name = models.CharField(
        max_length=100,
        verbose_name="Название продукта",
        help_text="Введите название продукта",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание продукта",
        help_text="Введите описание продукта",
    )
    picture = models.ImageField(
        upload_to="catalog/photo/",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категории",
        help_text="Выберите категорию",
        related_name="products",
    )  # категория
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        # validators=[MinValueValidator(0)],  # Цена не может быть отрицательной
        verbose_name="Цена продукта",
        help_text="Стоимость продукта",
    )  # цена за покупку
    created_at = models.DateTimeField(
        auto_now_add=True,  # автоматически при создании
        verbose_name="Дата и время создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,  # автоматически обновляется при каждом сохранении
        verbose_name="Дата последнего изменения",
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовать продукт",
        help_text="Отметьте, чтобы опубликовать продукт",
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Владелец продукта",
        blank=True, null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        """Метаданные модели продукта."""

        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category", "name"]
        permissions = [
            ("can_unpublish_product", "Can unpublish product")    # может отменять публикацию продукта
        ]

    def __str__(self) -> str:
        """Строковое представление продукта."""
        return f"{self.name} ({self.category})"