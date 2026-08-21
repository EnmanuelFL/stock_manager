# Create your views here.
from django.shortcuts import render
from .models import Producto, AlertaStock, FacturaVenta
from django.db.models import F
from django.shortcuts import render, redirect
from .forms import ProductoForm
from django.shortcuts import get_object_or_404

def dashboard(request):
    contexto = {
        'total_productos': Producto.objects.count(),
        'productos_bajo_stock': Producto.objects.filter(stock_actual__lte=F('stock_minimo')).count(),
        'alertas_sin_resolver': AlertaStock.objects.filter(resuelta=False).count(),
    }
    return render(request, 'inventario/dashboard.html', contexto)

def lista_productos(request):
    productos = Producto.objects.all()
    contexto = {
        'productos': productos
    }
    return render(request, 'inventario/productos/lista.html', contexto)

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST )
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
        return render(request, 'inventario/productos/crear.html', {'form': form})
    elif request.method == 'GET':
        form = ProductoForm()
        return render(request, 'inventario/productos/crear.html', {'form': form})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
        return render(request, 'inventario/productos/editar.html', {'form': form})
    else:
        form = ProductoForm(instance=producto)
        return render(request, 'inventario/productos/editar.html', {'form': form})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'inventario/productos/eliminar.html', {'producto': producto})