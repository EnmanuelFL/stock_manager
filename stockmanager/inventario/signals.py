from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import transaction
from .models import DetalleFactura, Devolucion, MovimientoInventario, DetalleOrdenCompra

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
    tipo_movimiento = "entrada" if diferencia > 0 else "salida"
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

# DEVOLUCION
@receiver(pre_save, sender=Devolucion)
def guardar_estado_anterior(sender, instance, **kwargs):
    if instance.pk:
        try:
            anterior = Devolucion.objects.get(pk=instance.pk)
            instance._estado_anterior = anterior.estado
        except Devolucion.DoesNotExist:
            instance._estado_anterior = None
@receiver(post_save, sender=Devolucion)
def procesar_devolucion(sender, instance, **kwargs):
    estado_anterior = getattr(sender, '_estado_anterior', None)
    if estado_anterior != "procesada" and instance.estado == "procesada":
            producto = instance.producto
            stock_anterior = producto.stock_actual
            producto.stock_actual += instance.cantidad
            producto.save()
            tipo_movimiento = "devolucion"
            MovimientoInventario.objects.create(
                producto=producto,
                tipo=tipo_movimiento,
                cantidad=abs(instance.cantidad),  
                stock_anterior=stock_anterior,
                stock_posterior=producto.stock_actual,
                referencia=instance.factura.numero_factura,  
                motivo=f'devolucion de producto{instance.motivo}',
                usuario=instance.usuario
            )
    
