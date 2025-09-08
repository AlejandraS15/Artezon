from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # 👈 aquí se define el name="home"
]