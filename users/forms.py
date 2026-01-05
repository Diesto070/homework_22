from django.contrib.auth.forms import UserCreationForm

from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """"""

    class Meta:
        """Метаданные формы пользователя."""

        model = User
        fields = ("email", "password1", "password2")
