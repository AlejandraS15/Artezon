from django import forms
from django.contrib.auth import authenticate


class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@dominio.com"}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"}))


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            from django.contrib.auth.models import User
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Correo electrónico o contraseña incorrectos.")
            user = authenticate(username=user.username, password=password)
            if user is None:
                raise forms.ValidationError("Correo electrónico o contraseña incorrectos.")
            cleaned_data["user"] = user
        return cleaned_data
