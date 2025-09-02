from django.urls import path
from .views import ProductListView

app_name = "productos"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
]