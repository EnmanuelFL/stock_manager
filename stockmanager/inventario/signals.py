from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import DetalleFactura, Producto, MovimientoInventario

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