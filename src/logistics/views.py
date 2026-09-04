from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Proveedor, Sucursal, Transportista, CategoriaInsumo, Material
from .forms import (
    ProveedorForm, SucursalForm, TransportistaForm,
    CategoriaInsumoForm, MaterialForm
)


# PANEL PRINCIPAL (DASHBOARD)

def index_logistics(request):
    contexto = {
        'total_proveedores': Proveedor.objects.count(),
        'total_sucursales': Sucursal.objects.count(),
        'total_transportistas': Transportista.objects.filter(activo=True).count(),
        'total_categorias': CategoriaInsumo.objects.count(),
        'total_materiales': Material.objects.count(),
        'materiales_recientes': Material.objects.select_related('categoria').all()[:5]
    }
    return render(request, 'logistics/index.html', contexto)


# CRUD: MATERIALES (ENTIDAD DEPENDIENTE 1:N)

def material_list(request):
    materiales = Material.objects.select_related('categoria').all()
    return render(request, 'logistics/material_list.html', {'materiales': materiales})


def material_create(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Material registrado exitosamente.")
            return redirect('logistics:material_list')
    else:
        form = MaterialForm()
    return render(request, 'logistics/material_form.html', {'form': form, 'titulo': 'Registrar Insumo / Material'})


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


def material_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        messages.warning(request, f'El material "{material.nombre}" fue eliminado.')
        return redirect('logistics:material_list')
    return render(request, 'logistics/material_confirm_delete.html', {'objeto': material})


# CRUD: CATEGORÍAS (ENTIDAD MAESTRA 1:N)

def categoria_list(request):
    categorias = CategoriaInsumo.objects.all()
    return render(request, 'logistics/categoria_list.html', {'categorias': categorias})


def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaInsumoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada con éxito.")
            return redirect('logistics:categoria_list')
    else:
        form = CategoriaInsumoForm()
    return render(request, 'logistics/categoria_form.html', {'form': form, 'titulo': 'Nueva Categoría de Insumo'})


# CRUD: PROVEEDORES (ENTIDAD INDEPENDIENTE)

def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'logistics/proveedor_list.html', {'proveedores': proveedores})


def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor registrado exitosamente.")
            return redirect('logistics:proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'logistics/proveedor_form.html', {'form': form, 'titulo': 'Registrar Proveedor'})
