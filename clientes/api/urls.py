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

    # =========================================================================
    # ENDPOINTS V2 — ClientesTestMejorado (todo se persiste en DB)
    # =========================================================================

    # Listar clientes (paginado)
    path('api/v2/',                                          views.listar_clientes_v2,            name="listar_clientes_v2"),

    # Crear prestamo (con o sin cronograma)
    path('api/v2/crear/',                                    views.crear_cliente_v2,               name="crear_cliente_v2"),

    # Obtener detalle completo de un prestamo
    path('api/v2/<int:cliente_id>/',                         views.obtener_cliente_detalle,        name="obtener_cliente_detalle"),

    # Pago de cuota (con cronograma — distribuye entre pendientes)
    path('api/v2/<int:cliente_id>/pagar/',                   views.registrar_pago,                 name="registrar_pago"),

    # Pago de cuota (sin cronograma)
    path('api/v2/<int:cliente_id>/pagar-sin-cronograma/',    views.registrar_pago_sin_cronograma,  name="registrar_pago_sin_cronograma"),

    # Pago de interes
    path('api/v2/<int:cliente_id>/pagar-interes/',           views.registrar_pago_interes,         name="registrar_pago_interes"),

    # Eliminar pago de interes
    path('api/v2/pagos-interes/<int:pago_id>/',              views.eliminar_pago_interes,          name="eliminar_pago_interes"),

    # Pagar saldo total
    path('api/v2/<int:cliente_id>/pagar-saldo-total/',       views.registrar_pago_saldo_total,     name="registrar_pago_saldo_total"),

    # Revertir pago de saldo total
    path('api/v2/pagos/<int:pago_id>/revertir-saldo-total/', views.revertir_pago_saldo_total,     name="revertir_pago_saldo_total"),

    # Cambiar fecha de cuota
    path('api/v2/cuotas/<int:cuota_id>/cambiar-fecha/',      views.cambiar_fecha_cuota,            name="cambiar_fecha_cuota"),

    # Eliminar/revertir pago de una cuota
    path('api/v2/cuotas/<int:cuota_id>/eliminar-pago/',      views.eliminar_pago_cuota,            name="eliminar_pago_cuota"),

    # Ampliar prestamo (liquidar + nuevo cronograma)
    path('api/v2/<int:cliente_id>/ampliar/',                 views.ampliar_prestamo,               name="ampliar_prestamo"),

    # Cambiar plazo (solo sin cronograma)
    path('api/v2/<int:cliente_id>/cambiar-plazo/',           views.cambiar_plazo,                  name="cambiar_plazo"),

    # Marcar como perdido
    path('api/v2/<int:cliente_id>/marcar-perdido/',          views.marcar_perdido,                 name="marcar_perdido"),

    # Exportar Excel completo (v2)
    path('api/v2/exportar/',                                 views.exportar_clientes_excel_v2,     name="exportar_clientes_excel_v2"),

    # Dashboard estadísticas
    path('api/v2/dashboard/',                                views.dashboard_stats,                name="dashboard_stats"),

    # Notas del prestamo
    path('api/v2/<int:cliente_id>/notas/',                   views.notas_prestamo,                 name="notas_prestamo"),
    path('api/v2/notas/<int:nota_id>/eliminar/',             views.eliminar_nota,                  name="eliminar_nota"),
]
