from django.test import TestCase, Client
from django.urls import reverse
from .models import Prenda


class PrendaModelAndORMTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.prenda1 = Prenda.objects.create(
            nombre="Polo Oversize Rebel Classic",
            marca="Rebel",
            tipo="Unisex",
            categoria="Polos",
            talla="L",
            precio=89.90,
            stock=20,
            disponible=True,
            activo=True,
            descripcion="Polo oversize de algodón peruano 100%."
        )
        self.prenda2 = Prenda.objects.create(
            nombre="Hoodie Doggis Street Corp",
            marca="Doggis Clothing",
            tipo="Hombre",
            categoria="Casacas y Poleras",
            talla="M",
            precio=159.90,
            stock=8,
            disponible=True,
            activo=True,
            descripcion="Buzo con capucha en French Terry."
        )
        self.prenda3 = Prenda.objects.create(
            nombre="Casaca Denim Doggis Vintage Wash",
            marca="Doggis Clothing",
            tipo="Unisex",
            categoria="Casacas y Poleras",
            talla="L",
            precio=189.90,
            stock=4,
            disponible=False,
            activo=True,
            descripcion="Casaca de mezclilla con lavado vintage."
        )
        self.prenda_inactiva = Prenda.objects.create(
            nombre="Prenda Archivada Antigua",
            marca="Vintage",
            tipo="Unisex",
            categoria="Polos",
            talla="M",
            precio=29.90,
            stock=0,
            disponible=False,
            activo=False,
            descripcion="Prenda desactivada del sistema."
        )

    def test_modelo_prenda_str(self):
        """El método __str__ debe retornar el nombre de la prenda"""
        self.assertEqual(str(self.prenda1), "Polo Oversize Rebel Classic")

    def test_prenda_list_view_status_and_context(self):
        """La vista prenda_list debe responder con 200 y contener solo las prendas activas"""
        response = self.client.get(reverse('store:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/prenda_list.html')
        # Solo 3 activas (la 4ta está con activo=False)
        self.assertEqual(response.context['total_catalogo'], 3)
        self.assertEqual(response.context['total_stock_global'], 32)
        self.assertEqual(response.context['total_activas'], 2)

    def test_prenda_list_filter_search(self):
        """Filtrado por texto de búsqueda en nombre, marca o descripción"""
        response = self.client.get(reverse('store:list'), {'q': 'Doggis'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['prendas']), 2)

        response_desc = self.client.get(reverse('store:list'), {'q': 'algodón'})
        self.assertEqual(len(response_desc.context['prendas']), 1)
        self.assertEqual(response_desc.context['prendas'][0].id, self.prenda1.id)

    def test_prenda_list_filter_tipo_and_categoria(self):
        """Filtrado por segmento (tipo) y por categoría"""
        response_tipo = self.client.get(reverse('store:list'), {'tipo': 'Hombre'})
        self.assertEqual(len(response_tipo.context['prendas']), 1)
        self.assertEqual(response_tipo.context['prendas'][0].marca, 'Doggis Clothing')

        response_cat = self.client.get(reverse('store:list'), {'categoria': 'Casacas y Poleras'})
        self.assertEqual(len(response_cat.context['prendas']), 2)

    def test_prenda_detail_view_success(self):
        """La vista prenda_detail debe responder con 200 para una prenda existente y activa"""
        response = self.client.get(reverse('store:detail', args=[self.prenda1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/prenda_detail.html')
        self.assertEqual(response.context['prenda'].nombre, self.prenda1.nombre)

    def test_prenda_detail_view_404_inexistente_o_inactivo(self):
        """La vista prenda_detail debe devolver 404 para ID inexistente o si la prenda está inactiva"""
        response = self.client.get(reverse('store:detail', args=[999]))
        self.assertEqual(response.status_code, 404)

        # Prenda inactiva debe responder 404 en el catálogo público
        response_inactiva = self.client.get(reverse('store:detail', args=[self.prenda_inactiva.id]))
        self.assertEqual(response_inactiva.status_code, 404)

    def test_prenda_create_get(self):
        """GET a prenda_create debe retornar el formulario vacío con status 200"""
        response = self.client.get(reverse('store:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/prenda_form.html')

    def test_prenda_create_post_success(self):
        """POST a prenda_create con datos válidos debe crear el registro en la BD y redirigir"""
        initial_count = Prenda.objects.count()
        payload = {
            'nombre': 'Gorra Snapback Urban Rebel',
            'marca': 'Rebel',
            'tipo': 'Unisex',
            'categoria': 'Ropa Deportiva',
            'talla': 'Única',
            'precio': '49.90',
            'stock': 15,
            'disponible': True,
            'activo': True,
            'descripcion': 'Gorra estilo snapback con bordado 3D frontal.'
        }
        response = self.client.post(reverse('store:create'), data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('store:list'))
        self.assertEqual(Prenda.objects.count(), initial_count + 1)

        nueva = Prenda.objects.get(nombre='Gorra Snapback Urban Rebel')
        self.assertEqual(nueva.marca, 'Rebel')
        self.assertEqual(nueva.talla, 'Única')
        self.assertEqual(float(nueva.precio), 49.90)
        self.assertEqual(nueva.stock, 15)
        self.assertTrue(nueva.disponible)
        self.assertTrue(nueva.activo)
