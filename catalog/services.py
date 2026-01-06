from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from catalog.models import Category, Product


class ProductService:
    """Сервис для работы с продуктами"""

    @staticmethod
    def get_list_products_by_category(category_id: int) -> QuerySet[Product]:
        """Возвращает список всех продуктов в указанной категории"""
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category, is_published=True)
        return products
