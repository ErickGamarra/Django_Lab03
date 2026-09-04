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

---

## 📋 2. Requisitos Funcionales (Ejercicio 8)

* **RF01 al RF04:** Gestión de Proveedores (Crear con RUC único de 11 dígitos, Listar, Editar datos de contacto y Eliminar).
* **RF05 y RF06:** Gestión de Sucursales (Registrar locales físicos, consultar capacidad de almacenamiento y actualizar o dar de baja).
* **RF07:** Control de Transportistas (Dar de alta unidades logísticas, registrar placa única, tipo de vehículo y disponibilidad de servicio).
* **RF08:** Gestión de Categorías de Insumos (Crear familias maestras de insumos con nombre único y descripción técnica).
* **RF09 al RF12:** Gestión de Materiales e Insumos (Registrar insumo vinculado a categoría mediante ForeignKey 1:N, listar con INNER JOIN, editar costos/stock y eliminar de forma segura con confirmación POST).

---

## 🏗️ 3. Aplicación Creada (`logistics`)

* **Modelos:** 5 entidades persistidas en SQLite (`CategoriaInsumo`, `Material`, `Proveedor`, `Sucursal`, `Transportista`).
* **Formularios:** Validaciones `clean_ruc`, `clean_placa` y `clean_precio_unitario`.
* **Vistas CRUD:** Con patrón Post/Redirect/Get (PRG), optimización `select_related('categoria')` y `get_object_or_404`.
* **Templates:** Dashboard interactivo, formularios con widgets Bootstrap 5 y tablas con badges de estado.

Para la guía completa y detalles técnicos, revisar [`../README.md`](../README.md).