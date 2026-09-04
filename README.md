# Laboratorio 03 — Implementación de ORM y Memoria Persistente

**Curso:** Desarrollo de Aplicaciones Empresariales  
**Institución:** Tecsup  
**Sección:** 4 - C24 - Sección CD  
**Docente:** Yunior Bestard Aroche  
**Integrantes:**
1. **Erick Arturo Gamarra Mundaca**
2. **Jesús Enrique Rocha Bobadilla**  
**Proyecto:** **UrbanTrend** — Catálogo de Moda Streetwear y Sistema de Abastecimiento Logístico

---

## 🏬 1. Problemática Investigada (Ejercicio 7)

Tras el sostenido crecimiento del catálogo público de **Urban Trend**, la empresa identificó serios cuellos de botella en sus operaciones internas. La falta de un sistema centralizado para gestionar el abastecimiento de materia prima textil, la cartera de proveedores, las sedes físicas y las flotas de transporte provocaba:

* **Desabastecimiento imprevisto:** Quiebres de stock en insumos críticos (telas, hilados, cierres) deteniendo la confección.
* **Falta de trazabilidad:** Carencia de registros unificados sobre transportistas y unidades asignadas a los despachos entre almacenes y sucursales.
* **Descontrol de proveedores:** Pérdida de cotizaciones históricas y datos de contacto de socios homologados.

### Actores del Sistema:
* **Jefe de Almacén:** Controla la recepción de insumos textiles, supervisa stock físico y fiscaliza existencias.
* **Coordinador de Logística y Despacho:** Gestiona convenios con transportistas y programa traslados a sucursales.
* **Administrador de Compras:** Administra el directorio de proveedores homologados y fiscaliza los costos unitarios de adquisición.

---

## 📋 2. Requisitos Funcionales (Ejercicio 8)

* **RF01:** Registrar empresas proveedoras en el sistema con RUC (11 dígitos), razón social, contacto, teléfono y correo electrónico.
* **RF02:** Consultar el directorio completo de proveedores registrados con sus datos de contacto.
* **RF03:** Actualizar o editar la información fiscal y comercial de cualquier proveedor almacenado.
* **RF04:** Eliminar el registro de proveedores que hayan concluido su relación comercial.
* **RF05:** Registrar y consultar sucursales físicas y puntos de venta indicando dirección, ciudad y capacidad máxima de almacenamiento.
* **RF06:** Modificar datos operativos de sucursales o eliminarlas en caso de cierre definitivo.
* **RF07:** Dar de alta y administrar unidades de transporte logístico (empresa, placa única, tipo de vehículo y disponibilidad operativa).
* **RF08:** Crear y listar categorías maestras de insumos textiles mediante nombre único y descripción técnica.
* **RF09:** Registrar nuevos materiales textiles vinculados obligatoriamente a una de las categorías existentes (relación 1:N), indicando nombre, unidad de medida, costo unitario y stock inicial.
* **RF10:** Consultar el catálogo general de insumos textiles en almacén visualizando la categoría a la que pertenece cada ítem.
* **RF11:** Modificar costos unitarios, existencias en almacén o categoría asignada a cualquier material.
* **RF12:** Eliminar insumos textiles descontinuados mediante confirmación previa en pantalla para evitar borrados accidentales.

---

## 🏗️ 3. Arquitectura y Aplicación Creada (`logistics`)

La nueva aplicación empresarial **`logistics`** se integró en el proyecto Django bajo el patrón MVT:

### 3.1 Modelo de Datos (5 Entidades Implementadas)
1. **`CategoriaInsumo` (Entidad Maestra - Lado 1):** Clasificación estandarizada de familias de insumos (`nombre` único, `descripcion`).
2. **`Material` (Entidad Dependiente - Lado N):** Insumos físicos vinculados a categoría mediante clave foránea con regla `on_delete=models.CASCADE` y `related_name='materiales'`.
3. **`Proveedor` (Entidad Independiente):** Directorio de empresas socias (`ruc` único de 11 dígitos, `razon_social`, `telefono`, `correo`).
4. **`Sucursal` (Entidad Independiente):** Sedes físicas receptoras (`nombre`, `direccion`, `ciudad`, `capacidad_almacen`).
5. **`Transportista` (Entidad Independiente):** Unidades logísticas de traslado (`empresa`, `placa` única, `tipo_vehiculo`, `activo`).

### 3.2 Relación Entidad-Relación (1:N)
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

### 3.3 Formularios y Validaciones (`forms.py`)
* `clean_ruc()`: Valida que el RUC sea estrictamente numérico y contenga 11 caracteres.
* `clean_placa()`: Convierte automáticamente a mayúsculas con `.strip().upper()`.
* `clean_precio_unitario()`: Valida que el costo monetario sea estrictamente mayor a cero.

### 3.4 Vistas y Ciclo CRUD Completo (`views.py`)
* **Dashboard (`index_logistics`):** Métricas agregadas con `.count()` y tabla de insumos recientes.
* **READ (Select):** `material_list` optimizado con `select_related('categoria')` (generando SQL `INNER JOIN` para evitar consultas $N+1$).
* **CREATE (Insert):** Vistas con formularios desacoplados y patrón Post/Redirect/Get (PRG).
* **UPDATE (Update):** Recuperación robusta con `get_object_or_404` y enlace mediante `instance`.
* **DELETE (Delete):** Borrado físico en SQLite condicionado a confirmación con método HTTP `POST`.

---

## 🗺️ 4. Mapa de Rutas del Sistema

| Módulo | Endpoint URL | Vista | Descripción |
| :--- | :--- | :--- | :--- |
| **Inicio** | `/` | `core.views.items_list` | Portada institucional UrbanTrend. |
| **Tienda** | `/ropa/` | `store.views.prenda_list` | Catálogo de prendas con filtros ORM. |
| **Tienda** | `/ropa/nueva/` | `store.views.prenda_create` | Registro persistente de prendas. |
| **Logística** | `/logistics/` | `logistics.views.index_logistics` | Panel de control de insumos y métricas. |
| **Logística** | `/logistics/materiales/` | `logistics.views.material_list` | Catálogo general de insumos textiles. |
| **Logística** | `/logistics/materiales/nuevo/` | `logistics.views.material_create` | Formulario de alta de material. |
| **Logística** | `/logistics/materiales/editar/<pk>/` | `logistics.views.material_update` | Edición de costos y existencias. |
| **Logística** | `/logistics/materiales/eliminar/<pk>/` | `logistics.views.material_delete` | Confirmación y borrado permanente. |
| **Logística** | `/logistics/categorias/` | `logistics.views.categoria_list` | Directorio de familias textiles (1:N). |
| **Logística** | `/logistics/categorias/nuevo/` | `logistics.views.categoria_create` | Alta de categoría maestra. |
| **Logística** | `/logistics/proveedores/` | `logistics.views.proveedor_list` | Directorio de proveedores homologados. |
| **Logística** | `/logistics/proveedores/nuevo/` | `logistics.views.proveedor_create` | Registro de proveedores con validación. |

---

## 🧪 5. Verificaciones Técnicas y Pruebas Automatizadas

El proyecto cuenta con scripts de verificación y una suite de pruebas completa:

### Comandos de Verificación:
```powershell
# 1. Comprobación del modelo relacional 1:N (Ejercicio 18)
python src/verificar_ejercicio18.py

# 2. Comprobación del ciclo CRUD completo en las 5 entidades (Ejercicio 19)
python src/verificar_ejercicio19.py

# 3. Suite completa de tests unitarios (29 tests pasando exitosamente)
python src/manage.py test
```

**Resultado de las pruebas:**
```text
Creating test database for alias 'default'...
.............................
----------------------------------------------------------------------
Ran 29 tests in 0.128s

OK
Destroying test database for alias 'default'...
```

---

## ⚙️ 6. Guía de Instalación y Ejecución Local

```powershell
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd Django_Lab03

# 2. Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones sobre SQLite
python src/manage.py migrate

# 5. Poblar datos iniciales
python src/seed_prendas.py
python src/seed_logistics.py

# 6. Iniciar servidor de desarrollo
python src/manage.py runserver
```

Navegar a:  
* Tienda Streetwear: `http://127.0.0.1:8000/ropa/`  
* Módulo Logístico: `http://127.0.0.1:8000/logistics/`  
