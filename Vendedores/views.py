from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm

@login_required
def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user  # asignamos el vendedor actual
            producto.save()
            return redirect("mis_productos")  # redirigir a la lista de productos del vendedor
    else:
        form = ProductoForm()
    return render(request, "productos/agregar_producto.html", {"form": form})

@login_required
def mis_productos(request):
    productos = request.user.productos.all()
    return render(request, "productos/mis_productos.html", {"productos": productos})
