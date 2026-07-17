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
    nit = models.CharField(max_length=50, unique=True, null=True, blank=True)
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
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

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