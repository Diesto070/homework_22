from typing import Any

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда для создания суперпользователя.
    Создает администратора с предустановленными правами:"""
    def handle(self, *args: Any, **options: Any) -> None:
        """Создает пользователя с административными привилегиями
        для доступа к панели администратора Django."""
        user = User.objects.create(email="admin@admin.com")
        user.set_password("123qwe")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
