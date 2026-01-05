from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from blog.models import Blog


class BlogListView(LoginRequiredMixin, ListView):
    """Отображает главную страницу блога только с теми статьями,
    которые помечены как опубликованные."""

    model = Blog
    template_name = "blog/blog_list.html"
    ordering = ["id"]

    def get_queryset(self) -> QuerySet[Blog]:
        """Возвращает отфильтрованный queryset только с опубликованными статьями."""
        return Blog.objects.filter(is_publication=True)


class BlogDetailView(LoginRequiredMixin, DetailView):
    """Представление для детального просмотра статьи блога.
    Автоматически увеличивает счетчик просмотров при каждом обращении
    к странице статьи."""

    model = Blog
    template_name = "blog/blog_detail.html"

    def get_object(self, queryset: Optional[QuerySet[Blog]] = None) -> Blog:
        """Получает объект статьи и увеличивает счетчик просмотров."""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(LoginRequiredMixin, CreateView):
    """Предоставляет форму для создания статьи с указанными полями
    и перенаправляет на список статей после успешного создания."""

    model = Blog
    fields = ["heading", "content", "picture", "is_publication"]
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:blog_list")

    def form_valid(self, form: Any) -> HttpResponse:
        """Обрабатывает валидную форму создания статьи."""
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    """Предоставляет форму для редактирования статьи и перенаправляет
    на детальную страницу этой статьи после успешного обновления.
    """

    model = Blog
    fields = ["heading", "content", "picture"]
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:blog_list")

    def get_success_url(self) -> Any:
        """Возвращает URL для перенаправления после успешного обновления.
        Перенаправляет на страницу самой статьи, а не на список."""
        return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """Предоставляет подтверждение удаления и перенаправляет
    на список статей после успешного удаления."""

    model = Blog
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:blog_list")
