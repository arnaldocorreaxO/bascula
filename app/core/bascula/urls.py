
from core.bascula.views.bascula.movimiento.views import *
from core.bascula.views.bascula.cliente.views import *
from core.bascula.views.bascula.producto.views import *
from core.bascula.views.bascula.marcavehiculo.views import *
from core.bascula.views.bascula.vehiculo.views import *
from core.bascula.views.bascula.transportista.views import *

from django.urls import path



urlpatterns = [    
    # URL para lectura de Puerto COM
	path('ajax_puerto_serial/<str:puerto>/',leer_puerto_serial,name='leer_puerto_serial'),
	path('ajax_peso_bascula/',leer_peso_bascula,name='leer_peso_bascula'),

    # MOVIMIENTO BASCULA
    path('movimiento', MovimientoList.as_view(), name='movimiento_list'),
    path('movimiento/add/', MovimientoCreate.as_view(), name='movimiento_create'),
    path('movimiento/update/<int:pk>/', MovimientoUpdate.as_view(), name='movimiento_update'),
    path('movimiento/delete/<int:pk>/', MovimientoDelete.as_view(), name='movimiento_delete'),
    path('movimiento/print/<int:pk>/', MovimientoPrint.as_view(), name='movimiento_print'),
    # CLIENTE
    path('cliente', ClienteList.as_view(), name='cliente_list'),
    path('cliente/add/', ClienteCreate.as_view(), name='cliente_create'),
    path('cliente/update/<int:pk>/', ClienteUpdate.as_view(), name='cliente_update'),
    path('cliente/delete/<int:pk>/', ClienteDelete.as_view(), name='cliente_delete'),
    # PRODUCTO
    path('producto', ProductoList.as_view(), name='producto_list'),
    path('producto/add/', ProductoCreate.as_view(), name='producto_create'),
    path('producto/update/<int:pk>/', ProductoUpdate.as_view(), name='producto_update'),
    path('producto/delete/<int:pk>/', ProductoDelete.as_view(), name='producto_delete'),
    # MARCA VEHICULO
    path('marcavehiculo', MarcaVehiculoList.as_view(), name='marcavehiculo_list'),
    path('marcavehiculo/add/', MarcaVehiculoCreate.as_view(), name='marcavehiculo_create'),
    path('marcavehiculo/update/<int:pk>/', MarcaVehiculoUpdate.as_view(), name='marcavehiculo_update'),
    path('marcavehiculo/delete/<int:pk>/', MarcaVehiculoDelete.as_view(), name='marcavehiculo_delete'),
    # VEHICULO
    path('vehiculo', VehiculoList.as_view(), name='vehiculo_list'),
    path('vehiculo/add/', VehiculoCreate.as_view(), name='vehiculo_create'),
    path('vehiculo/update/<int:pk>/', VehiculoUpdate.as_view(), name='vehiculo_update'),
    path('vehiculo/delete/<int:pk>/', VehiculoDelete.as_view(), name='vehiculo_delete'),
    # TRANSPORTISTA
    path('transportista', TransportistaList.as_view(), name='transportista_list'),
    path('transportista/add/', TransportistaCreate.as_view(), name='transportista_create'),
    path('transportista/update/<int:pk>/', TransportistaUpdate.as_view(), name='transportista_update'),
    path('transportista/delete/<int:pk>/', TransportistaDelete.as_view(), name='transportista_delete'),

   ]
