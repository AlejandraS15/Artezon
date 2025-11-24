from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from .models import Profile, Color, Accesorio


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Escribe tu nombre de usuario"}
        ),
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "correo@dominio.com"}
        ),
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Escribe tu contraseña"}
        ),
        help_text="Mínimo 8 caracteres, debe incluir números y al menos 1 carácter especial (@#$%&*!)"
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Repite tu contraseña"}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        
        if not re.search(r'\d', password):
            raise ValidationError("La contraseña debe incluir al menos un número.")
        
        if not re.search(r'[@#$%&*!]', password):
            raise ValidationError("La contraseña debe incluir al menos un carácter especial (@#$%&*!).")
        
        return password


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Nombre",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu nombre"}),
    )
    last_name = forms.CharField(
        label="Apellido",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu apellido"}),
    )
    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@dominio.com"}),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileUpdateForm(forms.ModelForm):
    telefono = forms.CharField(
        label="Teléfono",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ejemplo: +57 300 123 4567"}),
    )
    direccion = forms.CharField(
        label="Dirección",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ejemplo: Calle 123 #45-67"}),
    )
    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    ciudad = forms.CharField(
        label="Ciudad",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu ciudad"})
    )
    tipo_lana = forms.ChoiceField(
        label="Tipo de lana favorita",
        choices=Profile.TIPO_LANA_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    colores_favoritos = forms.ModelMultipleChoiceField(
        queryset=Color.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Colores favoritos"
    )

    class Meta:
        model = Profile
        fields = [
            "telefono",
            "direccion",
            "fecha_nacimiento",
            "ciudad",
            "tipo_lana",
            "colores_favoritos",
        ]
