from django import forms
from .models import Producto, FacturaVenta, DetalleFactura

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_sku', 'nombre', 'categoria', 'proveedor', 
                  'precio_compra', 'precio_venta', 'stock_actual', 
                  'stock_minimo', 'stock_maximo', 'peso', 'activo']
class FacturaVentaForm(forms.ModelForm):
    class Meta:
        model = FacturaVenta
        fields = ['numero_factura', 'cliente', 'fecha_vencimiento', 'impuesto', 'notas']
class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = ['producto', 'cantidad', 'precio_unitario', 'descuento']