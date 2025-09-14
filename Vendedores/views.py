from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm
from productos.models import Product

@login_required
def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.seller = request.user  # Asigna el vendedor actual
            producto.save()
            return redirect("mis_productos")
    else:
        form = ProductoForm()
    return render(request, "forms/agregar_productos.html", {"form": form})

@login_required
def mis_productos(request):
    productos = Product.objects.filter(seller=request.user)
    return render(request, "manejoProductos/mis_productos.html", {"productos": productos})

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
            producto.seller = request.user  # Mantiene el vendedor actual
            producto.save()
            return redirect("mis_productos")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "forms/editar_producto.html", {"form": form, "producto": producto})
