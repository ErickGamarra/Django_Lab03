import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Prenda

prendas_data = [
    {
        'id': 1,
        'nombre': 'Polo Oversize Rebel Classic',
        'marca': 'Rebel',
        'categoria': 'Polos',
        'tipo': 'Unisex',
        'talla': 'L',
        'precio': 89.90,
        'stock': 20,
        'disponible': True,
        'descripcion': 'Polo oversize de algodón peruano 100%, corte streetwear con logo bordado en el pecho.',
    },
    {
        'id': 2,
        'nombre': 'Hoodie Doggis Street Corp',
        'marca': 'Doggis Clothing',
        'categoria': 'Casacas y Poleras',
        'tipo': 'Hombre',
        'talla': 'M',
        'precio': 159.90,
        'stock': 8,
        'disponible': True,
        'descripcion': 'Buzo con capucha en French Terry, print frontal serigrafiado y bolsillo canguro.',
    },
    {
        'id': 3,
        'nombre': 'Jean Baggy Rasec Wide Leg',
        'marca': 'Rasec',
        'categoria': 'Jeans',
        'tipo': 'Unisex',
        'talla': '32',
        'precio': 179.00,
        'stock': 0,
        'disponible': True,
        'descripcion': 'Jean de corte ancho (baggy) en denim rígido, tiro medio, silueta skater.',
    },
    {
        'id': 4,
        'nombre': 'Casaca Selva Alegre Windbreaker',
        'marca': 'Selva Alegre',
        'categoria': 'Casacas y Poleras',
        'tipo': 'Unisex',
        'talla': 'XL',
        'precio': 219.90,
        'stock': 5,
        'disponible': True,
        'descripcion': 'Rompevientos ligero con capucha, inspirado en la identidad amazónica de la marca.',
    },
    {
        'id': 5,
        'nombre': 'Polera Cosa Nostra Crewneck',
        'marca': 'Cosa Nostra',
        'categoria': 'Casacas y Poleras',
        'tipo': 'Hombre',
        'talla': 'M',
        'precio': 139.90,
        'stock': 12,
        'disponible': True,
        'descripcion': 'Crewneck en fleece pesado con bordado del logo característico en la manga.',
    },
    {
        'id': 6,
        'nombre': 'Polo Box Fit Mugre Basics',
        'marca': 'Mugre',
        'categoria': 'Polos',
        'tipo': 'Unisex',
        'talla': 'S',
        'precio': 69.90,
        'stock': 15,
        'disponible': True,
        'descripcion': 'Polo de corte cuadrado (box fit) en algodón peinado 24/1, tela pesada.',
    },
    {
        'id': 7,
        'nombre': 'Short Cargo Rebel Utility',
        'marca': 'Rebel',
        'categoria': 'Ropa Deportiva',
        'tipo': 'Hombre',
        'talla': '30',
        'precio': 109.90,
        'stock': 3,
        'disponible': True,
        'descripcion': 'Short cargo con bolsillos laterales tipo cartuchera y cordón ajustable.',
    },
    {
        'id': 8,
        'nombre': 'Vestido Oversized Tee Dress Rasec',
        'marca': 'Rasec',
        'categoria': 'Vestidos',
        'tipo': 'Mujer',
        'talla': 'Única',
        'precio': 99.90,
        'stock': 7,
        'disponible': True,
        'descripcion': 'Vestido tipo camiseta extralarga, silueta oversize, ideal para looks casuales.',
    },
    {
        'id': 9,
        'nombre': 'Casaca Denim Doggis Vintage Wash',
        'marca': 'Doggis Clothing',
        'categoria': 'Casacas y Poleras',
        'tipo': 'Unisex',
        'talla': 'L',
        'precio': 189.90,
        'stock': 4,
        'disponible': False,
        'descripcion': 'Casaca de mezclilla con lavado vintage y parche bordado en la espalda.',
    },
    {
        'id': 10,
        'nombre': 'Polo Niños Selva Alegre Mini',
        'marca': 'Selva Alegre',
        'categoria': 'Polos',
        'tipo': 'Niños',
        'talla': '8-10',
        'precio': 59.90,
        'stock': 10,
        'disponible': True,
        'descripcion': 'Versión infantil del polo insignia de la marca, algodón suave hipoalergénico.',
    },
]

for p in prendas_data:
    obj, created = Prenda.objects.update_or_create(
        id=p['id'],
        defaults=p
    )
    print(f"[{'CREADO' if created else 'ACTUALIZADO'}] ID #{obj.id}: {obj.nombre} (S/{obj.precio})")

print(f"\nTotal de prendas registradas en la base de datos SQLite: {Prenda.objects.count()}")
