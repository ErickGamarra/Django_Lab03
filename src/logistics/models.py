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
