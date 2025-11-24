from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import ProductoForm
from productos.models import Product

def calcular_precio_sugerido(material, horas, experiencia):
    base = 1000
    material_factor = {
        'algodon': 1.0,
        'lana': 1.2,
        'cuero': 1.5,
    }
    experiencia_factor = {
        'principiante': 1.0,
        'intermedio': 1.2,
        'experto': 1.5,
    }
    precio = base * material_factor.get(material, 1) * experiencia_factor.get(experiencia, 1) + (horas * 500)
    return round(precio, 2)

@login_required
def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.seller = request.user
            # Calcula el precio sugerido
            material = form.cleaned_data.get('material')
            horas = form.cleaned_data.get('horas')
            experiencia = form.cleaned_data.get('experiencia')
            producto.price = calcular_precio_sugerido(material, horas, experiencia)
            producto.save()
            return redirect("mis_productos")
    else:
        form = ProductoForm()
    return render(request, "forms/agregar_productos.html", {"form": form})

@login_required
def mis_productos(request):
    productos = Product.objects.filter(seller=request.user)
    
    # Búsqueda por nombre
    search_query = request.GET.get('search', '')
    if search_query:
        productos = productos.filter(name__icontains=search_query)
    
    # Filtro por estado
    estado_filter = request.GET.get('estado', '')
    if estado_filter == 'activo':
        productos = productos.filter(is_active=True, stock__gt=0)
    elif estado_filter == 'inactivo':
        productos = productos.filter(is_active=False)
    elif estado_filter == 'sin_stock':
        productos = productos.filter(stock=0)
    
    # Filtro por rango de precio
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    if precio_min:
        productos = productos.filter(price__gte=precio_min)
    if precio_max:
        productos = productos.filter(price__lte=precio_max)
    
    # Ordenamiento
    orden = request.GET.get('orden', '-created_at')
    if orden in ['-created_at', 'created_at', '-price', 'price', '-stock', 'stock', 'name']:
        productos = productos.order_by(orden)
    
    # Paginación
    paginator = Paginator(productos, 15)  # 15 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    total_productos = Product.objects.filter(seller=request.user).count()
    productos_activos = Product.objects.filter(seller=request.user, is_active=True, stock__gt=0).count()
    valor_inventario = sum([p.price * p.stock for p in Product.objects.filter(seller=request.user)])
    
    return render(request, "manejoProductos/mis_productos.html", {
        "page_obj": page_obj,
        "productos": page_obj,
        "total_productos": total_productos,
        "productos_activos": productos_activos,
        "valor_inventario": valor_inventario,
        "search_query": search_query,
        "estado_filter": estado_filter,
        "precio_min": precio_min,
        "precio_max": precio_max,
        "orden": orden,
    })

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Product, id=producto_id, seller=request.user)
    if request.method == "POST":
        producto.delete()
        return redirect('mis_productos')
    return render(request, "forms/confirmar_eliminacion.html", {"producto": producto})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Product, id=producto_id, seller=request.user)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.seller = request.user
            material = form.cleaned_data.get('material')
            horas = form.cleaned_data.get('horas')
            experiencia = form.cleaned_data.get('experiencia')
            producto.price = calcular_precio_sugerido(material, horas, experiencia)
            producto.save()
            return redirect("mis_productos")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "forms/editar_producto.html", {"form": form, "producto": producto})
