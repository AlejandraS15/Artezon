from django.shortcuts import render
from decimal import Decimal, InvalidOperation
from django.views.generic import ListView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = "productos/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True, stock__gt=0)
        material = self.request.GET.get("material")
        color = self.request.GET.get("color")
        price_min = self.request.GET.get("price_min")
        price_max = self.request.GET.get("price_max")

        if material:
            qs = qs.filter(material__iexact=material)
        if color:
            qs = qs.filter(color__iexact=color)
        if price_min:
            try:
                qs = qs.filter(price__gte=Decimal(price_min))
            except (InvalidOperation, TypeError):
                pass
        if price_max:
            try:
                qs = qs.filter(price__lte=Decimal(price_max))
            except (InvalidOperation, TypeError):
                pass

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["materials"] = (
            Product.objects.filter(is_active=True).exclude(material="")
            .values_list("material", flat=True).distinct().order_by("material")
        )
        ctx["colors"] = (
            Product.objects.filter(is_active=True).exclude(color="")
            .values_list("color", flat=True).distinct().order_by("color")
        )
        ctx["current_filters"] = {
            "material": self.request.GET.get("material", ""),
            "color": self.request.GET.get("color", ""),
            "price_min": self.request.GET.get("price_min", ""),
            "price_max": self.request.GET.get("price_max", ""),
        }
        return ctx
