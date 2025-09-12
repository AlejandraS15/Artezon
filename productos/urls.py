

from django.urls import path
from .views import (
    home,
    landing_page,
    register_view,
    email_login_view,
    CustomLogoutView,
    profile_view,
    edit_profile,
    create_seller_and_store,
    edit_seller_and_store,
    store_profile_view,
)

urlpatterns = [
    path("", landing_page, name="landing"),
    path("home/", home, name="home"),
    path("register/", register_view, name="register"),
    path("login/", email_login_view, name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", profile_view, name="profile"),
    path("edit-profile/", edit_profile, name="edit_profile"),  # 👈 ruta única
    path("vendedor/crear/", create_seller_and_store, name="create_seller_and_store"),
    path("vendedor/editar/", edit_seller_and_store, name="edit_seller_and_store"),
    path("mi-tienda/", store_profile_view, name="store_profile"),
]
