from django.shortcuts import render
from django.db.models import Q

from .models import Product


def home(request):
    """
    Vista principal que muestra barra de búsqueda,
    filtros y productos disponibles.
    """

    query = request.GET.get("q", "")
    material = request.GET.get("material", "")
    color = request.GET.get("color", "")
    price_min = request.GET.get("price_min", "")
    price_max = request.GET.get("price_max", "")

    productos = Product.objects.all()

    if query:
        productos = productos.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if material:
        productos = productos.filter(material=material)

    if color:
        productos = productos.filter(color=color)

    if price_min:
        productos = productos.filter(price__gte=price_min)

    if price_max:
        productos = productos.filter(price__lte=price_max)

    materiales = Product.objects.values_list(
        "material", flat=True
    ).distinct()
    colores = Product.objects.values_list(
        "color", flat=True
    ).distinct()

    context = {
        "productos": productos,
        "current_filters": {
            "q": query,
            "material": material,
            "color": color,
            "precio_min": price_min,
            "precio_max": price_max,
        },
        "materiales": materiales,
        "colores": colores,
    }
    return render(request, "productos/home.html", context)