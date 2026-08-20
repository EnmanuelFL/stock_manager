# Create your views here.
from django.shortcuts import render
from .models import Producto, AlertaStock, FacturaVenta
from django.db.models import F

def dashboard(request):
    contexto = {
        'total_productos': Producto.objects.count(),
        'productos_bajo_stock': Producto.objects.filter(stock_actual__lte=F('stock_minimo')).count(),
        'alertas_sin_resolver': AlertaStock.objects.filter(resuelta=False).count(),
    }
    return render(request, 'inventario/dashboard.html', contexto)