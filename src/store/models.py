from django.db import models

# ============================================================
# Funciones del Laboratorio de la Semana 2 (almacenamiento en
# memoria). Se conservan comentadas como evidencia del código
# anterior; ya no se usan porque la persistencia ahora se
# maneja mediante el Model Prenda y Django ORM (Semana 3).
# ============================================================

# PRENDAS = [
#     {
#         'id': 1,
#         'nombre': 'Polo Oversize Rebel Classic',
#         'marca': 'Rebel',
#         'categoria': 'Polos',
#         'tipo': 'Unisex',
#         'talla': 'L',
#         'precio': 89.90,
#         'stock': 20,
#         'disponible': True,
#         'descripcion': 'Polo oversize de algodón peruano 100%, corte streetwear con logo bordado en el pecho.',
#     },
#     {
#         'id': 2,
#         'nombre': 'Hoodie Doggis Street Corp',
#         'marca': 'Doggis Clothing',
#         'categoria': 'Casacas y Poleras',
#         'tipo': 'Hombre',
#         'talla': 'M',
#         'precio': 159.90,
#         'stock': 8,
#         'disponible': True,
#         'descripcion': 'Buzo con capucha en French Terry, print frontal serigrafiado y bolsillo canguro.',
#     },
#     {
#         'id': 3,
#         'nombre': 'Jean Baggy Rasec Wide Leg',
#         'marca': 'Rasec',
#         'categoria': 'Jeans',
#         'tipo': 'Unisex',
#         'talla': '32',
#         'precio': 179.00,
#         'stock': 0,
#         'disponible': True,
#         'descripcion': 'Jean de corte ancho (baggy) en denim rígido, tiro medio, silueta skater.',
#     },
#     {
#         'id': 4,
#         'nombre': 'Casaca Selva Alegre Windbreaker',
#         'marca': 'Selva Alegre',
#         'categoria': 'Casacas y Poleras',
#         'tipo': 'Unisex',
#         'talla': 'XL',
#         'precio': 219.90,
#         'stock': 5,
#         'disponible': True,
#         'descripcion': 'Rompevientos ligero con capucha, inspirado en la identidad amazónica de la marca.',
#     },
#     {
#         'id': 5,
#         'nombre': 'Polera Cosa Nostra Crewneck',
#         'marca': 'Cosa Nostra',
#         'categoria': 'Casacas y Poleras',
#         'tipo': 'Hombre',
#         'talla': 'M',
#         'precio': 139.90,
#         'stock': 12,
#         'disponible': True,
#         'descripcion': 'Crewneck en fleece pesado con bordado del logo característico en la manga.',
#     },
#     {
#         'id': 6,
#         'nombre': 'Polo Box Fit Mugre Basics',
#         'marca': 'Mugre',
#         'categoria': 'Polos',
#         'tipo': 'Unisex',
#         'talla': 'S',
#         'precio': 69.90,
#         'stock': 15,
#         'disponible': True,
#         'descripcion': 'Polo de corte cuadrado (box fit) en algodón peinado 24/1, tela pesada.',
#     },
#     {
#         'id': 7,
#         'nombre': 'Short Cargo Rebel Utility',
#         'marca': 'Rebel',
#         'categoria': 'Ropa Deportiva',
#         'tipo': 'Hombre',
#         'talla': '30',
#         'precio': 109.90,
#         'stock': 3,
#         'disponible': True,
#         'descripcion': 'Short cargo con bolsillos laterales tipo cartuchera y cordón ajustable.',
#     },
#     {
#         'id': 8,
#         'nombre': 'Vestido Oversized Tee Dress Rasec',
#         'marca': 'Rasec',
#         'categoria': 'Vestidos',
#         'tipo': 'Mujer',
#         'talla': 'Única',
#         'precio': 99.90,
#         'stock': 7,
#         'disponible': True,
#         'descripcion': 'Vestido tipo camiseta extralarga, silueta oversize, ideal para looks casuales.',
#     },
#     {
#         'id': 9,
#         'nombre': 'Casaca Denim Doggis Vintage Wash',
#         'marca': 'Doggis Clothing',
#         'categoria': 'Casacas y Poleras',
#         'tipo': 'Unisex',
#         'talla': 'L',
#         'precio': 189.90,
#         'stock': 4,
#         'disponible': False,
#         'descripcion': 'Casaca de mezclilla con lavado vintage y parche bordado en la espalda.',
#     },
#     {
#         'id': 10,
#         'nombre': 'Polo Niños Selva Alegre Mini',
#         'marca': 'Selva Alegre',
#         'categoria': 'Polos',
#         'tipo': 'Niños',
#         'talla': '8-10',
#         'precio': 59.90,
#         'stock': 10,
#         'disponible': True,
#         'descripcion': 'Versión infantil del polo insignia de la marca, algodón suave hipoalergénico.',
#     },
# ]
#
# def obtener_prendas():
#     return PRENDAS
#
# def obtener_prenda_por_id(prenda_id):
#     return next((p for p in PRENDAS if p['id'] == prenda_id), None)
#
# def agregar_prenda(nueva_prenda):
#     nueva_prenda['id'] = max((p['id'] for p in PRENDAS), default=0) + 1
#     PRENDAS.append(nueva_prenda)
#     return nueva_prenda


TIPOS_CHOICES = [
    ('Hombre', 'Moda Hombre'),
    ('Mujer', 'Moda Mujer'),
    ('Niños', 'Moda Infantil / Niños'),
    ('Unisex', 'Línea Unisex'),
]

CATEGORIAS_CHOICES = [
    ('Polos', 'Polos y Camisas'),
    ('Jeans', 'Pantalones y Jeans'),
    ('Casacas y Poleras', 'Casacas y Poleras'),
    ('Vestidos', 'Vestidos y Faldas'),
    ('Ropa Deportiva', 'Ropa Deportiva'),
    ('Calzado', 'Calzado'),
]

TALLAS_CHOICES = [
    ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'),
    ('28', '28'), ('30', '30'), ('32', '32'), ('34', '34'),
    ('4-6', '4-6 años'), ('8-10', '8-10 años'), ('12-14', '12-14 años'),
    ('Única', 'Talla Única'),
]


class Prenda(models.Model):
    nombre = models.CharField(max_length=120)
    marca = models.CharField(max_length=80)
    tipo = models.CharField(max_length=20, choices=TIPOS_CHOICES)
    categoria = models.CharField(max_length=40, choices=CATEGORIAS_CHOICES)
    talla = models.CharField(max_length=10, choices=TALLAS_CHOICES)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    activo = models.BooleanField(default=True, help_text="Indica si el registro está activo en el sistema o archivado")
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre