from django.db.models.signals import post_save
from django.db.models.signals import pre_save
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

@transaction.atomic
@receiver(pre_save, sender=DetalleOrdenCompra)
def actualizar_stock_por_compra(sender, instance, **kwargs):
    if not instance.pk:
        print("El registro es nuevo, no hay una version antigua")
        return
    try:
        registro_anterior = DetalleOrdenCompra.objects.get(pk=instance.pk)
    except DetalleOrdenCompra.DoesNotExist:
        return
    cantidad_anterior = registro_anterior.cantidad_recibida
    cantidad_nueva = instance.cantidad_recibida
    diferencia = cantidad_nueva - cantidad_anterior
    if diferencia == 0:
        return
    if diferencia > 0:
        producto = instance.producto
        stock_anterior = producto.stock_actual        
        producto.stock_actual = producto.stock_actual + diferencia
        producto.save()   
    # 5. Registrar en MovimientoInventario
        tipo = "entrada"
        cantidad = diferencia
        stock_posterior = producto.stock_actual
        MovimientoInventario.objects.create(
            producto = producto,
            tipo = tipo,
            cantidad = cantidad,
            stock_anterior = stock_anterior,
            stock_posterior = stock_posterior,
            referencia = instance.orden_compra.numero_orden,
            motivo = 'Compra de producto',
            usuario = instance.orden_compra.usuario
        )