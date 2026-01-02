from typing import Any

from django.core.exceptions import ValidationError
from django.forms import BooleanField, ModelForm

from catalog.models import Product

# Список запрещенных слов для валидации
words_forbidden = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]


class StyleFormMixin:
    """Миксин для автоматического добавления CSS - классов к полям формы.
    Автоматически назначает классы 'form-control' для обычных полей и 'form-check-input'
    для булевых полей(чекбоксов)."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    """Форма для создания и редактирования продуктов.
    Включает валидацию на наличие запрещенных слов в названии и описании продукта."""

    class Meta:
        """Метаданные формы продукта."""

        model = Product
        fields = "__all__"

    def clean_name(self) -> Any:
        """Валидация названия продуктов.
        Проверяет, что название не содержит запрещенных слов."""
        name = self.cleaned_data.get("name")

        if name.lower() in words_forbidden:
            raise ValidationError(f'"{name}" нельзя использовать в названии продукта')
        return name

    def clean_description(self) -> Any:
        """Валидация описания продуктов.
        Проверяет, что описание продуктов не содержит запрещенных слов."""
        description = self.cleaned_data.get("description")

        for words in words_forbidden:
            if words in description.lower():
                raise ValidationError(f'Нельзя использовать слово "{words}"в описании продукта')
        return description

    def clean_purchase_price(self) -> Any:
        """Валидация проверяет, что цена продукта не может быть отрицательной.
        Если цена введена неправильно, отображается соответствующее сообщение пользователю"""
        price = self.cleaned_data.get("purchase_price")
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной. Введите другое значение.")
        return price

    def clean_picture(self) -> object:
        """Валидация проверяет, загружаемое изображение на соответствие формату и размеру."""
        picture = self.cleaned_data.get("picture")

        if picture:
            if picture.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
                raise ValidationError("Можно загружать только JPG и PNG файлы")

            if picture.size > 5 * 1024 * 1024:
                raise ValidationError("Размер изображения не должен превышать 5 МБ.")
        return picture
