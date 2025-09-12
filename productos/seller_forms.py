from django import forms

from .models import SellerProfile, Store

class SellerProfileForm(forms.ModelForm):
    alias = forms.CharField(label="Nombre de usuario / alias", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alias público'}))
    descripcion = forms.CharField(label="Breve descripción / biografía", required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Habla sobre tu experiencia, tradición o pasión por el arte artesanal', 'rows': 3}))
    redes_sociales = forms.CharField(label="Redes sociales (Instagram, Facebook, TikTok, etc.)", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}))
    ubicacion = forms.CharField(label="Ubicación geográfica", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad, región, etc. (opcional)'}))

    class Meta:
        model = SellerProfile
        fields = ['nombre', 'alias', 'foto_perfil', 'correo', 'contacto', 'descripcion', 'redes_sociales', 'ubicacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico de contacto'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono o WhatsApp'}),
        }

class StoreForm(forms.ModelForm):
    banner = forms.ImageField(label="Banner o imagen de portada", required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    politica_devoluciones = forms.CharField(label="Política de devoluciones / cambios", required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe tu política de devoluciones o cambios', 'rows': 2}))

    class Meta:
        model = Store
        fields = [
            'nombre', 'logotipo', 'banner', 'descripcion', 'color_principal', 'color_secundario', 'tema_visual',
            'categorias', 'metodos_pago', 'politica_envios', 'politica_devoluciones', 'stock_inicial'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la tienda'}),
            'logotipo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '¿Qué productos vendes? ¿Cuál es la filosofía o inspiración antioqueña?', 'rows': 3}),
            'color_principal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color principal (ej: #FF5733 o azul)'}),
            'color_secundario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color secundario'}),
            'tema_visual': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tema visual (ej: claro, oscuro, pastel...)'}),
            'categorias': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Crochet, tejidos, decoración, souvenirs...'}),
            'metodos_pago': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Transferencia, PayPal, contraentrega, tarjetas'}),
            'politica_envios': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tiempo, costos, regiones cubiertas', 'rows': 2}),
            'stock_inicial': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }