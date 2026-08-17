from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import transaction
from .models import DetalleFactura, Producto, MovimientoInventario, DetalleOrdenCompra

@transaction.atomic
@receiver(post_save, sender=DetalleFactura)
def actualizar_stock_por_venta(sender, instance, created, **kwargs):
    if created:
        producto = instance.producto
        if producto.stock_actual < instance.cantidad:
            raise ValueError('No stock suficiente')
        stock_anterior = producto.stock_actual
        producto.stock_actual = producto.stock_actual - instance.cantidad
        producto.save()    
        tipo = 'salida'
        cantidad = instance.cantidad
        stock_posterior = producto.stock_actual
        MovimientoInventario.objects.create(
            producto = producto,
            tipo = tipo,
            cantidad = cantidad,
            stock_anterior = stock_anterior,
            stock_posterior = stock_posterior,
            referencia = instance.factura.numero_factura,  
            motivo = 'Venta a cliente',
            usuario = instance.factura.usuario
        )

@receiver(pre_save, sender=DetalleOrdenCompra)
@transaction.atomic
def actualizar_stock_por_compra(sender, instance, **kwargs):
    cantidad_anterior = 0
    if instance.pk:
        try:
            registro_anterior = DetalleOrdenCompra.objects.get(pk=instance.pk)
            cantidad_anterior = registro_anterior.cantidad_recibida
        except DetalleOrdenCompra.DoesNotExist:
            cantidad_anterior = 0
    cantidad_nueva = instance.cantidad_recibida or 0
    diferencia = cantidad_nueva - cantidad_anterior
    if diferencia == 0:
        return
    producto = instance.producto
    stock_anterior = producto.stock_actual        
    producto.stock_actual += diferencia  # Suma si es positivo, resta si es negativo
    producto.save()   
    tipo_movimiento = "entrada" if diferencia > 0 else "ajuste_salida"
    MovimientoInventario.objects.create(
        producto=producto,
        tipo=tipo_movimiento,
        cantidad=abs(diferencia),  # Guardamos la cantidad en positivo
        stock_anterior=stock_anterior,
        stock_posterior=producto.stock_actual,
        referencia=instance.orden_compra.numero_orden,  
        motivo='Ajuste de recepción de compra',
        usuario=instance.orden_compra.usuario
    )