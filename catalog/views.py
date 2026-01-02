from typing import Any

from django import forms
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, TemplateView, UpdateView

from catalog.forms import ProductForm
from catalog.forms_contact import ContactForm
from catalog.models import Product


class HomeView(TemplateView):
    """Отображает главную страницу """
    template_name = 'catalog/home.html'


class ContactsView(FormView):
    """ Отображает страницу контактов и форму обратной связи """
    template_name = 'catalog/contacts.html'
    form_class = ContactForm

    def form_valid(self, form: forms.Form) -> HttpResponse:
        """Обрабатывает валидную форму и возвращает HTTP-ответ с результатом.
        Эта функция вызывается когда данные формы прошли валидацию."""
        name = form.cleaned_data['name']
        message = form.cleaned_data['message']
        response_content = (
            f"Спасибо, {name}! Сообщение получено.<br>"
            f"Ваше сообщение: '{message}'"
        )
        return HttpResponse(response_content)


class ProductListView(ListView):
    """  Отображает главную страницу с данными по всем продуктам """
    model = Product

    def get_queryset(self) -> Any:
        """Выводим последние созданные 5 продуктов в консоль"""
        products = Product.objects.order_by('-created_at')[:5]

        print("=== ПОСЛЕДНИЕ 5 ПРОДУКТОВ ===")
        for product in products:
            print(f"{product.id} - {product.name} ({product.created_at.strftime('%d.%m.%Y %H:%M')})")
        return Product.objects.all()


class ProductsListView(ListView):
    """Отображает все продукты в виде списка из базы данных
    в порядке убывания даты создания"""
    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'
    ordering = ['-created_at']


class ProductDetailView(DetailView):
    """Выводит данные по одному продукту"""
    model = Product


class ProductCreateView(CreateView):
    """"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form: Any) -> HttpResponse:
        """Обрабатывает валидную форму создания продукта."""
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')


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
