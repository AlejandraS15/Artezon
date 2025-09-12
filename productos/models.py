
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator


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
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)
    material = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return f"Perfil de {self.user.username}"


# Señales para crear y guardar perfil automáticamente
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.profile.save()
