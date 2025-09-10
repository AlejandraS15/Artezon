from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from .models import Product
from .forms import RegisterForm


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

    materiales = Product.objects.values_list("material", flat=True).distinct()
    colores = Product.objects.values_list("color", flat=True).distinct()

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


def landing_page(request):
    """
    Landing page inicial con botones de registro e inicio de sesión.
    """
    return render(request, "productos/landing.html")


def register_view(request):
    """
    Registro de usuarios nuevos.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "productos/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "productos/login.html"


class CustomLogoutView(LogoutView):
    next_page = "landing"
