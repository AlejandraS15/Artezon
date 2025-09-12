# ────────── IMPORTS ──────────
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Para los mensajes flash

from .models import Product, Profile, SellerProfile, Store
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from .seller_forms import SellerProfileForm, StoreForm
from .email_login_form import EmailLoginForm

# ────────── VISTAS HOME ──────────
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
    """Landing page inicial con botones de registro e inicio de sesión."""
    return render(request, "productos/landing.html", {"is_landing": True})


# ────────── VISTAS USUARIO ──────────
def register_view(request):
    """Registro de usuarios nuevos."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "productos/register.html", {"form": form})


def email_login_view(request):
    """Login personalizado por correo electrónico."""
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            tipo_usuario = form.cleaned_data["tipo_usuario"]
            login(request, user)
            request.session["tipo_usuario"] = tipo_usuario
            if tipo_usuario == "comprador_vendedor":
                # Si es vendedor y comprador, verificar si ya tiene perfil de vendedor
                from .models import SellerProfile
                if SellerProfile.objects.filter(user=user).exists():
                    return redirect("store_profile")
                else:
                    return redirect("create_seller_and_store")
            else:
                # Solo comprador
                return redirect("home")
    else:
        form = EmailLoginForm()
    return render(request, "productos/login.html", {"form": form})


class CustomLogoutView(LogoutView):
    next_page = "landing"


@login_required
def profile_view(request):
    """Vista para mostrar los datos del perfil del usuario logueado."""
    profile = request.user.profile
    return render(request, "productos/profile.html", {"profile": profile})


@login_required
def edit_profile(request):
    """Editar la información personal y de perfil del usuario."""
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "✅ Perfil actualizado con éxito")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(
        request,
        "productos/edit_profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


# ────────── VISTAS VENDEDOR / TIENDA ──────────
@login_required
def store_profile_view(request):
    """Vista para mostrar el perfil de la tienda."""
    try:
        seller_profile = request.user.sellerprofile
        store = seller_profile.store
    except (SellerProfile.DoesNotExist, Store.DoesNotExist):
        messages.info(request, 'Primero debes crear tu perfil de vendedor y tienda.')
        return redirect('create_seller_and_store')
    return render(request, 'productos/store_profile.html', {'store': store})


@login_required
def create_seller_and_store(request):
    """Crear perfil de vendedor y tienda."""
    try:
        seller_profile = request.user.sellerprofile
        return redirect('edit_seller_and_store')
    except SellerProfile.DoesNotExist:
        seller_profile = None

    if request.method == 'POST':
        seller_form = SellerProfileForm(request.POST, request.FILES)
        store_form = StoreForm(request.POST, request.FILES)
        if seller_form.is_valid() and store_form.is_valid():
            seller = seller_form.save(commit=False)
            seller.user = request.user
            seller.save()
            store = store_form.save(commit=False)
            store.seller = seller
            store.save()
            messages.success(request, '✅ Perfil de vendedor y tienda creados correctamente.')
            return redirect('home')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        seller_form = SellerProfileForm()
        store_form = StoreForm()

    return render(request, 'productos/seller_store_form.html', {
        'seller_form': seller_form,
        'store_form': store_form,
        'modo': 'crear',
    })


@login_required
def edit_seller_and_store(request):
    """Editar perfil de vendedor y tienda existente."""
    try:
        seller_profile = request.user.sellerprofile
        store = seller_profile.store
    except (SellerProfile.DoesNotExist, Store.DoesNotExist):
        return redirect('create_seller_and_store')

    if request.method == 'POST':
        seller_form = SellerProfileForm(request.POST, request.FILES, instance=seller_profile)
        store_form = StoreForm(request.POST, request.FILES, instance=store)
        if seller_form.is_valid() and store_form.is_valid():
            seller_form.save()
            store_form.save()
            messages.success(request, '✅ Perfil de vendedor y tienda actualizados correctamente.')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        seller_form = SellerProfileForm(instance=seller_profile)
        store_form = StoreForm(instance=store)

    return render(request, 'productos/seller_store_form.html', {
        'seller_form': seller_form,
        'store_form': store_form,
        'modo': 'editar',
    })
