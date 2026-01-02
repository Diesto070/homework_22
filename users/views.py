import secrets

from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    """Контроллер регистрации нового пользователя с подтверждением email.
    Обрабатывает процесс регистрации: создает неактивного пользователя,
    генерирует токен подтверждения и отправляет письмо с ссылкой для активации."""

    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form: UserRegisterForm) -> HttpResponse:
        """Обрабатывает валидную форму регистрации пользователя.
        Создает неактивного пользователя, генерирует токен подтверждения,
        отправляет email с ссылкой для активации аккаунта."""
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Здравствуйте! Благодарим вас за регистрацию в нашем онлайн-магазине.\n"
            f"Если у вас возникнут вопросы, пожалуйста, свяжитесь с нами.\n"
            f"С уважением, Команда онлайн-магазина.\n"
            f"Для подтверждения почты, перейди по ссылке {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )  # Отправка самого сообщения
        return super().form_valid(form)


def email_verification(request: HttpRequest, token: str) -> HttpResponse:
    """Активация пользователя по токену подтверждения email.
    Находит пользователя по токену, активирует его учетную запись
    и очищает использованный токен."""
    user = get_object_or_404(User, token=token)  # получаем пользователя
    user.is_active = True
    user.token = None  # Очищаем токен после использования
    user.save()
    return redirect(reverse("users:login"))
