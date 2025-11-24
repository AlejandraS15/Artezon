from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


# Perfil de vendedor
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    foto_perfil = models.ImageField(upload_to="vendedores/perfiles/", blank=True, null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])]
    )
    contacto = models.CharField(max_length=50, blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vendedor: {self.nombre} ({self.user.username})"

# Tienda online
class Store(models.Model):
    seller = models.OneToOneField(SellerProfile, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    logotipo = models.ImageField(upload_to="vendedores/tiendas/", blank=True, null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])]
    )
    color_principal = models.CharField(max_length=30, blank=True)
    color_secundario = models.CharField(max_length=30, blank=True)
    tema_visual = models.CharField(max_length=30, blank=True)
    metodos_pago = models.CharField(max_length=200, blank=True, help_text="Ej: Transferencia, PayPal, Efectivo")
    politica_envios = models.TextField(blank=True)
    stock_inicial = models.PositiveIntegerField(default=0)
    categorias = models.CharField(max_length=200, blank=True, help_text="Ej: Ropa, Accesorios, Decoración")
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tienda: {self.nombre} (Vendedor: {self.seller.nombre})"


class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)
    material = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to="imagenProductos/", blank=True, null=True)

    def save(self, *args, **kwargs):
        """Comprime y redimensiona la imagen automáticamente al guardar"""
        if self.imagen:
            # Abrir la imagen
            img = Image.open(self.imagen)
            
            # Convertir a RGB si es necesario (para PNG con transparencia)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Redimensionar si es muy grande (máximo 1200px en el lado más largo)
            max_size = (1200, 1200)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Guardar en memoria con compresión
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            # Reemplazar la imagen original con la comprimida
            self.imagen = InMemoryUploadedFile(
                output, 'ImageField',
                f"{self.imagen.name.split('.')[0]}.jpg",
                'image/jpeg',
                sys.getsizeof(output), None
            )
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Tablas auxiliares para preferencias
class Color(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Accesorio(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Información básica personal
    foto_perfil = models.ImageField(upload_to="perfiles/", blank=True, null=True, validators=[FileExtensionValidator(["jpg", "jpeg", "png"])])
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)

    # Preferencias de productos
    TIPO_LANA_CHOICES = [
        ("algodon", "Algodón"),
        ("lana", "Lana"),
        ("acrilico", "Acrílico"),
        ("mezcla", "Mezcla"),
    ]
    tipo_lana = models.CharField(
        max_length=20, choices=TIPO_LANA_CHOICES, blank=True
    )

    colores_favoritos = models.ManyToManyField(Color, blank=True)
    accesorios_favoritos = models.ManyToManyField(Accesorio, blank=True)

    def save(self, *args, **kwargs):
        """Comprime y redimensiona la foto de perfil automáticamente al guardar"""
        if self.foto_perfil:
            # Abrir la imagen
            img = Image.open(self.foto_perfil)
            
            # Convertir a RGB si es necesario
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Redimensionar a 500x500 para foto de perfil
            max_size = (500, 500)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Guardar en memoria con compresión
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            # Reemplazar la imagen original con la comprimida
            self.foto_perfil = InMemoryUploadedFile(
                output, 'ImageField',
                f"{self.foto_perfil.name.split('.')[0]}.jpg",
                'image/jpeg',
                sys.getsizeof(output), None
            )
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Perfil de {self.user.username}"


# Señales para crear y guardar perfil automáticamente
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
