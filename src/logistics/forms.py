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
