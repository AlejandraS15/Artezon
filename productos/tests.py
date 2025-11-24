from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from productos.models import Product

class SimpleViewTests(TestCase):

    def test_home_page_status(self):
        """La página de inicio debe cargar correctamente."""
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ProductModelTest(TestCase):

    def test_crear_producto(self):
        """El modelo Product debe guardarse correctamente."""

        # Crear un usuario para asignarlo como seller (obligatorio)
        user = User.objects.create_user(username="testuser", password="12345")

        producto = Product.objects.create(
            seller=user,
            name="Gorro",
            price=15000,
            description="Gorro hecho a mano",
            category="Accesorios",
            material="Lana",
            color="Rosado",
            stock=10
        )

        # Validaciones
        self.assertEqual(producto.name, "Gorro")
        self.assertEqual(producto.price, 15000)
        self.assertEqual(producto.seller.username, "testuser")
        self.assertTrue(producto.id)