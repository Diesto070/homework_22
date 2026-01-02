from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Ваше имя",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите имя"}),
    )
    phone = forms.CharField(max_length=100, label="Телефон", widget=forms.TextInput(attrs={"class": "form-control"}))
    message = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Напишите сообщение"}),
        label="Сообщение",
    )
