from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    nombre = forms.CharField(
        label="Nombre del producto",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ejemplo: Bufanda tejida"
        }),
    )
    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Describe tu producto",
            "rows": 3
        }),
    )
    precio = forms.DecimalField(
        label="Precio",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Ejemplo: 15000"
        }),
    )
    stock = forms.IntegerField(
        label="Stock disponible",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Ejemplo: 10"
        }),
    )
    imagen = forms.ImageField(
        label="Imagen del producto",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control"
        }),
    )

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen']