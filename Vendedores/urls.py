from django.urls import path
from . import views

urlpatterns = [
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('mis-productos/', views.mis_productos, name='mis_productos'),
]
