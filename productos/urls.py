from django.urls import path
from . import views
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
    ProductListAPIView,
    ExternalAPIFormView
)

urlpatterns = [
    path('api/products/', ProductListAPIView.as_view(), name='api_products'),
    path('external_api/', ExternalAPIFormView.as_view(), name='external_api'),
    path("producto/crear/", views.create_product, name="create_product"),
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
    path("producto/<int:pk>/", views.product_detail, name="product_detail"),
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("carrito/agregar/<int:pk>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("carrito/quitar/<int:pk>/", views.quitar_del_carrito, name="quitar_del_carrito"),
    path("carrito/limpiar/", views.limpiar_carrito, name="limpiar_carrito"),
    path("carrito/comprar/", views.comprar_carrito, name="comprar_carrito"),
]
