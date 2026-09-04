# Informe de Implementación — Módulo de Logística y Persistencia (Semana 3, Parte 2)

**Curso:** Desarrollo de Aplicaciones Empresariales  
**Sección:** 4 - C24 - Sección CD  
**Integrantes:**
1. Erick Arturo Gamarra Mundaca
2. Jesús Enrique Rocha Bobadilla  
**Docente:** Yunior Bestard Aroche  
**Proyecto:** UrbanTrend — Sistema de Gestión Logística y Abastecimiento Textil con Django ORM y SQLite  

---

## 📋 Índice de Contenidos
1. [Investigación de la Problemática Real (Ejercicio 7)](#1-investigación-de-la-problemática-real-ejercicio-7)
2. [Definición de Requisitos Funcionales (Ejercicio 8)](#2-definición-de-requisitos-funcionales-ejercicio-8)
3. [Diseño del Modelo de Datos (Ejercicio 9)](#3-diseño-del-modelo-de-datos-ejercicio-9)
4. [Representación de Relaciones ER (Ejercicio 10)](#4-representación-de-relaciones-er-ejercicio-10)
5. [Creación y Configuración de la App `logistics` (Ejercicio 11)](#5-creación-y-configuración-de-la-app-logistics-ejercicio-11)
6. [Implementación de Models en `logistics/models.py` (Ejercicio 12)](#6-implementación-de-models-en-logisticsmodelspy-ejercicio-12)
7. [Estructura Persistente y Migraciones SQLite (Ejercicio 13)](#7-estructura-persistente-y-migraciones-sqlite-ejercicio-13)
8. [Implementación de CREATE con Django Forms (Ejercicio 14)](#8-implementación-de-create-con-django-forms-ejercicio-14)
9. [Implementación de READ con QuerySets y Templates (Ejercicio 15)](#9-implementación-de-read-con-querysets-y-templates-ejercicio-15)
10. [Implementación de UPDATE con Validación de Integridad (Ejercicio 16)](#10-implementación-de-update-con-validación-de-integridad-ejercicio-16)
11. [Implementación de DELETE con Confirmación Segura (Ejercicio 17)](#11-implementación-de-delete-con-confirmación-segura-ejercicio-17)
12. [Cuadro Mapeo ORM a Sentencias SQL Relacionales](#12-cuadro-mapeo-orm-a-sentencias-sql-relacionales)
13. [Verificación de Entidades Relacionadas (Ejercicio 18)](#13-verificación-de-entidades-relacionadas-ejercicio-18)
14. [Verificación del CRUD Completo en Todas las Entidades (Ejercicio 19)](#14-verificación-del-crud-completo-en-todas-las-entidades-ejercicio-19)
15. [Documentación del Flujo Completo de las Cuatro Operaciones CRUD (Ejercicio 20)](#15-documentación-del-flujo-completo-de-las-cuatro-operaciones-crud-ejercicio-20)
16. [Conclusiones Técnicas](#conclusiones-técnicas)

---

## 1. Investigación de la Problemática Real (Ejercicio 7)

### Problemática actual dentro de la tienda digital:
Tras el crecimiento del catálogo público de **Urban Trend**, la empresa requiere un sistema interno para coordinar el abastecimiento de inventario, la distribución a puntos de venta físicos y el control de insumos de confección. La falta de un sistema centralizado provoca desabastecimiento imprevisto, falta de trazabilidad en los despachos y descontrol de la recepción de materias primas textiles.

### Entidades involucradas:
- **Jefe de almacén:** Controla la recepción de insumos textiles y supervisa los niveles de stock.
- **Coordinador de Logística y Despacho:** Gestiona los convenios con transportistas y programa los envíos a las diferentes sucursales.
- **Administrador de Compras:** Mantiene la cartera de proveedores homologados y fiscaliza los costos unitarios de adquisición.

### Procesos a mejorar:
Centralización y automatización del registro de proveedores, sedes físicas de entrega, flotas de transporte y catalogación estandarizada de materiales textiles clasificados por familias de producto.

---

## 2. Definición de Requisitos Funcionales (Ejercicio 8)

1. **RF01 - Registro de Proveedores:** El usuario puede registrar nuevas empresas proveedoras en el sistema ingresando su número de RUC, razón social, persona de contacto, teléfono y correo electrónico corporativo.
2. **RF02 - Consulta de Directorio:** El usuario puede consultar una lista completa de todos los proveedores registrados para verificar de forma rápida su información de contacto.
3. **RF03 - Modificación de Proveedores:** El usuario puede editar la razón social o actualizar los datos de contacto de cualquier proveedor almacenado.
4. **RF04 - Baja de Proveedores:** El usuario puede eliminar del sistema el registro de un proveedor que haya concluido su relación comercial con la empresa.
5. **RF05 - Gestión de Sucursales:** El usuario puede registrar y consultar las distintas sucursales físicas o puntos de venta, indicando su código de sede, nombre comercial, dirección, ciudad y volumen máximo de almacenamiento.
6. **RF06 - Operatividad de Sedes:** El usuario puede actualizar los datos operativos de una sucursal existente o eliminarla en caso de cierre definitivo.
7. **RF07 - Control de Flota Logística:** El usuario puede dar de alta y administrar las unidades de transporte logístico asignadas a las entregas, especificando la empresa transportista, número de placa, tipo de vehículo y disponibilidad de servicio.
8. **RF08 - Catalogación de Familias Textiles:** El usuario puede crear y listar categorías maestras de insumos textiles mediante un nombre descriptivo y un prefijo técnico para clasificar los materiales.
9. **RF09 - Registro de Insumos Relacionados:** El usuario puede registrar un nuevo material textil asociado obligatoriamente a una de las categorías existentes, ingresando su nombre técnico, unidad de medida, costo por unidad y stock inicial.
10. **RF10 - Supervisión de Existencias:** El usuario puede consultar el catálogo general de materiales en almacén para supervisar las existencias y la categoría a la que pertenece cada ítem.
11. **RF11 - Actualización de Costos y Stock:** El usuario puede modificar el costo unitario, las existencias registradas o la categoría vinculada a cualquier material.
12. **RF12 - Eliminación Segura de Materiales:** El usuario puede eliminar un material textil del catálogo cuando quede descontinuado, mediante una confirmación previa en pantalla con método POST para evitar borrados accidentales.

---

## 3. Diseño del Modelo de Datos (Ejercicio 9)

El diseño comprende **cinco entidades**: tres entidades independientes y dos vinculadas mediante clave foránea (1:N).

### Tabla de Entidad: `Proveedor` (Independiente)
| Campo | Tipo de Dato | PK | FK | Obligatorio | Restricciones / Reglas |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `id` | BigAutoField | SI | NO | SI | Clave primaria autoincremental. |
| `ruc` | CharField(max_length=11) | NO | NO | SI | `unique=True`, exactamente 11 dígitos fiscales numéricos. |
| `razon_social` | CharField(max_length=120) | NO | NO | SI | Nombre legal completo de la compañía proveedora. |
| `telefono` | CharField(max_length=15) | NO | NO | SI | Teléfono móvil o fijo de contacto comercial. |
| `correo` | EmailField() | NO | NO | SI | Formato estándar de correo electrónico corporativo. |

*Justificación:* Desacopla y centraliza el directorio de empresas socias que abastecen materias primas, asegurando que los datos de contacto no se dupliquen ni dependan de otras entidades del sistema.

### Tabla de Entidad: `Sucursal` (Independiente)
| Campo | Tipo de Dato | PK | FK | Obligatorio | Restricciones / Reglas |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `id` | BigAutoField | SI | NO | SI | Clave primaria autoincremental. |
| `nombre` | CharField(max_length=80) | NO | NO | SI | Denominación del local o almacén físico. |
| `direccion` | CharField(max_length=150) | NO | NO | SI | Ubicación física exacta y punto de descarga. |
| `ciudad` | CharField(max_length=50) | NO | NO | SI | Jurisdicción operativa y logística. |
| `capacidad_almacen` | PositiveIntegerField() | NO | NO | SI | Volumen en unidades; valor entero $\ge 0$. |

*Justificación:* Permite gestionar sedes y almacenes físicos receptores de mercadería sin depender de la lógica de distribución ni de otras entidades.

### Tabla de Entidad: `Transportista` (Independiente)
| Campo | Tipo de Dato | PK | FK | Obligatorio | Restricciones / Reglas |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `id` | BigAutoField | SI | NO | SI | Clave primaria autoincremental. |
| `empresa` | CharField(max_length=100) | NO | NO | SI | Razón social de la empresa de transporte tercerizada. |
| `placa` | CharField(max_length=10) | NO | NO | SI | Placa vehicular única (`unique=True`). |
| `tipo_vehiculo` | CharField(max_length=30) | NO | NO | SI | Clasificación: Camión, Furgón o Moto Carga. |
| `activo` | BooleanField(default=True) | NO | NO | SI | Disponibilidad operativa del servicio. |

*Justificación:* Controla las unidades de traslado de forma autónoma, permitiendo dar de alta o baja operadores logísticos sin afectar la información de los materiales transportados.

### Tabla de Entidad: `CategoriaInsumo` (Relacionada - Lado 1)
| Campo | Tipo de Dato | PK | FK | Obligatorio | Restricciones / Reglas |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `id` | BigAutoField | SI | NO | SI | Clave primaria autoincremental. |
| `nombre` | CharField(max_length=60) | NO | NO | SI | Denominación única (`unique=True`). |
| `descripcion` | TextField(blank=True) | NO | NO | NO | Detalle técnico de la categoría textil. |

*Justificación:* Estandariza las familias de insumos (telas, avíos, hilos, empaque), previniendo redundancias y errores de digitación antes de la asignación de materiales.

### Tabla de Entidad: `Material` (Relacionada - Lado N)
| Campo | Tipo de Dato | PK | FK | Obligatorio | Restricciones / Reglas |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `id` | BigAutoField | SI | NO | SI | Clave primaria autoincremental. |
| `categoria_id` | ForeignKey(CategoriaInsumo) | NO | SI | SI | Clave foránea con regla `on_delete=models.CASCADE` y `related_name='materiales'`. |
| `nombre` | CharField(max_length=100) | NO | NO | SI | Nombre descriptivo del insumo textil. |
| `unidad_medida` | CharField(max_length=20) | NO | NO | SI | Métrica de inventario: Metros, Conos, Piezas, Rollos, Millares. |
| `precio_unitario` | DecimalField(max_digits=8, decimal_places=2) | NO | NO | SI | Precisión monetaria exacta en Soles (S/). |
| `stock` | PositiveIntegerField(default=0) | NO | NO | SI | Cantidad física en almacén; valor $\ge 0$. |

*Justificación:* Representa físicamente los insumos de corte y confección. Su relación 1:N con `CategoriaInsumo` garantiza la integridad referencial y evita la existencia de materiales huérfanos sin clasificación.

---

## 4. Representación de Relaciones ER (Ejercicio 10)

```
┌───────────────────────────┐         ┌───────────────────────────┐
│      CategoriaInsumo      │         │         Proveedor         │
│ ───────────────────────── │         │ ───────────────────────── │
│  PK  id                   │         │  PK  id                   │
│      nombre (UQ)          │         │      ruc (UQ)             │
│      descripcion          │         │      razon_social         │
└─────────────┬─────────────┘         │      telefono             │
              │ 1                     │      correo               │
              │                       └───────────────────────────┘
              │                       ┌───────────────────────────┐
              │ N                     │         Sucursal          │
┌─────────────▼─────────────┐         │ ───────────────────────── │
│         Material          │         │  PK  id                   │
│ ───────────────────────── │         │      nombre               │
│  PK  id                   │         │      direccion            │
│  FK  categoria_id ────────┘         │      ciudad               │
│      nombre                         │      capacidad_almacen    │
│      unidad_medida                  └───────────────────────────┘
│      precio_unitario                ┌───────────────────────────┐
│      stock                          │       Transportista       │
└───────────────────────────┘         │ ───────────────────────── │
                                      │  PK  id                   │
                                      │      empresa              │
                                      │      placa (UQ)           │
                                      │      tipo_vehiculo        │
                                      │      activo               │
                                      └───────────────────────────┘
```

---

## 5. Creación y Configuración de la App `logistics` (Ejercicio 11)

### Creación mediante CLI:
```bash
python manage.py startapp logistics
```

### Inclusión en `src/config/settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'store',
    'logistics',  # <-- Registrada exitosamente
]
```

### Inclusión en `src/config/urls.py`:
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('ropa/', include('store.urls')),
    path('logistics/', include('logistics.urls')),  # <-- Espacio de rutas modular
]
```

---

## 6. Implementación de Models en `logistics/models.py` (Ejercicio 12)

El archivo `src/logistics/models.py` implementa rigurosamente el diseño propuesto:

```python
from django.db import models

# 1. ENTIDADES INDEPENDIENTES

class Proveedor(models.Model):
    ruc = models.CharField(max_length=11, unique=True, verbose_name="RUC")
    razon_social = models.CharField(max_length=120, verbose_name="Razón Social")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    correo = models.EmailField(verbose_name="Correo Electrónico")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['razon_social']

    def __str__(self):
        return f"{self.razon_social} ({self.ruc})"


class Sucursal(models.Model):
    nombre = models.CharField(max_length=80, verbose_name="Nombre de Sede")
    direccion = models.CharField(max_length=150, verbose_name="Dirección")
    ciudad = models.CharField(max_length=50, verbose_name="Ciudad")
    capacidad_almacen = models.PositiveIntegerField(verbose_name="Capacidad de Almacén (unidades)")

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"


class Transportista(models.Model):
    empresa = models.CharField(max_length=100, verbose_name="Empresa de Transporte")
    placa = models.CharField(max_length=10, unique=True, verbose_name="Número de Placa")
    tipo_vehiculo = models.CharField(max_length=30, verbose_name="Tipo de Vehículo")
    activo = models.BooleanField(default=True, verbose_name="Operativo / Activo")

    class Meta:
        verbose_name = "Transportista"
        verbose_name_plural = "Transportistas"
        ordering = ['empresa']

    def __str__(self):
        return f"{self.empresa} [{self.placa}]"


# 2. ENTIDADES RELACIONADAS (1:N)

class CategoriaInsumo(models.Model):
    nombre = models.CharField(max_length=60, unique=True, verbose_name="Nombre de Categoría")
    descripcion = models.TextField(blank=True, verbose_name="Descripción Técnica")

    class Meta:
        verbose_name = "Categoría de Insumo"
        verbose_name_plural = "Categorías de Insumos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Material(models.Model):
    categoria = models.ForeignKey(
        CategoriaInsumo,
        on_delete=models.CASCADE,
        related_name='materiales',
        verbose_name="Categoría Asignada"
    )
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Insumo")
    unidad_medida = models.CharField(max_length=20, verbose_name="Unidad de Medida")
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Precio Unitario (S/)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock en Almacén")

    class Meta:
        verbose_name = "Material / Insumo"
        verbose_name_plural = "Materiales / Insumos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.categoria.nombre})"
```

---

## 7. Estructura Persistente y Migraciones SQLite (Ejercicio 13)

### Ejecución de migraciones:
1. `python manage.py makemigrations logistics`
   - Salida:
     ```text
     Migrations for 'logistics':
       src\logistics\migrations\0001_initial.py
         + Create model CategoriaInsumo
         + Create model Proveedor
         + Create model Sucursal
         + Create model Transportista
         + Create model Material
     ```
2. `python manage.py migrate`
   - Salida:
     ```text
     Operations to perform:
       Apply all migrations: admin, auth, contenttypes, core, logistics, sessions, store
     Running migrations:
       Applying logistics.0001_initial... OK
     ```
3. `python manage.py showmigrations logistics`
   - Salida:
     ```text
     logistics
      [X] 0001_initial
     ```

---

## 8. Implementación de CREATE con Django Forms (Ejercicio 14)

Se diseñó `src/logistics/forms.py` empleando `ModelForm` y validadores específicos:
- `clean_ruc()`: Valida que el RUC sea estrictamente numérico y cuente con exactamente 11 dígitos.
- `clean_placa()`: Convierte los caracteres a mayúsculas con `.strip().upper()`.
- `clean_precio_unitario()`: Asegura que el costo unitario sea estrictamente mayor a cero (`precio > 0`).

### Código en `src/logistics/forms.py`:
```python
from django import forms
from .models import Proveedor, Sucursal, Transportista, CategoriaInsumo, Material


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['ruc', 'razon_social', 'telefono', 'correo']
        widgets = {
            'ruc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 20123456789'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Textiles del Sur S.A.C.'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 987654321'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contacto@textiles.com'}),
        }

    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        if ruc:
            ruc = ruc.strip()
            if not ruc.isdigit():
                raise forms.ValidationError("El RUC debe contener únicamente dígitos numéricos.")
            if len(ruc) != 11:
                raise forms.ValidationError("El RUC debe contener exactamente 11 dígitos numéricos.")
        return ruc


class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'direccion', 'ciudad', 'capacidad_almacen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Almacén Central Lima'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Av. Argentina 1234'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Lima'}),
            'capacidad_almacen': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class TransportistaForm(forms.ModelForm):
    class Meta:
        model = Transportista
        fields = ['empresa', 'placa', 'tipo_vehiculo', 'activo']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Express Cargo SAC'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. ABC-123'}),
            'tipo_vehiculo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Camión 5TN'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        if placa:
            return placa.strip().upper()
        return placa


class CategoriaInsumoForm(forms.ModelForm):
    class Meta:
        model = CategoriaInsumo
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Telas e Hilados'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción técnica...'}),
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['categoria', 'nombre', 'unidad_medida', 'precio_unitario', 'stock']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Tela Algodón Pima 50/1'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Metros / Conos / Rollos'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

    def clean_precio_unitario(self):
        precio = self.cleaned_data.get('precio_unitario')
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio unitario debe ser mayor a cero.")
        return precio
```

---

## 9. Implementación de READ con QuerySets y Templates (Ejercicio 15)

Se implementó el Dashboard estadístico y las vistas de consulta utilizando métodos de persistencia optimizados:
- `Material.objects.select_related('categoria').all()`: Realiza un INNER JOIN SQL para recuperar en una sola consulta el material y su categoría asociada, mitigando el problema del $N+1$.
- `Proveedor.objects.all()` y `CategoriaInsumo.objects.all()`.
- Conteo eficiente mediante `.count()` que ejecuta `SELECT COUNT(*)`.

---

## 10. Implementación de UPDATE con Validación de Integridad (Ejercicio 16)

Para la actualización se utilizó `get_object_or_404(Material, pk=pk)`, inicializando el formulario con `instance=material`. Si la petición es POST y los datos son válidos, `form.save()` actualiza únicamente los campos modificados ejecutando una instrucción SQL `UPDATE`:

```python
def material_update(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, "Material actualizado correctamente.")
            return redirect('logistics:material_list')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'logistics/material_form.html', {'form': form, 'titulo': 'Editar Insumo / Material'})
```

---

## 11. Implementación de DELETE con Confirmación Segura (Ejercicio 17)

Para garantizar la seguridad de los datos contra borrados accidentales:
1. Las solicitudes GET renderizan una plantilla de confirmación (`material_confirm_delete.html`) que especifica el impacto de la acción.
2. La eliminación se procesa exclusivamente mediante petición POST que invoca `.delete()` sobre el ORM, ejecutando la sentencia SQL `DELETE FROM logistics_material WHERE id = ?`.

```python
def material_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        messages.warning(request, f'El material "{material.nombre}" fue eliminado.')
        return redirect('logistics:material_list')
    return render(request, 'logistics/material_confirm_delete.html', {'objeto': material})
```

---

## 12. Cuadro Mapeo ORM a Sentencias SQL Relacionales

| Operación Django ORM | Operación SQL Conceptual | Ejemplo de Sentencia Generada en SQLite |
| :--- | :---: | :--- |
| `Material.objects.all()` | `SELECT` | `SELECT id, categoria_id, nombre, unidad_medida, precio_unitario, stock FROM logistics_material;` |
| `Material.objects.select_related('categoria').all()` | `SELECT` con `INNER JOIN` | `SELECT m.id, m.nombre, c.nombre FROM logistics_material m INNER JOIN logistics_categoriainsumo c ON (m.categoria_id = c.id);` |
| `get_object_or_404(Material, pk=pk)` | `SELECT` con límite | `SELECT * FROM logistics_material WHERE id = ? LIMIT 1;` |
| `form.save()` (Nuevo registro) | `INSERT` | `INSERT INTO logistics_material (categoria_id, nombre, unidad_medida, precio_unitario, stock) VALUES (?, ?, ?, ?, ?);` |
| `form.save()` (Con instancia) | `UPDATE` | `UPDATE logistics_material SET precio_unitario = ?, stock = ? WHERE id = ?;` |
| `material.delete()` | `DELETE` | `DELETE FROM logistics_material WHERE id = ?;` |
| `Proveedor.objects.count()` | `SELECT COUNT(*)` | `SELECT COUNT(*) AS "__count" FROM logistics_proveedor;` |
| `Transportista.objects.filter(activo=True)` | `SELECT` con `WHERE` | `SELECT * FROM logistics_transportista WHERE activo = 1;` |

---

## 13. Verificación de Entidades Relacionadas (Ejercicio 18)

Para demostrar que la relación 1:N entre `CategoriaInsumo` y `Material` opera de forma estricta y transparente entre Python y SQLite, se ejecutó un protocolo de pruebas con el script `src/verificar_ejercicio18.py`.

### 1. Comprobación de la Clave Foránea en SQLite
Mediante `python manage.py sqlmigrate logistics 0001` y la consulta de metadatos del motor (`PRAGMA foreign_key_list(logistics_material);`), se certificó la estructura física generada en la base de datos:

```sql
CREATE TABLE "logistics_material" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "nombre" varchar(100) NOT NULL,
    "unidad_medida" varchar(20) NOT NULL,
    "precio_unitario" decimal NOT NULL,
    "stock" integer unsigned NOT NULL CHECK ("stock" >= 0),
    "categoria_id" bigint NOT NULL REFERENCES "logistics_categoriainsumo" ("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX "logistics_material_categoria_id_20d6a116" ON "logistics_material" ("categoria_id");
```

**Análisis técnico:**
- Django ORM generó automáticamente la columna `"categoria_id"` vinculada como clave foránea a `"logistics_categoriainsumo" ("id")`.
- Generó un índice B-Tree dedicado sobre `"categoria_id"` (`CREATE INDEX`) para optimizar el rendimiento de las cláusulas `JOIN` y filtros relacionales.

### 2. Registro de Datos Asociados (CREATE -> INSERT)
Se persistió una categoría maestra junto con dos insumos hijos asociados:
```python
cat_demo = CategoriaInsumo.objects.create(
    nombre="Cierres y Metales de Prueba",
    descripcion="Categoría para prueba técnica de relaciones 1:N."
)
mat1 = Material.objects.create(
    nombre="Cierre Metal Dorado 15cm",
    categoria=cat_demo,
    unidad_medida="Piezas",
    precio_unitario=Decimal("2.50"),
    stock=300
)
mat2 = Material.objects.create(
    nombre="Deslizador Niquelado N°5",
    categoria=cat_demo,
    unidad_medida="Docenas",
    precio_unitario=Decimal("4.20"),
    stock=150
)
```
- Resultado: Ambos registros fueron persistidos asignando internamente `categoria_id = 5` en SQLite.

### 3. Consulta Directa e Inversa de Registros Relacionados (READ -> SELECT)
- **Consulta Directa (Hijo -> Padre):**
  ```python
  material = Material.objects.get(id=mat1.id)
  print(material.categoria_id)       # 5 (FK en SQLite)
  print(material.categoria.nombre)   # 'Cierres y Metales de Prueba'
  ```
- **Consulta Inversa (Padre -> Hijos con `related_name='materiales'`):**
  ```python
  print(cat_demo.materiales.count()) # 2
  for m in cat_demo.materiales.all():
      print(m.nombre, m.stock, m.precio_unitario)
  ```
- **Consulta Optimizada con `select_related('categoria')`:**
  Ejecuta una sola consulta relacional combinada utilizando `INNER JOIN`:
  ```sql
  SELECT "logistics_material"."id", "logistics_material"."categoria_id", "logistics_material"."nombre",
         "logistics_material"."unidad_medida", "logistics_material"."precio_unitario", "logistics_material"."stock",
         "logistics_categoriainsumo"."id", "logistics_categoriainsumo"."nombre", "logistics_categoriainsumo"."descripcion"
  FROM "logistics_material"
  INNER JOIN "logistics_categoriainsumo" ON ("logistics_material"."categoria_id" = "logistics_categoriainsumo"."id")
  WHERE "logistics_material"."categoria_id" = 5
  ORDER BY "logistics_material"."nombre" ASC;
  ```

### 4. Verificación de Integridad y Eliminación en Cascada (`CASCADE`)
Se creó una categoría temporal y un material hijo; al ejecutar `cat_temp.delete()`, Django ORM y SQLite borraron en cascada el material dependiente, demostrando que no pueden existir registros huérfanos sin categoría contenedora.

---

## 14. Verificación del CRUD Completo en Todas las Entidades (Ejercicio 19)

Se diseñó e implementó el script `src/verificar_ejercicio19.py` para demostrar empíricamente el ciclo completo de vida de los datos (`CREATE`, `READ`, `UPDATE`, `DELETE`) en las 5 entidades implementadas (`CategoriaInsumo`, `Material`, `Proveedor`, `Sucursal`, `Transportista`), utilizando exclusivamente Django ORM y persistencia en SQLite, sin redactar sentencias SQL manuales.

### Matriz de Operaciones CRUD por Entidad

| Entidad | CREATE $\to$ INSERT | READ $\to$ SELECT | UPDATE $\to$ UPDATE | DELETE $\to$ DELETE |
| :--- | :--- | :--- | :--- | :--- |
| **`CategoriaInsumo`** | `CategoriaInsumo.objects.create(nombre=...)` | `CategoriaInsumo.objects.get(id=...)` | `cat.nombre = ...; cat.save()` | `cat.delete()` |
| **`Material`** | `Material.objects.create(categoria=..., ...)` | `Material.objects.select_related().get(...)` | `mat.precio_unitario = ...; mat.save()` | `mat.delete()` |
| **`Proveedor`** | `Proveedor.objects.create(ruc=..., ...)` | `Proveedor.objects.get(id=...)` | `prov.telefono = ...; prov.save()` | `prov.delete()` |
| **`Sucursal`** | `Sucursal.objects.create(nombre=..., ...)` | `Sucursal.objects.get(id=...)` | `suc.capacidad = ...; suc.save()` | `suc.delete()` |
| **`Transportista`** | `Transportista.objects.create(empresa=..., ...)`| `Transportista.objects.get(id=...)` | `trans.activo = False; trans.save()` | `trans.delete()` |

### Evidencia de Ejecución Consolidada
Todas las operaciones concluyeron con verificación de estado (`.exists() == False` tras la eliminación), confirmando la atomicidad y persistencia transaccional del ORM.

---

## 15. Documentación del Flujo Completo de las Cuatro Operaciones CRUD (Ejercicio 20)

Para documentar el recorrido integral extremo a extremo se seleccionó la entidad **`Material`** (Insumo Textil), al ser la entidad central del módulo de abastecimiento que incorpora validaciones de formulario, relación relacional 1:N mediante clave foránea, optimización de consultas y ciclo completo de persistencia.

A continuación se detalla el recorrido técnico de las cuatro operaciones:
$$\text{Navegador} \to \text{URL} \to \text{View} \to \text{Model} \to \text{Django ORM} \to \text{SQLite} \to \text{redirect / render} \to \text{Template} \to \text{Navegador}$$

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                RECORRIDO DEL FLUJO COMPLETO EN DJANGO MVT                              │
│                                                                                                        │
│  [1. Navegador] ──(Request GET/POST)──> [2. URL Enrutador] ──(Delega)──> [3. View Controlador]         │
│                                                                                   │                    │
│  [9. Navegador] <──(HTML / 302)─────── [7. Response / Context] <─────────── [4. Model / Form]         │
│         ▲                                         ▲                               │                    │
│         │                                         │                               ▼                    │
│  [8. Template HTML] <──(Renderiza)────────────────┴────────────────────── [5. Django ORM]             │
│                                                                                   │ (Genera SQL)       │
│                                                                                   ▼                    │
│                                                                            [6. Motor SQLite]           │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Flujo 1: Operación READ (Consulta del Catálogo de Insumos)

1. **Navegador:** El usuario solicita la URL `http://127.0.0.1:8000/logistics/materiales/` mediante una petición `GET`.
2. **URL:** El archivo `config/urls.py` deriva el prefijo `logistics/` hacia `logistics/urls.py`, resolviendo la ruta `path('materiales/', views.material_list, name='material_list')`.
3. **View:** Se ejecuta la función `material_list(request)`.
4. **Model:** Invoca a la entidad `Material`.
5. **Django ORM:** Se ejecuta la instrucción relacional optimizada:
   ```python
   materiales = Material.objects.select_related('categoria').all()
   ```
6. **SQLite:** El motor SQLite procesa la sentencia generada con `INNER JOIN`:
   ```sql
   SELECT "logistics_material"."id", "logistics_material"."nombre", "logistics_material"."stock",
          "logistics_material"."precio_unitario", "logistics_categoriainsumo"."nombre"
   FROM "logistics_material"
   INNER JOIN "logistics_categoriainsumo" 
           ON ("logistics_material"."categoria_id" = "logistics_categoriainsumo"."id");
   ```
7. **View & Context:** La vista recibe el QuerySet con los registros y empaqueta el contexto:
   `contexto = {'materiales': materiales}`.
8. **Template:** Django evalúa `logistics/material_list.html`, iterando sobre la colección `{% for m in materiales %}` e inyectando las propiedades de cada insumo y su categoría foránea.
9. **Navegador:** Se retorna una respuesta `HttpResponse` con código **200 OK**, mostrando la tabla visual interactiva.

---

### Flujo 2: Operación CREATE (Registro de Nuevo Insumo)

1. **Navegador:** El usuario completa el formulario en `/logistics/materiales/nuevo/` y presiona el botón "Guardar Registro", emitiendo una petición HTTP `POST` con los datos cargados y el token CSRF.
2. **URL:** `logistics/urls.py` reconoce el patrón `path('materiales/nuevo/', views.material_create, name='material_create')`.
3. **View:** Se invoca `material_create(request)` detectando `request.method == 'POST'`.
4. **Model & Form:** Se instancia `MaterialForm(request.POST)`. Se ejecuta `form.is_valid()`, activando la sanitización de tipos y el validador personalizado `clean_precio_unitario()`.
5. **Django ORM:** Tras la validación, se ejecuta `form.save()`, generando la instrucción SQL de inserción atómica.
6. **SQLite:** El motor ejecuta la sentencia:
   ```sql
   INSERT INTO "logistics_material" ("categoria_id", "nombre", "unidad_medida", "precio_unitario", "stock")
   VALUES (1, 'Tela Rib 2x1 Negro', 'Metros', 22.50, 180);
   ```
   SQLite asigna un identificador primario autoincremental `id` y persiste los datos en disco.
7. **redirect / Pattern PRG:** Para evitar duplicación de registros al refrescar el navegador, la vista encola una notificación con `messages.success(request, "Material registrado exitosamente.")` y retorna:
   ```python
   return redirect('logistics:material_list')
   ```
8. **Template:** No se renderiza una plantilla de forma directa; el servidor emite una respuesta `HttpResponseRedirect` con código **302 Found**.
9. **Navegador:** El navegador recibe la redirección y ejecuta automáticamente una petición `GET /logistics/materiales/`, mostrando el listado con el nuevo registro insertado y la alerta de éxito.

---

### Flujo 3: Operación UPDATE (Modificación de Insumo Existente)

1. **Navegador:** El usuario presiona el botón "Editar" de un insumo específico (ej. ID 9), emitiendo una petición `GET /logistics/materiales/editar/9/`.
2. **URL:** El enrutador captura el parámetro numérico a través del convertidor de rutas: `path('materiales/editar/<int:pk>/', views.material_update)`.
3. **View:** Se ejecuta `material_update(request, pk=9)`.
4. **Model & ORM (Fase de Carga):** Se obtiene la instancia mediante `get_object_or_404(Material, pk=pk)`, ejecutando en SQLite `SELECT * FROM logistics_material WHERE id = 9 LIMIT 1;`. Se instancia `MaterialForm(instance=material)` precargando los valores existentes en la plantilla.
5. **Navegador (Envío de Cambios):** El usuario altera el stock o costo unitario y presiona "Guardar Registro" enviando una solicitud `POST`.
6. **View (Fase de Guardado):** La vista enlaza los datos con la instancia existente: `form = MaterialForm(request.POST, instance=material)`.
7. **Django ORM:** Tras validar el formulario (`form.is_valid()`), `form.save()` detecta la existencia de la clave primaria `id=9`.
8. **SQLite:** El motor ejecuta una sentencia SQL de actualización:
   ```sql
   UPDATE "logistics_material"
   SET "precio_unitario" = 24.50, "stock" = 250
   WHERE "id" = 9;
   ```
9. **redirect / Navegador:** La vista añade `messages.success(request, "Material actualizado correctamente.")` y redirige con código **302** al listado, donde el navegador refleja los valores persistidos.

---

### Flujo 4: Operación DELETE (Eliminación Segura con Confirmación)

1. **Navegador (Solicitud Inicial):** El usuario presiona el botón "Eliminar" en la fila correspondiente al registro ID 9 (`GET /logistics/materiales/eliminar/9/`).
2. **URL:** Resuelve la ruta `path('materiales/eliminar/<int:pk>/', views.material_delete)`.
3. **View:** Se ejecuta `material_delete(request, pk=9)`, recuperando el registro con `get_object_or_404(Material, pk=pk)`.
4. **Template:** Como el método HTTP es `GET`, se renderiza la plantilla `logistics/material_confirm_delete.html` mostrando la advertencia de eliminación y el detalle del objeto.
5. **Navegador (Confirmación):** El usuario presiona "Sí, Eliminar Registro", enviando un formulario con método `POST` y token de seguridad CSRF.
6. **View:** La función comprueba `if request.method == 'POST':`.
7. **Model & Django ORM:** Se ejecuta la instrucción de eliminación:
   ```python
   material.delete()
   ```
8. **SQLite:** El motor relacional ejecuta físicamente la sentencia SQL:
   ```sql
   DELETE FROM "logistics_material" WHERE "id" = 9;
   ```
9. **redirect / Navegador:** La vista encola un mensaje `messages.warning(request, f'El material "{material.nombre}" fue eliminado.')` y devuelve `redirect('logistics:material_list')`. El navegador carga el listado actualizado sin el elemento eliminado y con la alerta de confirmación.

---

## Conclusiones Técnicas

1. **Persistencia Transaccional vs. Memoria Volátil:** Se completó exitosamente la transición de estructuras volátiles en RAM a un esquema persistente con SQLite, garantizando la durabilidad (ACID) de los registros ante reinicios del servidor.
2. **Integridad Referencial en SQLite:** La configuración de relaciones 1:N entre `CategoriaInsumo` y `Material` con `on_delete=models.CASCADE` previene registros inconsistentes en la base de datos.
3. **Eficiencia en Consultas con `select_related`:** La optimización de lectura evita sobrecargar el motor de base de datos con múltiples consultas individuales al momento de renderizar relaciones foráneas en los templates.
4. **Validación Declarativa con ModelForms:** Centralizar las validaciones de tipo, longitud y formato en la capa intermedia protege el sistema contra datos maliciosos o corruptos antes de llegar a la capa relacional.
5. **Arquitectura MVT y Patrón PRG:** La separación clara de responsabilidades entre URLs, Views, Models y Templates, complementada con el patrón Post/Redirect/Get, asegura una navegación robusta y previene reenvíos accidentales de datos en el servidor.



