from django.db import models
from django.db.models import CharField


class Blog(models.Model):
    heading = models.CharField(
        max_length=100,
        verbose_name="Заголовок",
    )
    content = models.TextField(
        blank=True,
        null=True,
        verbose_name="Содержимое блога",
        help_text="Введите текст записи",
    )
    picture = models.ImageField(
        upload_to="blog/photo/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,  # автоматически при создании
        verbose_name='Дата и время создания',
    )
    is_publication = models.BooleanField(
        default=False,    # признак публикации
        verbose_name="Опубликовано",
    )
    views_count = models.PositiveIntegerField(
        verbose_name="Количество просмотров",
        help_text="Автоматически увеличивается при просмотре",
        default=0
    )

    class Meta:
        """Метаданные модели блога"""
        verbose_name = "Запись блога"
        verbose_name_plural = "Записи блога"
        ordering = ['id']

    def __str__(self) -> CharField:
        """Возвращает заголовок блога."""
        return self.heading
