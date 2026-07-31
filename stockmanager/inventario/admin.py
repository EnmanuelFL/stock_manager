from django.contrib import admin

# Register your models here.
from .models import Producto
from .models import Categoria
from .models import Proveedor
from .models import Cliente
from .models import Usuario
from .models import OrdenCompra
from .models import DetalleOrdenCompra
from .models import FacturaVenta
from .models import DetalleFactura
from .models import Devolucion
from .models import MovimientoInventario
from .models import AlertaStock
from .models import GastoOperacional
from .models import HistorialPrecio


admin.site.register([Producto, Categoria, Proveedor, Cliente, Usuario, OrdenCompra, DetalleOrdenCompra,
FacturaVenta, DetalleFactura, Devolucion, MovimientoInventario, AlertaStock, GastoOperacional, HistorialPrecio])