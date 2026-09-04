from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from .models import Proveedor, Sucursal, Transportista, CategoriaInsumo, Material
from .forms import ProveedorForm, TransportistaForm, MaterialForm


class LogisticsModelTests(TestCase):
    def setUp(self):
        self.cat = CategoriaInsumo.objects.create(
            nombre="Telas y Tejidos",
            descripcion="Insumos para confección"
        )
        self.material = Material.objects.create(
            categoria=self.cat,
            nombre="Algodón Pima",
            unidad_medida="Metros",
            precio_unitario=Decimal("35.00"),
            stock=100
        )
        self.proveedor = Proveedor.objects.create(
            ruc="20601234567",
            razon_social="Textil S.A.",
            telefono="987654321",
            correo="info@textil.pe"
        )
        self.sucursal = Sucursal.objects.create(
            nombre="Almacén Sur",
            direccion="Av. Industrial 123",
            ciudad="Lima",
            capacidad_almacen=20000
        )
        self.transportista = Transportista.objects.create(
            empresa="Carga Express",
            placa="ABC-123",
            tipo_vehiculo="Camión 5TN",
            activo=True
        )

    def test_string_representations(self):
        self.assertEqual(str(self.cat), "Telas y Tejidos")
        self.assertEqual(str(self.material), "Algodón Pima (Telas y Tejidos)")
        self.assertEqual(str(self.proveedor), "Textil S.A. (20601234567)")
        self.assertEqual(str(self.sucursal), "Almacén Sur - Lima")
        self.assertEqual(str(self.transportista), "Carga Express [ABC-123]")

    def test_relationship_categoria_materiales(self):
        # Comprobar acceso inverso mediante related_name='materiales'
        self.assertEqual(self.cat.materiales.count(), 1)
        self.assertEqual(self.cat.materiales.first(), self.material)

    def test_cascade_delete(self):
        # Al eliminar la categoría padre, el material hijo se elimina por CASCADE
        self.cat.delete()
        self.assertEqual(Material.objects.count(), 0)


class LogisticsFormTests(TestCase):
    def test_proveedor_form_valid_ruc(self):
        form = ProveedorForm(data={
            'ruc': '20123456789',
            'razon_social': 'Proveedor Valido SAC',
            'telefono': '999888777',
            'correo': 'ventas@valido.pe'
        })
        self.assertTrue(form.is_valid())

    def test_proveedor_form_invalid_ruc_length(self):
        form = ProveedorForm(data={
            'ruc': '2012345',  # Menos de 11 dígitos
            'razon_social': 'Invalido SAC',
            'telefono': '999888777',
            'correo': 'test@invalido.pe'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('ruc', form.errors)

    def test_transportista_form_clean_placa_uppercase(self):
        form = TransportistaForm(data={
            'empresa': 'Transportes Lima',
            'placa': '  abc-999  ',
            'tipo_vehiculo': 'Furgón',
            'activo': True
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['placa'], 'ABC-999')

    def test_material_form_invalid_negative_price(self):
        cat = CategoriaInsumo.objects.create(nombre="Avíos")
        form = MaterialForm(data={
            'categoria': cat.id,
            'nombre': 'Botones',
            'unidad_medida': 'Piezas',
            'precio_unitario': '-5.00',
            'stock': 10
        })
        self.assertFalse(form.is_valid())
        self.assertIn('precio_unitario', form.errors)


class LogisticsViewCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cat = CategoriaInsumo.objects.create(
            nombre="Telas",
            descripcion="Categoría principal"
        )
        self.material = Material.objects.create(
            categoria=self.cat,
            nombre="Tela Jersey",
            unidad_medida="Metros",
            precio_unitario=Decimal("20.00"),
            stock=50
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('logistics:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Módulo de Logística")
        self.assertEqual(response.context['total_materiales'], 1)

    def test_material_list_view(self):
        response = self.client.get(reverse('logistics:material_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tela Jersey")

    def test_material_create_view(self):
        # Operación CREATE -> INSERT y redirección PRG
        response = self.client.post(reverse('logistics:material_create'), {
            'categoria': self.cat.id,
            'nombre': 'Tela Rib',
            'unidad_medida': 'Metros',
            'precio_unitario': '25.00',
            'stock': 80
        })
        self.assertRedirects(response, reverse('logistics:material_list'))
        self.assertEqual(Material.objects.count(), 2)
        self.assertTrue(Material.objects.filter(nombre='Tela Rib').exists())

    def test_material_update_view(self):
        # Operación UPDATE
        response = self.client.post(
            reverse('logistics:material_update', kwargs={'pk': self.material.pk}),
            {
                'categoria': self.cat.id,
                'nombre': 'Tela Jersey Premium',
                'unidad_medida': 'Metros',
                'precio_unitario': '24.50',
                'stock': 120
            }
        )
        self.assertRedirects(response, reverse('logistics:material_list'))
        self.material.refresh_from_db()
        self.assertEqual(self.material.nombre, 'Tela Jersey Premium')
        self.assertEqual(self.material.stock, 120)

    def test_material_delete_view(self):
        # Operación DELETE
        pk = self.material.pk
        response = self.client.post(reverse('logistics:material_delete', kwargs={'pk': pk}))
        self.assertRedirects(response, reverse('logistics:material_list'))
        self.assertFalse(Material.objects.filter(pk=pk).exists())
