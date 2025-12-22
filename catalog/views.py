from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


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
