from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from .models import Producto, AlertaStock, FacturaVenta, Usuario, OrdenCompra, DetalleOrdenCompra
from .forms import (
    ProductoForm,
    FacturaVentaForm,
    DetalleFacturaForm,
    OrdenCompraForm,
    DetalleOrdenCompraForm,
)

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

def crear_venta(request):
    if request.method == 'POST':
        factura_form = FacturaVentaForm(request.POST)
        detalle_form = DetalleFacturaForm(request.POST)
        if factura_form.is_valid() and detalle_form.is_valid():
            factura = factura_form.save(commit=False)
            factura.usuario = Usuario.objects.first()
            factura.save()
            detalle = detalle_form.save(commit=False)
            detalle.factura = factura
            detalle.save()
            return redirect('lista_ventas')
    else:
        factura_form = FacturaVentaForm()
        detalle_form = DetalleFacturaForm()
    return render(request, 'inventario/ventas/crear.html', {
        'factura_form': factura_form,
        'detalle_form': detalle_form
    })

def lista_ventas(request):
    facturas = FacturaVenta.objects.all()
    return render(request, 'inventario/ventas/lista.html', {'facturas': facturas})

def crear_compra(request):
    if request.method == 'POST':
        compra_form = OrdenCompraForm(request.POST)
        detalle_compra_form = DetalleOrdenCompraForm(request.POST)
        if compra_form.is_valid() and detalle_compra_form.is_valid():
            compra = compra_form.save(commit=False)
            compra.usuario = Usuario.objects.first()
            compra.save()
            detalle_compra = detalle_compra_form.save(commit=False)
            detalle_compra.orden_compra = compra
            detalle_compra.save()
            return redirect('lista_compras')
    else:
        compra_form = OrdenCompraForm()
        detalle_compra_form = DetalleOrdenCompraForm()
    return render(request, 'inventario/compras/crear.html', {
        'compra_form': compra_form,
        'detalle_compra': detalle_compra_form
    })

def lista_compras(request):
    compras = OrdenCompra.objects.all()
    return render(request, 'inventario/compras/lista.html', {'compras': compras})