from django import forms
from productos.models import Product  # Importa el modelo correcto

class ProductoForm(forms.ModelForm):
    MATERIAL_CHOICES = [
        ('algodon', 'Algodón'),
        ('lana', 'Lana'),
        ('cuero', 'Cuero'),
        # agrega más materiales si lo necesitas
    ]
    EXPERIENCE_CHOICES = [
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('experto', 'Experto'),
    ]

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
    material = forms.ChoiceField(choices=MATERIAL_CHOICES, label="Material", widget=forms.Select(attrs={"class": "form-control"}))
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
    horas = forms.IntegerField(label="Horas invertidas", min_value=1, widget=forms.NumberInput(attrs={"class": "form-control"}))
    experiencia = forms.ChoiceField(choices=EXPERIENCE_CHOICES, label="Experiencia", widget=forms.Select(attrs={"class": "form-control"}))
    cantidad_material = forms.DecimalField(
        label="Cantidad de material (KG)",
        min_value=0.01,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Ejemplo: 0.5"
        }),
    )

    class Meta:
        model = Product
        fields = [
            'name', 'description', 'category', 'material', 'cantidad_material', 'color',
            'price', 'stock', 'imagen', 'horas', 'experiencia'
        ]