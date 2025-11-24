# ────────── IMPORTS ──────────
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import quote
from django.utils.translation import gettext as _

from .product_form import ProductForm
from .models import Product, Profile, SellerProfile, Store
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, ExternalAPIForm
from .seller_forms import SellerProfileForm, StoreForm
from .email_login_form import EmailLoginForm
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer
import requests
from django.views.generic import FormView


# ────────── API REST ──────────
class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ExternalAPIFormView(FormView):
    template_name = "external_api/external_api.html"
    form_class = ExternalAPIForm
    success_url = "."

    def form_valid(self, form):
        url = form.cleaned_data["url"]
        data = None
        error = None

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            error = f"Error al consumir el servicio: {str(e)}"

        return render(
            self.request,
            self.template_name,
            {
                "form": form,
                "data": data,
                "error": error,
            }
        )


# ────────── VISTAS PRODUCTO ──────────
@login_required
def create_product(request):
    """Vista para crear producto (requiere perfil de vendedor)."""
    try:
        seller_profile = SellerProfile.objects.get(user=request.user)
    except SellerProfile.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil de vendedor antes de publicar productos')
        return redirect('create_seller_and_store')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('store_profile')
    else:
        form = ProductForm()
    return render(request, 'productos/create_product.html', {'form': form})

from django.utils.translation import gettext as _
from django.shortcuts import render

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

    productos = Product.objects.select_related('seller__sellerprofile').all()

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


# ────────── FAVORITOS ──────────
@csrf_exempt
def toggle_favorite(request, producto_id):
    """Toggle favorito para un producto usando AJAX y sesión."""
    if request.method == "POST":
        favoritos = request.session.get("favoritos", [])
        if not isinstance(favoritos, list):
            favoritos = []
        
        producto_id_str = str(producto_id)
        if producto_id_str in favoritos:
            favoritos.remove(producto_id_str)
            favorito = False
        else:
            favoritos.append(producto_id_str)
            favorito = True
        
        request.session["favoritos"] = favoritos
        request.session.modified = True
        return JsonResponse({"favorito": favorito})
    return JsonResponse({"error": "Método no permitido"}, status=405)


@login_required
def favoritos(request):
    """Vista para mostrar productos favoritos del usuario."""
    favoritos_ids = request.session.get("favoritos", [])
    productos = Product.objects.filter(id__in=favoritos_ids)
    return render(request, "productos/favoritos.html", {"productos": productos})


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
            login(request, user)
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
    """Editar la información personal, perfil y vendedor del usuario."""
    user = request.user
    profile = user.profile
    try:
        seller_profile = user.sellerprofile
    except SellerProfile.DoesNotExist:
        seller_profile = None

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        seller_form = SellerProfileForm(request.POST, request.FILES, instance=seller_profile)

        forms_valid = user_form.is_valid() and profile_form.is_valid() and seller_form.is_valid()
        if forms_valid:
            user_form.save()
            profile_form.save()
            seller = seller_form.save(commit=False)
            seller.user = user
            seller.save()
            messages.success(request, "Perfil actualizado con éxito")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)
        seller_form = SellerProfileForm(instance=seller_profile)

    return render(
        request,
        "productos/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "seller_form": seller_form,
        },
    )

def product_detail(request, pk):
    producto = get_object_or_404(Product, pk=pk)

    # buscar perfil del vendedor
    seller_profile = SellerProfile.objects.filter(user=producto.seller).first()
    store = Store.objects.filter(seller=seller_profile).first() if seller_profile else None

    context = {
        "producto": producto,
        "seller_profile": seller_profile,
        "store": store,
    }
    return render(request, "productos/product_detail.html", context)


# ────────── VISTAS CARRITO ──────────
def ver_carrito(request):
    """Ver el carrito de compras."""
    carrito = request.session.get("carrito", {})

    if not isinstance(carrito, dict):
        carrito = {}
        request.session["carrito"] = carrito
        request.session.modified = True

    total = sum(item["precio"] * item["cantidad"] for item in carrito.values())

    return render(request, "carrito/ver_carrito.html", {
        "carrito": carrito,
        "total": total,
    })


def agregar_al_carrito(request, pk):
    """Agregar producto al carrito."""
    carrito = request.session.get("carrito", {})

    if not isinstance(carrito, dict):
        carrito = {}

    producto = get_object_or_404(Product, pk=pk)
    producto_id = str(producto.pk)

    if producto_id in carrito:
        carrito[producto_id]["cantidad"] += 1
    else:
        carrito[producto_id] = {
            "nombre": producto.name,
            "precio": float(producto.price),
            "cantidad": 1,
        }

    request.session["carrito"] = carrito
    request.session.modified = True

    messages.success(request, _("Se agregó %(producto)s al carrito.") % {"producto": producto.name})
    return redirect("ver_carrito")


def quitar_del_carrito(request, pk):
    """Quitar producto del carrito."""
    carrito = request.session.get("carrito", {})

    if not isinstance(carrito, dict):
        carrito = {}

    producto_id = str(pk)

    if producto_id in carrito:
        if carrito[producto_id]["cantidad"] > 1:
            carrito[producto_id]["cantidad"] -= 1
        else:
            del carrito[producto_id]

        request.session["carrito"] = carrito
        request.session.modified = True
        messages.warning(request, _("Producto eliminado del carrito."))

    return redirect("ver_carrito")


def limpiar_carrito(request):
    """Limpiar todo el carrito."""
    request.session["carrito"] = {}
    request.session.modified = True
    messages.warning(request, _("El carrito fue vaciado."))
    return redirect("ver_carrito")




# ────────── VISTAS VENDEDOR / TIENDA ──────────
@login_required
def store_profile_view(request):
    """Vista para mostrar el perfil de la tienda."""
    try:
        seller_profile = request.user.sellerprofile
        store = seller_profile.store
    except (SellerProfile.DoesNotExist, Store.DoesNotExist):
        messages.info(request, _("Primero debes crear tu perfil de vendedor y tienda."))
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
            messages.success(request, 'Perfil de vendedor y tienda creados correctamente.')
            return redirect('home')
        else:
            messages.error(request, _("Por favor corrige los errores en el formulario."))
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
            messages.success(request, 'Perfil de vendedor y tienda actualizados correctamente.')
            return redirect('profile')
        else:
            messages.error(request, _("Por favor corrige los errores en el formulario."))
    else:
        seller_form = SellerProfileForm(instance=seller_profile)
        store_form = StoreForm(instance=store)

    return render(request, 'productos/seller_store_form.html', {
        'seller_form': seller_form,
        'store_form': store_form,
        'modo': 'editar',
    })


def export_products_report(request):
    """Exporta un reporte de productos como archivo (CSV o JSON según configuración).

    Usa la fábrica `get_report_generator()` en `productos/factories.py`.
    """
    from .factories import get_report_generator
    # usamos el modelo `Product` ya importado en este módulo
    # Obtener más detalles de producto. Mapear seller__username -> seller_username
    raw_rows = Product.objects.values(
        "name",
        "price",
        "description",
        "category",
        "material",
        "color",
        "stock",
        "created_at",
        "seller__username",
    )

    rows = []
    for r in raw_rows:
        rows.append({
            "name": r.get("name"),
            "price": r.get("price"),
            "description": r.get("description", ""),
            "category": r.get("category", ""),
            "material": r.get("material", ""),
            "color": r.get("color", ""),
            "stock": r.get("stock", 0),
            # convertir created_at a ISO string para evitar problemas de serialización
            "created_at": (r.get("created_at").isoformat() if r.get("created_at") else ""),
            "seller_username": r.get("seller__username", ""),
        })

    generator = get_report_generator()
    file_bytes = generator.generate(rows)

    response = HttpResponse(file_bytes, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{generator.filename()}"'
    return response

def _formatear_items_carrito_para_mensaje(carrito):
    partes = []
    for _id, item in carrito.items():
        cantidad = item.get("cantidad", 0)
        nombre = item.get("nombre", "").strip()
        if nombre:
            partes.append(f"{cantidad} {nombre}")
    if not partes:
        return ""
    if len(partes) == 1:
        return partes[0]
    return ", ".join(partes[:-1]) + " y " + partes[-1]


def comprar_carrito(request):
    carrito = request.session.get("carrito", {})
    if not isinstance(carrito, dict) or not carrito:
        messages.warning(request, "El carrito está vacío.")
        return redirect("home")

    total = sum(item.get("precio", 0) * item.get("cantidad", 0)
                for item in carrito.values())
    items_texto = _formatear_items_carrito_para_mensaje(carrito)

    mensaje = (
        f"Hola, deseo comprar {items_texto}. "
        f"Total: ${total:.2f}. ¿Podrían confirmarme disponibilidad y envío? Gracias."
    )

    numero = getattr(settings, "WHATSAPP_NUMBER", "")
    if not numero:
        messages.error(request, "Número de WhatsApp no configurado.")
        return redirect("ver_carrito")

    url = f"https://wa.me/{numero}?text={quote(mensaje)}"
    return redirect(url)
