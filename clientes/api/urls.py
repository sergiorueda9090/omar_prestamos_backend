from django.urls import path
from . import views

urlpatterns = [
    # Clientes
    path('api/',                               views.listar_clientes,      name="listar_clientes"),
    path('api/crear/',                         views.crear_cliente,        name="crear_cliente"),
    path('api/<int:cliente_id>/',              views.obtener_cliente,      name="obtener_cliente"),
    path('api/<int:cliente_id>/actualizar/',   views.actualizar_cliente,   name="actualizar_cliente"),
    path('api/delete/<int:cliente_id>/',       views.eliminar_cliente,     name="eliminar_cliente"),
    path('api/exportar/',                      views.exportar_clientes_excel, name='exportar_clientes_excel'),
    # Cuotas
    path('api/cuotas/', views.listar_cuotas,                                     name="listar_cuotas"),
    path('api/cuotas/crear/', views.crear_cuota,                                 name="crear_cuota"),
    path('api/cuotas/<int:cuota_id>/actualizar/', views.actualizar_estado_cuota, name="actualizar_estado_cuota"),
]
