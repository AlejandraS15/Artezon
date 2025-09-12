from django import forms
from productos.models import Product  # Importa el modelo correcto

class ProductoForm(forms.ModelForm):
    name = forms.CharField(
        label="Nombre del producto",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ejemplo: Bufanda tejida"
        }),
    )
    description = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Describe tu producto",
            "rows": 3
        }),
        required=False,
    )
    category = forms.CharField(
        label="Categoría",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ejemplo: Ropa"
        }),
        required=False,
    )
    material = forms.CharField(
        label="Material",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ejemplo: Algodón"
        }),
        required=False,
    )
    color = forms.CharField(
        label="Color",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ejemplo: Beige"
        }),
        required=False,
    )
    price = forms.DecimalField(
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
        model = Product
        fields = [
            'name', 'description', 'category', 'material', 'color',
            'price', 'stock', 'imagen'
        ]