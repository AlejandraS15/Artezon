from django.db import models
from django.contrib.auth.models import User

# class Producto(models.Model):
#     vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="productos")
#     nombre = models.CharField(max_length=200)
#     descripcion = models.TextField()
#     precio = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.PositiveIntegerField(default=0)
#     imagen = models.ImageField(upload_to="productos/", blank=True, null=True)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.nombre

