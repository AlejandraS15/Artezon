from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("home/", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
]
