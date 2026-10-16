from django.urls import path
from . import views, api_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

auth_views.LoginView.as_view(templeate_name='login.html')
auth_views.LogoutView.as_view(next_page='login.html')

router = DefaultRouter()
router.register(r'productos', api_views.ProductoViewSet)
router.register(r'categorias', api_views.CategoriaViewSet)
router.register(r'ventas', api_views.FacturaVentaViewSet)
router.register(r'detalles_factura', api_views.DetalleFacturaViewSet)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/crear/', views.crear_venta, name='crear_venta'),
    path('compras/', views.lista_compras, name='lista_compras'),
    path('compras/crear/', views.crear_compra, name='crear_compra'),
    path('api/', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(templeate_name='login.html')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login.html'))
]