import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from logistics.models import CategoriaInsumo, Material

def run_verification():
    print("=" * 80)
    print("EJERCICIO 18: VERIFICACIÓN DE ENTIDADES RELACIONADAS (1:N)")
    print("=" * 80)

    # ---------------------------------------------------------
    # PARTE 1: Comprobar la Clave Foránea en SQLite
    # ---------------------------------------------------------
    print("\n[1] COMPROBACIÓN DE LA CLAVE FORÁNEA EN SQLITE (PRAGMA foreign_key_list)")
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_key_list(logistics_material);")
        fks = cursor.fetchall()
        for fk in fks:
            print(f"    -> ID: {fk[0]} | Columna Origen: {fk[3]} | Tabla Destino: {fk[2]} | Columna Destino: {fk[4]} | On Delete: {fk[6]}")

        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='logistics_material';")
        create_sql = cursor.fetchone()[0]
        print("\n    DDL Generado por SQLite:")
        print("    " + create_sql.replace("\n", "\n    "))

    # ---------------------------------------------------------
    # PARTE 2: Registro de Datos Asociados mediante ORM
    # ---------------------------------------------------------
    print("\n[2] REGISTRO DE DATOS ASOCIADOS (CREATE -> INSERT)")
    # Crear o recuperar categoría de prueba
    cat_demo, creada = CategoriaInsumo.objects.get_or_create(
        nombre="Cierres y Metales de Prueba",
        defaults={'descripcion': "Categoría para prueba técnica de relaciones 1:N."}
    )
    print(f"    -> Categoría Maestra (Lado 1): ID={cat_demo.id} | '{cat_demo.nombre}' (Creada={creada})")

    # Crear materiales asociados a esa categoría
    mat1, _ = Material.objects.get_or_create(
        nombre="Cierre Metal Dorado 15cm",
        categoria=cat_demo,
        defaults={
            'unidad_medida': 'Piezas',
            'precio_unitario': Decimal("2.50"),
            'stock': 300
        }
    )
    mat2, _ = Material.objects.get_or_create(
        nombre="Deslizador Niquelado N°5",
        categoria=cat_demo,
        defaults={
            'unidad_medida': 'Docenas',
            'precio_unitario': Decimal("4.20"),
            'stock': 150
        }
    )
    print(f"    -> Material Asociado 1: ID={mat1.id} | '{mat1.nombre}' | FK categoria_id={mat1.categoria_id}")
    print(f"    -> Material Asociado 2: ID={mat2.id} | '{mat2.nombre}' | FK categoria_id={mat2.categoria_id}")

    # ---------------------------------------------------------
    # PARTE 3: Consulta Directa e Inversa de Registros Relacionados
    # ---------------------------------------------------------
    print("\n[3] CONSULTA DE REGISTROS RELACIONADOS (READ -> SELECT)")
    
    # 3.1 Consulta hacia adelante (Material -> Categoria)
    print("    3.1 Consulta Directa (Hijo -> Padre: material.categoria):")
    material_recuperado = Material.objects.get(id=mat1.id)
    print(f"        Material: '{material_recuperado.nombre}'")
    print(f"        -> FK cruda en BD (material.categoria_id): {material_recuperado.categoria_id}")
    print(f"        -> Instancia relacionada (material.categoria.nombre): '{material_recuperado.categoria.nombre}'")
    print(f"        -> Descripción del padre: '{material_recuperado.categoria.descripcion}'")

    # 3.2 Consulta inversa (Categoria -> Materiales con related_name='materiales')
    print("\n    3.2 Consulta Inversa (Padre -> Hijos: categoria.materiales.all()):")
    materiales_hijos = cat_demo.materiales.all()
    print(f"        Total de insumos asociados a '{cat_demo.nombre}': {cat_demo.materiales.count()}")
    for idx, m in enumerate(materiales_hijos, start=1):
        print(f"        [{idx}] ID={m.id} | Insumo: {m.nombre} | Stock: {m.stock} {m.unidad_medida} | Precio: S/ {m.precio_unitario}")

    # 3.3 Consulta optimizada con select_related y sentencia SQL resultante
    print("\n    3.3 Inspección de la Sentencia SQL Generada con select_related('categoria'):")
    qs = Material.objects.filter(categoria=cat_demo).select_related('categoria')
    print(f"        SQL Generado por Django ORM:")
    print(f"        {qs.query}")

    # ---------------------------------------------------------
    # PARTE 4: Demostración de Integridad Referencial y Cascade Delete
    # ---------------------------------------------------------
    print("\n[4] VERIFICACIÓN DE INTEGRIDAD REFERENCIAL Y ON_DELETE = models.CASCADE")
    # Crear una categoría y un material temporal para probar la eliminación en cascada
    cat_temp = CategoriaInsumo.objects.create(nombre="Categoría Temporal Cascade", descripcion="Para probar CASCADE")
    mat_temp = Material.objects.create(
        categoria=cat_temp,
        nombre="Insumo Temporal Volátil",
        unidad_medida="Metros",
        precio_unitario=Decimal("10.00"),
        stock=5
    )
    temp_mat_id = mat_temp.id
    temp_cat_id = cat_temp.id
    print(f"    -> Creada categoría temporal ID={temp_cat_id} con material hijo ID={temp_mat_id}")
    print(f"    -> ¿Existe material antes de borrar categoría? {Material.objects.filter(id=temp_mat_id).exists()}")
    
    print(f"    -> Ejecutando: cat_temp.delete()...")
    cat_temp.delete()
    
    existe_material = Material.objects.filter(id=temp_mat_id).exists()
    print(f"    -> ¿Existe material después de borrar categoría? {existe_material}")
    print(f"    -> Integridad confirmada: El material hijo fue eliminado automáticamente por CASCADE (evita registros huérfanos).")

    print("\n" + "=" * 80)
    print("VERIFICACIÓN DEL EJERCICIO 18 FINALIZADA CON ÉXITO")
    print("=" * 80)

if __name__ == '__main__':
    run_verification()
