from django.urls import path
from . import views

urlpatterns = [
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('mis-productos/', views.mis_productos, name='mis_productos'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
]
