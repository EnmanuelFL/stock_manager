from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_sku', 'nombre', 'categoria', 'proveedor', 
                  'precio_compra', 'precio_venta', 'stock_actual', 
                  'stock_minimo', 'stock_maximo', 'peso', 'activo']