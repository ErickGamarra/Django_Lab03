from django.urls import path
from . import views

app_name = 'logistics'

urlpatterns = [
    # Dashboard principal de logistica
    path('', views.index_logistics, name='index'),

    # CRUD: Materiales (Entidad Dependiente 1:N)
    path('materiales/', views.material_list, name='material_list'),
    path('materiales/nuevo/', views.material_create, name='material_create'),
    path('materiales/editar/<int:pk>/', views.material_update, name='material_update'),
    path('materiales/eliminar/<int:pk>/', views.material_delete, name='material_delete'),

    # CRUD: Categorías (Entidad Maestra 1:N)
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/nuevo/', views.categoria_create, name='categoria_create'),

    # CRUD: Proveedores (Entidad Independiente)
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/nuevo/', views.proveedor_create, name='proveedor_create'),
]
