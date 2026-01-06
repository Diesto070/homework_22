from typing import Any

from .models import Category


class CategoryMixin:
    """Миксин для добавления списка всех категорий в контекст шаблонов.

    Обеспечивает доступ к категориям продуктов во всех представлениях,
    где используется данный миксин. Категории передаются в шаблон
    через переменную контекста 'categories'."""
    def get_context_data(self, **kwargs: Any) -> dict[Any, Any]:
        """Добавляет список всех категорий в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
