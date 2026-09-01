## Contexto

En la Semana 2 se construyó **UrbanTrend**, un catálogo digital de ropa streetwear en Django, usando el patrón MVT: Views, URLs, Templates y un formulario (`PrendaForm`). Los datos se guardaban en una lista de diccionarios en memoria RAM (`PRENDAS` en `store/models.py`), con funciones auxiliares `obtener_prendas()`, `obtener_prenda_por_id()` y `agregar_prenda()`. El problema: cada vez que se reinicia el servidor, todos los registros agregados se pierden, porque nunca se guardan en disco.

En este laboratorio (Semana 3, Parte 1) vamos a resolver eso: convertir esa estructura temporal en **persistencia real** usando **Django Models, migraciones, Django ORM y SQLite**. Al terminar, los datos sobrevivirán a un reinicio del servidor, y las Views leerán y escribirán directamente contra la base de datos en vez de manipular una lista en memoria.

Sigue los pasos en orden. No avances al siguiente ejercicio sin terminar y verificar el anterior.

---

## Ejercicio 1 — Recuperar y analizar la aplicación anterior

1. Abre el proyecto y localiza:
   - Entidad principal: `Prenda` (representada hoy como diccionario, no como Model).
   - Datos en memoria: lista `PRENDAS` en `store/models.py`.
   - Views: `prenda_list`, `prenda_detail`, `prenda_create` en `store/views.py`.
   - URLs: `store/urls.py` (`list`, `detail`, `create`).
   - Formulario: `PrendaForm` en `store/forms.py`.
   - Templates: `store/templates/store/prenda_list.html`, `prenda_detail.html`, `prenda_form.html`.
2. Redacta un párrafo corto explicando qué ocurre con los registros agregados por `agregar_prenda()` cuando se reinicia el servidor (se pierden porque `PRENDAS` es una lista en memoria RAM, no hay persistencia en disco).
3. Guarda este análisis como texto (lo usaremos en el informe final), no requiere código todavía.

---

## Ejercicio 2 — Convertir la entidad en un Django Model

Agrega a `store/models.py` un modelo real. Mantén los mismos campos que ya existen en los diccionarios y en `PrendaForm`, usando tipos de datos apropiados de Django.

```python
from django.db import models

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
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
```

**Importante:** no borres la lista `PRENDAS` ni las funciones `obtener_prendas()`, `obtener_prenda_por_id()` y `agregar_prenda()`. Coméntalas para que dejen de ejecutarse, dejando claro que corresponden al laboratorio anterior (Semana 2), como evidencia de la versión previa del código:

```python
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
#     # ... (10 prendas base registradas)
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
```

---

## Ejercicio 3 — Crear la estructura persistente de datos

Desde `src/`, con el entorno virtual activado, ejecuta:

```powershell
python manage.py makemigrations store
python manage.py migrate
python manage.py showmigrations store
```

Toma **captura de pantalla** de la salida de los tres comandos. Verifica que se creó la tabla `store_prenda` en `db.sqlite3`.

Comando opcional para confirmar visualmente la tabla:

```powershell
python manage.py dbshell
.tables
.schema store_prenda
.quit
```

---

## Ejercicio 4 — Implementar la consulta mediante ORM

Edita `store/views.py`. Sustituye la llamada a `obtener_prendas()` en `prenda_list` por un `QuerySet` de Django ORM.

```python
from django.shortcuts import render
from .models import Prenda

def prenda_list(request):
    query = request.GET.get('q', '').strip().lower()
    tipo = request.GET.get('tipo', '').strip()
    categoria = request.GET.get('categoria', '').strip()

    prendas = Prenda.objects.all()

    if query:
        from django.db.models import Q
        prendas = prendas.filter(
            Q(nombre__icontains=query) |
            Q(marca__icontains=query) |
            Q(descripcion__icontains=query)
        )

    if tipo:
        prendas = prendas.filter(tipo=tipo)

    if categoria:
        prendas = prendas.filter(categoria=categoria)

    total_catalogo = Prenda.objects.count()
    total_stock_global = sum(p.stock for p in Prenda.objects.all())
    total_activas = Prenda.objects.filter(disponible=True).count()

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
```

Adapta también `prenda_detail` para usar el ORM en vez de `obtener_prenda_por_id`:

```python
from django.http import Http404

def prenda_detail(request, prenda_id):
    try:
        prenda = Prenda.objects.get(id=prenda_id)
    except Prenda.DoesNotExist:
        raise Http404(f"La prenda con ID #{prenda_id} no existe.")

    return render(request, 'store/prenda_detail.html', {
        'prenda': prenda,
        'titulo': f"Detalle: {prenda.nombre}",
    })
```

> Nota: como `Prenda` ahora es un objeto de modelo (no un diccionario), en los templates cambia `prenda.nombre`, `prenda.stock`, etc. — la sintaxis de Django templates es la misma para diccionarios y objetos, así que **no necesitas tocar los templates**.

Antes de continuar, carga algunos registros de prueba desde el admin o el shell:

```powershell
python manage.py shell
```

```python
from store.models import Prenda
Prenda.objects.create(nombre="Polo Oversize Rebel Classic", marca="Rebel", tipo="Unisex",
    categoria="Polos", talla="L", precio=89.90, stock=20, disponible=True,
    descripcion="Polo oversize de algodón peruano 100%.")
```

Verifica en el navegador (`http://127.0.0.1:8000/ropa/`) que el registro aparece correctamente.

---

## Ejercicio 5 — Implementar el registro mediante ORM

Edita `prenda_create` en `store/views.py` para guardar con Django ORM en vez de `agregar_prenda()`:

```python
from django.shortcuts import redirect
from .forms import PrendaForm

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

> Alternativa más "Django-idiomática" (opcional, no obligatoria para este ejercicio): convertir `PrendaForm` en un `ModelForm` de `Prenda` y usar `form.save()` directamente. Si el agente lo hace, debe documentar el cambio y ajustar `forms.py` en consecuencia.

**Prueba de persistencia:**
1. Registra una prenda nueva desde `/ropa/nueva/`.
2. Verifica que aparece en `/ropa/`.
3. Reinicia el servidor (`Ctrl+C` y `python manage.py runserver` de nuevo).
4. Confirma que la prenda **sigue apareciendo** — esta es la evidencia clave de persistencia real.

---

## Ejercicio 6 — Analizar el flujo de persistencia

Documenta (en texto, para el informe) el recorrido completo de una **consulta** y de una **creación**, siguiendo este esquema:

```
Request → URL → View → Model → Manager / QuerySet → Django ORM → SQLite → View → Context → Template → Response
```

Para cada paso, indica qué ocurre concretamente en el proyecto UrbanTrend. Por ejemplo:

| Paso | Consulta (Ejercicio 4) | Creación (Ejercicio 5) |
|---|---|---|
| Request | GET a `/ropa/` | POST a `/ropa/nueva/` con datos del formulario |
| URL | `store:list` → `views.prenda_list` | `store:create` → `views.prenda_create` |
| View | `prenda_list()` recibe filtros GET | `prenda_create()` valida `PrendaForm` |
| Model | `Prenda` | `Prenda` |
| Manager/QuerySet | `Prenda.objects.all()` / `.filter(...)` | `Prenda.objects.create(...)` |
| Django ORM | Traduce el QuerySet a SQL | Traduce `create()` a SQL |
| SQLite | Ejecuta `SELECT ... FROM store_prenda ...` | Ejecuta `INSERT INTO store_prenda ...` |
| Template | `prenda_list.html` recorre `prendas` | — (redirect, no renderiza directamente) |
| Response | HTML con la tabla de prendas | Redirect 302 → `/ropa/` |

Indica explícitamente la operación SQL conceptual detrás de cada acción ORM:
- `Prenda.objects.all()` / `.filter(...)` → `SELECT`
- `Prenda.objects.create(...)` → `INSERT`
- (para referencia futura en la Parte 2) `.save()` sobre un objeto existente → `UPDATE`, `.delete()` → `DELETE`

---

## Checklist de verificación antes de cerrar la Parte 1

- [ ] `store/models.py` contiene la clase `Prenda(models.Model)` con todos los campos.
- [ ] La lista `PRENDAS` y las funciones `obtener_prendas()`, `obtener_prenda_por_id()`, `agregar_prenda()` quedaron comentadas (no eliminadas) y marcadas como pertenecientes al laboratorio de la Semana 2.
- [ ] `makemigrations`, `migrate` y `showmigrations` ejecutados y con captura de pantalla.
- [ ] `prenda_list` usa `Prenda.objects.all()` / `.filter(...)`, ya no `obtener_prendas()`.
- [ ] `prenda_detail` usa `Prenda.objects.get(id=...)`, ya no `obtener_prenda_por_id()`.
- [ ] `prenda_create` usa `Prenda.objects.create(...)`, ya no `agregar_prenda()`.
- [ ] Se registró una prenda nueva, se reinició el servidor y el dato **persiste**.
- [ ] Está documentado el flujo Request → ... → Response para consulta y creación, con las operaciones SQL asociadas.
- [ ] Capturas de pantalla guardadas: `makemigrations`/`migrate`/`showmigrations`, listado con datos, formulario de creación, listado tras reiniciar el servidor con el dato persistido.

Una vez completado este checklist, la Parte 1 está lista para el informe. La Parte 2 (nueva app con 5 entidades y relación ForeignKey) se aborda en un documento aparte.
