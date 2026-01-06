from typing import Any

from django import forms
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, TemplateView, UpdateView

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.forms_contact import ContactForm
from catalog.models import Product


class HomeView(TemplateView):
    """Отображает главную страницу"""

    template_name = "catalog/home.html"


class ContactsView(FormView):
    """Отображает страницу контактов и форму обратной связи"""

    template_name = "catalog/contacts.html"
    form_class = ContactForm

    def form_valid(self, form: forms.Form) -> HttpResponse:
        """Обрабатывает валидную форму и возвращает HTTP-ответ с результатом.
        Эта функция вызывается когда данные формы прошли валидацию."""
        name = form.cleaned_data["name"]
        message = form.cleaned_data["message"]
        response_content = f"Спасибо, {name}! Сообщение получено.<br>" f"Ваше сообщение: '{message}'"
        return HttpResponse(response_content)


class ProductListView(ListView):
    """Отображает главную страницу с данными по всем продуктам"""

    model = Product

    def get_queryset(self) -> Any:
        """Возвращает queryset в зависимости от прав пользователя.
        Выводим последние созданные 5 продуктов в консоль"""
        products = Product.objects.order_by("-created_at")[:5]

        print("=== ПОСЛЕДНИЕ 5 ПРОДУКТОВ ===")
        for product in products:
            print(f"{product.id} - {product.name} ({product.created_at.strftime('%d.%m.%Y %H:%M')})")

        user = self.request.user
        # Модераторы видят все продукты
        if user.has_perm('catalog.can_unpublish_product'):
            return Product.objects.all()

        # Авторизованный пользователь видит все продукты
        if user.is_authenticated:
            return Product.objects.all()

        # Неавторизованный - только опубликованные
        return Product.objects.filter(is_published=True)


class ProductsListView(ListView):
    """Отображает все продукты в виде списка из базы данных
    в порядке убывания даты создания"""

    model = Product
    template_name = "catalog/products_list.html"
    context_object_name = "products"
    ordering = ["-created_at"]


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Отображение детальной информации о продукте."""

    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания нового продукта."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form: Any) -> HttpResponse:
        """Обрабатывает валидную форму создания продукта.
        Автоматически устанавливаем текущего пользователя как владельца"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования существующего продукта."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def get_object(self, queryset: QuerySet | None = None) -> Product:
        """Получает объект продукта и проверяет права доступа для редактирования."""
        # Получаем продукт
        product: Product = super().get_object(queryset)
        user = self.request.user
        # Проверяем, является ли текущий пользователь владельцем продукта
        if product.owner != user:
            # Если нет, возвращаем ошибку 403 Forbidden
            raise PermissionDenied("Нет прав для редактирования")
        return product

    def get_form_class(self) -> type[forms.ModelForm]:
        """Определяет класс формы в зависимости от прав пользователя."""
        user = self.request.user
        # Владелец получает полную форму
        if user == self.object.owner:
            return ProductForm
        # Модератор получает ограниченную форму
        if user.has_perm('catalog.can_unpublish_product'):
            return ProductModeratorForm
        # Другие пользователи не могут редактировать продукт
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления продукта."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")
    # permission_required = 'catalog.delete_product'

    def get_object(self, queryset: QuerySet | None = None) -> Product:
        """Получает объект продукта и проверяет права доступа для удаления."""
        # Получаем продукт
        product: Product = super().get_object(queryset)
        user = self.request.user
        # Проверяем, является ли текущий пользователь владельцем продукта или модератором
        if product.owner != user and not user.has_perm('catalog.delete_product'):
            # Если нет, возвращаем ошибку 403 Forbidden
            raise PermissionDenied("Нет прав для удаления")
        return product


@permission_required('catalog.can_unpublish_product')
def unpublish_product(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """Отменяет публикацию продукта.
    Доступно только пользователям с правом 'catalog.can_unpublish_product'."""
    product = get_object_or_404(Product, pk=pk)

    if product.is_published:
        product.is_published = False
        product.save()
    return redirect('catalog:product_list')

# def unpublish_product(request, pk):
#     """Отменяет публикацию продукта"""
#     # Проверка аутентификации
#     if not request.user.is_authenticated:
#         return redirect('login')    # Перенаправляем на страницу логина
#
#     # Получаем продукт или выбрасываем 404, если он не найден
#     product = get_object_or_404(Product, pk=pk)
#
#     # Проверяем, есть ли у пользователя право на отмену публикации
#     if not request.user.has_perm('catalog.can_unpublish_product'):
#         product.is_published = False
#         product.save()
#         return redirect('catalog:product_list')
#     else:
#         # Возвращаем ошибку, если у пользователя нет прав
#         return HttpResponseForbidden("У вас недостаточно прав для отмены публикации этого продукта.")

# def home(request: HttpRequest) -> HttpResponse:
#     """  Отображает главную страницу """
#     return render(request, 'home.html')

# def product_detail(request: HttpRequest, pk) -> HttpResponse:
#     """Выводит данные по одному продукту"""
#     product = get_object_or_404(Product, pk=pk)
#     context = {"product": product}
#     return render(request, 'catalog/product_detail.html', context)

# def products_list(request: HttpRequest) -> HttpResponse:
#     """Выводит данные по всем продуктам"""
#     products = Product.objects.all()
#     context = {"products": products}
#     return render(request, 'product_list.html', context)

# def contacts(request: HttpRequest) -> HttpResponse:
#     """ Отображает страницу контактов и форму обратной связи """
#     if request.method == "POST":
#         name = request.POST.get("name")
#         message = request.POST.get("message")
#
#         return HttpResponse(f"Спасибо, {name}! Сообщение получено. <br>"
#                             f"Ваше сообщение: '{message}'")
#     return render(request, 'catalog/contacts.html')