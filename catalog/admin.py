from django.contrib import admin

from catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "purchase_price", "category")
    list_filter = ("category",)                 # Фильтрация по категории
    search_fields = ("name", "description")     # Поиск по name и description
