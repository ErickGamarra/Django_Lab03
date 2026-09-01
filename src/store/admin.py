from django.contrib import admin
from .models import Prenda


@admin.register(Prenda)
class PrendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'marca', 'tipo', 'categoria', 'talla', 'precio', 'stock', 'disponible', 'activo')
    list_filter = ('tipo', 'categoria', 'disponible', 'activo')
    search_fields = ('nombre', 'marca', 'descripcion')
    list_editable = ('precio', 'stock', 'disponible', 'activo')
