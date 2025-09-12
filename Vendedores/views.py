from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm
from productos.models import Product  # Importa el modelo correcto

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
