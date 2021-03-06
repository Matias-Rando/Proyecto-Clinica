from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

    path("pacientescargar", views.pacientescargar, name="pacientescargar"),
    path("pacientesindex", views.pacientesindex, name="pacientesindex"),
    path("pacienteshow/<int:paciente_id>", views.pacienteshow, name="pacienteshow"),
    path("pacientesupdate/<int:paciente_id>", views.pacientesupdate, name="pacientesupdate"),
    path("pacientesdelete/<int:paciente_id>", views.pacientesdelete, name="pacientesdelete"),

    path("historialshow/<int:historial_id>", views.historialshow, name="historialshow"),
    path("historialupdate/<int:historial_id>", views.historialupdate, name="historialupdate"),
    path("historialdelete/<int:historial_id>", views.historialdelete, name="historialdelete"),

    path("turnoscreate", views.turnoscreate, name="turnoscreate"),
    path("turnosindex", views.turnosindex, name="turnosindex"),
    path("turnoshow/<int:turno_id>", views.turnoshow, name="turnoshow"),
    path("turnosupdate/<int:turno_id>", views.turnosupdate, name="turnosupdate"),
    path("turnosdelete/<int:turno_id>", views.turnosdelete, name="turnosdelete"),
    path("turnoasistencia/<int:turno_id><int:asistencia_id>", views.turnoasistencia, name="turnoasistencia"),

    path("categoriascreate", views.categoriascreate, name="categoriascreate"),
    path("categoriasindex", views.categoriasindex, name="categoriasindex"),
    path("categoriashow/<int:categoria_id>", views.categoriashow, name="categoriashow"),
    path("categoriasupdate/<int:categoria_id>", views.categoriasupdate, name="categoriasupdate"),
    path("categoriasdelete/<int:categoria_id>", views.categoriasdelete, name="categoriasdelete"),

    path("productoscreate", views.productoscreate, name="productoscreate"),
    path("productosindex", views.productosindex, name="productosindex"),
    path("productoshow/<int:producto_id>", views.productoshow, name="productoshow"),
    path("productosupdate/<int:producto_id>", views.productosupdate, name="productosupdate"),
    path("productosdelete/<int:producto_id>", views.productosdelete, name="productosdelete"),

    path("pedidoscreate", views.pedidoscreate, name="pedidoscreate"),
    path("pedidosindex", views.pedidosindex, name="pedidosindex"),
    path("pedidoshow/<int:pedido_id>", views.pedidoshow, name="pedidoshow"),
    path("pedidosupdate/<int:pedido_id>", views.pedidosupdate, name="pedidosupdate"),
    path("pedidosdelete/<int:pedido_id>", views.pedidosdelete, name="pedidosdelete"),
    path("pedidoestado/<int:pedido_id><int:estado_id>", views.pedidoestado, name="pedidoestado"),

    path("consulta", views.consulta, name="consulta"),

    path("itemdelete/<int:item_id>", views.itemdelete, name="itemdelete"),

    path("reportepacientes/<int:asistencia_id><int:rango>", views.reportepacientes, name="reportepacientes"),
    path("reportepacientespedidos/<int:rango>", views.reportepacientespedidos, name="reportepacientespedidos"),
    path("reporteproductos", views.reporteproductos, name="reporteproductos"),
    path("reporteventas", views.reporteventas, name="reporteventas"),
]