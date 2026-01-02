from typing import Any, Union

from django import template

register = template.Library()


@register.filter()
def media_filter(path: Union[str, Any]) -> str:
    """Фильтр для формирования URL медиа‑файла."""
    if path:
        return f"/media/{path}"
    return "#"
