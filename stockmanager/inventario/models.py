from django.db import models
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique = True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'categorias' 

    def __str__(self):
        return self.nombre
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, unique = True)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    terminos_pago = models.IntegerField(default=30)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'proveedores'
    def __str__(self):
        return self.nombre
class Cliente(models.Model):
    class TipoChoices(models.TextChoices):
        MINORISTA = 'minorista', 'Minorista'
        MAYORISTA = 'mayorista', 'Mayorista'

    nombre = models.CharField(max_length=150)
    nif = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=9, choices=TipoChoices.choices, default=TipoChoices.MINORISTA)
    class Meta:
        db_table = 'clientes'
    def __str__(self):  
        return self.nombre

class Usuario(models.Model):
    class RolChoices(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        VENDEDOR = 'vendedor', 'Vendedor'
        GERENTE = 'gerente', 'Gerente'
    
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    password_hash  = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=RolChoices.choices, default=RolChoices.VENDEDOR)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'usuarios'
    def __str__(self):
        return self.username
    
class Producto(models.Model):
    codigo_sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    categoria =models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor =models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=10)
    stock_maximo     = models.IntegerField(default=100)
    peso = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    imagen_url = models.URLField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class UnidadPesoChoices(models.TextChoices):
        GRAMOS = 'g', 'Gramos (g)'
        KILOGRAMOS = 'kg', 'Kilogramos (kg)'
        LIBRAS = 'lb', 'Libras (lb)'

    unidad_peso = models.CharField(
        max_length=10,
        choices=UnidadPesoChoices.choices,
        default=UnidadPesoChoices.KILOGRAMOS,
        blank=True,
        null=True
    )
    class Meta:
        db_table = 'productos'

    def __str__(self):
        return self.nombre

class OrdenCompra(models.Model):
    class EstadoChoices(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        RECIBIDA = 'recibida', 'Recibida'
        PARCIAL = 'parcial', 'Parcial'
        CANCELADA = 'cancelada', 'Cancelada'

    numero_orden = models.CharField(max_length=50, unique= True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_orden = models.DateTimeField(auto_now_add=True)
    fecha_entrega_esperada = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=EstadoChoices.choices, default=EstadoChoices.PENDIENTE)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    notas = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'ordenes_compra'
    def __str__(self):
        return self.numero_orden
    
class DetalleOrdenCompra(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_solicitada = models.IntegerField()
    cantidad_recibida = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'detalles_orden_compra'
    
    def __str__(self):
        return f"{self.orden_compra.numero_orden} - {self.producto.nombre}"

class FacturaVenta(models.Model):
    class EstadoChoices(models.TextChoices):
        PAGADA = 'pagada', 'Pagada'
        PENDIENTE = 'pendiente', 'Pendiente'
        VENCIDA = 'vencida', 'Vencida'
        CANCELADA = 'cancelada', 'Cancelada'
    
    numero_factura = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=EstadoChoices.choices, default=EstadoChoices.PENDIENTE)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'facturas_venta'
    
    def __str__(self):
        return self.numero_factura

class DetalleFactura(models.Model):
    factura = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    class Meta:
        db_table = 'detalles_factura'
    
    def __str__(self):
        return f"{self.factura.numero_factura} - {self.producto.nombre}"

class Devolucion(models.Model):
    class MotivoChoices(models.TextChoices):
        DEFECTO = 'defecto', 'Defecto'
        CAMBIO = 'cambio', 'Cambio'
        CLIENTE = 'cliente', 'Solicitud del cliente'
    
    class EstadoChoices(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        PROCESADA = 'procesada', 'Procesada'
        RECHAZADA = 'rechazada', 'Rechazada'
    
    factura = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=20, choices=MotivoChoices.choices)
    estado = models.CharField(max_length=20, choices=EstadoChoices.choices, default=EstadoChoices.PENDIENTE)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'devoluciones'
    
    def __str__(self):
        return f"Devolución {self.id} - {self.producto.nombre}"

class MovimientoInventario(models.Model):
    """
    Registro de TODAS las transacciones de stock.
    Cuando entra una compra, cuando se vende, cuando hay ajuste, etc.
    Es el "historial" del inventario para auditoría.
    """
    class TipoChoices(models.TextChoices):
        ENTRADA = 'entrada', 'Entrada'
        SALIDA = 'salida', 'Salida'
        AJUSTE = 'ajuste', 'Ajuste'
        DEVOLUCION = 'devolucion', 'Devolución'
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TipoChoices.choices)
    cantidad = models.IntegerField()
    stock_anterior = models.IntegerField()
    stock_posterior = models.IntegerField()
    referencia = models.CharField(max_length=100, blank=True, null=True)  # FK externa (orden_compra_id, factura_id, etc)
    motivo = models.CharField(max_length=200, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'movimientos_inventario'
        indexes = [
            models.Index(fields=['producto', 'fecha']),
            models.Index(fields=['tipo', 'fecha']),
        ]
    
    def __str__(self):
        return f"{self.tipo} - {self.producto.codigo_sku}"

class AlertaStock(models.Model):
    class TipoAlertaChoices(models.TextChoices):
        STOCK_BAJO = 'stock_bajo', 'Stock Bajo'
        SIN_STOCK = 'sin_stock', 'Sin Stock'
        SOBRE_STOCK = 'sobre_stock', 'Sobre Stock'
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo_alerta = models.CharField(max_length=20, choices=TipoAlertaChoices.choices)
    fecha_alerta = models.DateTimeField(auto_now_add=True)
    resuelta = models.BooleanField(default=False)
    fecha_resolución = models.DateTimeField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'alertas_stock'
        indexes = [
            models.Index(fields=['producto', 'resuelta']),
            models.Index(fields=['tipo_alerta', 'resuelta']),
        ]
    
    def __str__(self):
        return f"{self.tipo_alerta} - {self.producto.nombre}"

class GastoOperacional(models.Model):
    class CategoriaChoices(models.TextChoices):
        ARRIENDO = 'arriendo', 'Arriendo'
        SERVICIOS = 'servicios', 'Servicios'
        PUBLICIDAD = 'publicidad', 'Publicidad'
        MANTENIMIENTO = 'mantenimiento', 'Mantenimiento'
        OTRO = 'otro', 'Otro'
    
    categoría = models.CharField(max_length=20, choices=CategoriaChoices.choices)
    descripción = models.CharField(max_length=200, blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'gastos_operacionales'
        indexes = [
            models.Index(fields=['categoría', 'fecha']),
        ]
    
    def __str__(self):
        return f"{self.categoría} - ${self.monto}"
class HistorialPrecio(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    precio_nuevo = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        db_table = 'historial_precios'
        indexes = [
            models.Index(fields=['producto', 'fecha_cambio']),
        ]
    
    def __str__(self):
        return f"{self.producto.nombre}: ${self.precio_anterior} → ${self.precio_nuevo}"