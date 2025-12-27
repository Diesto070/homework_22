from typing import Any

from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    """Команда управления для загрузки тестовых данных продуктов
    в базу данных."""

    help = 'Add test students to the database'

    def handle(self, *args: Any, **kwargs: Any) -> None:
        """ Основной метод выполнения команды.
        Действия:
        - Удаляет все существующие продукты
        - Загружает данные из фикстуры products.json
        - Выводит сообщение о результате выполнения
        """
        # Удаляем существующие записи продуктов
        Product.objects.all().delete()

        call_command('loaddata', 'products.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
