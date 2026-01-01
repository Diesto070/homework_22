from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "heading", "content", "picture", "created_at", "views_count")
    list_filter = ("created_at",)      # Фильтрация по created_at
    search_fields = ("content", "created_at")     # Поиск по content и created_at
