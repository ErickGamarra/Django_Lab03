from django.contrib import admin
from .models import Proveedor, Sucursal, Transportista, CategoriaInsumo, Material


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'ruc', 'telefono', 'correo')
    search_fields = ('razon_social', 'ruc')


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'direccion', 'capacidad_almacen')
    list_filter = ('ciudad',)


@admin.register(Transportista)
class TransportistaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'placa', 'tipo_vehiculo', 'activo')
    list_filter = ('activo', 'tipo_vehiculo')


@admin.register(CategoriaInsumo)
class CategoriaInsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'unidad_medida', 'precio_unitario', 'stock')
    list_filter = ('categoria',)
    search_fields = ('nombre',)
