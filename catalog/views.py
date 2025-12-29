from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product


def home(request: HttpRequest) -> HttpResponse:
    """  Отображает главную страницу """
    return render(request, 'home.html')


def contacts(request: HttpRequest) -> HttpResponse:
    """ Отображает страницу контактов и форму обратной связи """
    if request.method == "POST":
        name = request.POST.get("name")
        message = request.POST.get("message")

        return HttpResponse(f"Спасибо, {name}! Сообщение получено. <br>"
                            f"Ваше сообщение: '{message}'")
    return render(request, 'contacts.html')


def product_detail(request: HttpRequest, pk) -> HttpResponse:
    """Выводит данные по одному продукту"""
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, 'product_detail.html', context)


def products_list(request: HttpRequest) -> HttpResponse:
    """Выводит данные по всем продуктам"""
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'products_list.html', context)
