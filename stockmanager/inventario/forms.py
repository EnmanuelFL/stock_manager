from django import forms
from .models import Producto, FacturaVenta, DetalleFactura, OrdenCompra, DetalleOrdenCompra

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_sku', 'nombre', 'categoria', 'proveedor', 
                  'precio_compra', 'precio_venta', 'stock_actual', 
                  'stock_minimo', 'stock_maximo', 'peso','unidad_peso', 'activo']
class FacturaVentaForm(forms.ModelForm):
    class Meta:
        model = FacturaVenta
        fields = ['numero_factura', 'cliente', 'fecha_vencimiento', 'impuesto', 'notas']
class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = ['producto', 'cantidad', 'precio_unitario', 'descuento']

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['numero_orden', 'proveedor', 'fecha_entrega_esperada', 'notas']

class DetalleOrdenCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleOrdenCompra
        fields = ['producto', 'cantidad_solicitada', 'precio_unitario']