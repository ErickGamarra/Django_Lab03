# Informe de Cambios y Persistencia — UrbanTrend (Semana 3, Parte 1)

Este informe documenta detalladamente todas las modificaciones realizadas en el proyecto **UrbanTrend**, explicando la transición de almacenamiento temporal en memoria RAM a persistencia relacional con **Django Models, Migraciones, Django ORM y SQLite**, incluyendo la adición del campo `activo` para control administrativo y soft-delete.

---

## 📋 Índice de Contenidos
1. [Diagnóstico y Análisis (Ejercicio 1)](#1-diagnóstico-y-análisis-ejercicio-1)
2. [Modelo de Datos en `store/models.py` (Ejercicio 2)](#2-modelo-de-datos-en-storemodelspy-ejercicio-2)
3. [Configuración del Admin en `store/admin.py`](#3-configuración-del-admin-en-storeadminpy)
4. [Estructura Persistente y Migraciones (Ejercicio 3)](#4-estructura-persistente-y-migraciones-ejercicio-3)
5. [Consultas con Django ORM en `store/views.py` (Ejercicio 4)](#5-consultas-con-django-orm-en-storeviewspy-ejercicio-4)
6. [Registro y Creación con ORM en `store/views.py` (Ejercicio 5)](#6-registro-y-creación-con-orm-en-storeviewspy-ejercicio-5)
7. [Script de Población Inicial `src/seed_prendas.py`](#7-script-de-población-inicial-srcseed_prendaspy)
8. [Pruebas Automatizadas en `store/tests.py`](#8-pruebas-automatizadas-en-storetestspy)
9. [Flujo de Persistencia y Mapeo SQL (Ejercicio 6)](#9-flujo-de-persistencia-y-mapeo-sql-ejercicio-6)
10. [Evidencia de Persistencia Real tras Reinicio](#10-evidencia-de-persistencia-real-tras-reinicio)

---

## 1. Diagnóstico y Análisis (Ejercicio 1)

### ¿Qué ocurría en la Semana 2?
En la versión previa, los datos se almacenaban en una lista en memoria RAM: `PRENDAS = [...]` dentro de `store/models.py`, manipulada con funciones auxiliares (`obtener_prendas()`, `obtener_prenda_por_id()`, `agregar_prenda()`).

### Causa técnica del problema:
La memoria RAM es un almacenamiento volátil. El ciclo de vida de la lista `PRENDAS` estaba ligado estrictamente al proceso en ejecución del servidor web (`python manage.py runserver`). Cuando el proceso se apagaba, se reiniciaba o recargaba por cambios de código (*hot reload*), el sistema operativo liberaba la memoria asignada al proceso.

### Consecuencia:
Todos los registros añadidos mediante `agregar_prenda()` durante la ejecución se destruían de forma permanente, regresando siempre a la lista hardcodeada original.

---

## 2. Modelo de Datos en `store/models.py` (Ejercicio 2)

Se definió el modelo `Prenda` heredando de `models.Model`, mapeando cada atributo a tipos de campos específicos de Django con opciones predefinidas (`choices`) y los campos de control `disponible` (comercial) y `activo` (control administrativo y de sistema).

Se conservó la lista `PRENDAS` y las funciones de la Semana 2 debidamente comentadas como evidencia histórica.

### 📄 Código implementado en `src/store/models.py`:

```python
from django.db import models

# ============================================================
# Funciones del Laboratorio de la Semana 2 (almacenamiento en
# memoria). Se conservan comentadas como evidencia del código
# anterior; ya no se usan porque la persistencia ahora se
# maneja mediante el Model Prenda y Django ORM (Semana 3).
# ============================================================

# PRENDAS = [ ... 10 prendas base ... ]
# def obtener_prendas(): ...
# def obtener_prenda_por_id(prenda_id): ...
# def agregar_prenda(nueva_prenda): ...


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
```

### Justificación técnica:
- `DecimalField(max_digits=8, decimal_places=2)`: Previene errores de precisión en cálculos financieros/monetarios.
- `PositiveIntegerField(default=0)`: Restringe a nivel de base de datos que el stock no pueda tomar números negativos.
- `choices`: Restringe los valores permitidos y genera automáticamente etiquetas legibles en formularios y admin.
- `activo = models.BooleanField(default=True)`: Permite borrado lógico (soft-delete), habilitación para futuros dashboards y segmentación de datos de administración vs. catálogo público.

---

## 3. Configuración del Admin en `store/admin.py`

Se registró `Prenda` con utilidades de búsqueda, filtrado y edición directa de `precio`, `stock`, `disponible` y `activo`.

### 📄 Código implementado en `src/store/admin.py`:

```python
from django.contrib import admin
from .models import Prenda


@admin.register(Prenda)
class PrendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'marca', 'tipo', 'categoria', 'talla', 'precio', 'stock', 'disponible', 'activo')
    list_filter = ('tipo', 'categoria', 'disponible', 'activo')
    search_fields = ('nombre', 'marca', 'descripcion')
    list_editable = ('precio', 'stock', 'disponible', 'activo')
```

---

## 4. Estructura Persistente y Migraciones (Ejercicio 3)

### Comandos ejecutados:

```powershell
# 1. Generación de la migración inicial
python manage.py makemigrations store
# Genera store/migrations/0001_initial.py (Create model Prenda)

# 2. Migración para el nuevo campo activo
python manage.py makemigrations store
# Genera store/migrations/0002_prenda_activo.py (Add field activo to prenda)

# 3. Aplicación a la base de datos SQLite
python manage.py migrate

# 4. Comprobación del estado de migraciones
python manage.py showmigrations store
# store
#  [X] 0001_initial
#  [X] 0002_prenda_activo
```

---

## 5. Consultas con Django ORM en `store/views.py` (Ejercicio 4)

Se implementó filtrado por `activo=True` para asegurar que el catálogo público solo muestre prendas vigentes, manteniendo el filtrado por texto (`Q`) y categorías.

### 📄 Código implementado para `prenda_list` y `prenda_detail`:

```python
from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Q
from .models import Prenda
from .forms import PrendaForm


def prenda_list(request):
    query = request.GET.get('q', '').strip().lower()
    tipo = request.GET.get('tipo', '').strip()
    categoria = request.GET.get('categoria', '').strip()

    prendas = Prenda.objects.filter(activo=True)

    if query:
        prendas = prendas.filter(
            Q(nombre__icontains=query) |
            Q(marca__icontains=query) |
            Q(descripcion__icontains=query)
        )

    if tipo:
        prendas = prendas.filter(tipo=tipo)

    if categoria:
        prendas = prendas.filter(categoria=categoria)

    total_catalogo = Prenda.objects.filter(activo=True).count()
    total_stock_global = sum(p.stock for p in Prenda.objects.filter(activo=True))
    total_activas = Prenda.objects.filter(activo=True, disponible=True).count()

    contexto = {
        'titulo': 'Catálogo de Ropa Streetwear',
        'prendas': prendas,
        'query': request.GET.get('q', ''),
        'tipo_seleccionado': tipo,
        'categoria_seleccionada': categoria,
        'total_resultados': prendas.count(),
        'total_catalogo': total_catalogo,
        'total_stock_global': total_stock_global,
        'total_activas': total_activas,
    }
    return render(request, 'store/prenda_list.html', contexto)


def prenda_detail(request, prenda_id):
    try:
        prenda = Prenda.objects.get(id=prenda_id, activo=True)
    except Prenda.DoesNotExist:
        raise Http404(f"La prenda con ID #{prenda_id} no existe o no está activa.")

    return render(request, 'store/prenda_detail.html', {
        'prenda': prenda,
        'titulo': f"Detalle: {prenda.nombre}",
    })
```

---

## 6. Registro y Creación con ORM en `store/views.py` (Ejercicio 5)

### 📄 Código implementado para `prenda_create`:

```python
def prenda_create(request):
    if request.method == 'POST':
        form = PrendaForm(request.POST)
        if form.is_valid():
            Prenda.objects.create(
                nombre=form.cleaned_data['nombre'],
                marca=form.cleaned_data['marca'],
                tipo=form.cleaned_data['tipo'],
                categoria=form.cleaned_data['categoria'],
                talla=form.cleaned_data['talla'],
                precio=form.cleaned_data['precio'],
                stock=form.cleaned_data['stock'],
                disponible=form.cleaned_data['disponible'],
                activo=form.cleaned_data.get('activo', True),
                descripcion=form.cleaned_data['descripcion'],
            )
            return redirect('store:list')
    else:
        form = PrendaForm()

    return render(request, 'store/prenda_form.html', {
        'titulo': 'Registrar Nueva Prenda',
        'form': form,
    })
```

---

## 7. Formulario `store/forms.py`

### 📄 Código en `src/store/forms.py`:

```python
from django import forms

# choices: TIPOS_CHOICES, CATEGORIAS_CHOICES, TALLAS_CHOICES...

class PrendaForm(forms.Form):
    nombre = forms.CharField(max_length=120, required=True, label="Nombre del Producto",
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    marca = forms.CharField(max_length=80, required=True, label="Marca / Fabricante",
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo = forms.ChoiceField(choices=TIPOS_CHOICES, required=True, label="Público / Tipo",
                             widget=forms.Select(attrs={'class': 'form-select'}))
    categoria = forms.ChoiceField(choices=CATEGORIAS_CHOICES, required=True, label="Categoría",
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    talla = forms.ChoiceField(choices=TALLAS_CHOICES, required=True, label="Talla",
                              widget=forms.Select(attrs={'class': 'form-select'}))
    precio = forms.DecimalField(required=True, min_value=0, label="Precio (S/)",
                                widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.10'}))
    stock = forms.IntegerField(required=True, min_value=0, label="Stock",
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    disponible = forms.BooleanField(required=False, initial=True, label="Disponible para venta")
    activo = forms.BooleanField(required=False, initial=True, label="Activo en el catálogo (Habilitado)")
    descripcion = forms.CharField(required=False, label="Descripción",
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
```

---

## 8. Pruebas Automatizadas en `store/tests.py`

8 pruebas unitarias que cubren filtrado por `activo`, estados de catálogo, respuestas 404 para prendas inactivas, creación con persistencia y cálculos agregados.

```powershell
python manage.py test store
# Ran 8 tests in 0.062s -> OK
```

---

## 9. Flujo de Persistencia y Mapeo SQL (Ejercicio 6)

### Tabla Comparativa de Ciclo de Vida:

| Paso | Consulta (`prenda_list`) | Creación (`prenda_create`) |
|---|---|---|
| **Request** | `GET /ropa/?q=rebel` | `POST /ropa/nueva/` con payload de formulario |
| **URL** | `store:list` $\rightarrow$ `views.prenda_list` | `store:create` $\rightarrow$ `views.prenda_create` |
| **View** | `prenda_list()` procesa filtros | `prenda_create()` valida `PrendaForm` |
| **Model** | `Prenda` | `Prenda` |
| **Manager / QuerySet** | `Prenda.objects.filter(activo=True)` | `Prenda.objects.create(...)` |
| **Django ORM** | Traduce el QuerySet a SQL `SELECT` | Traduce `create()` a SQL `INSERT` |
| **SQLite Engine** | Ejecuta `SELECT ... WHERE activo = 1` | Ejecuta `INSERT INTO store_prenda (...) VALUES (...)` |
| **View / Context** | Inyecta el `QuerySet` en `contexto` | Procesa redirección |
| **Template** | `prenda_list.html` itera sobre `prendas` | — (Redirección HTTP 302 hacia `/ropa/`) |
| **Response** | HTTP 200 con tabla de catálogo | HTTP 302 Found |

### Mapeo de Operaciones ORM a SQL:
- `Prenda.objects.all()` / `.filter(...)` $\rightarrow$ `SELECT`
- `Prenda.objects.create(...)` $\rightarrow$ `INSERT`
- `prenda.save()` $\rightarrow$ `UPDATE`
- `prenda.delete()` $\rightarrow$ `DELETE`

---

## 10. Evidencia de Persistencia Real tras Reinicio

1. Se registró desde la interfaz web la prenda `#11`: **Casaca Cortaviento Urban Street Tech** (S/ 149.90, Stock 10, Activo True).
2. Se apagó por completo el servidor (`task kill` / `Ctrl+C`).
3. Se verificó el contenido directo en `db.sqlite3` y todas las 11 prendas persisten en disco.
4. Se reinició el servidor y se confirmó que el registro `#11` **permanece en la base de datos y visible en la web**.
