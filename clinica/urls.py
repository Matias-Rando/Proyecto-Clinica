from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

    path("pacientescargar", views.pacientescargar, name="pacientescargar"),
    path("pacientesindex", views.pacientesindex, name="pacientesindex"),

    path("turnoscreate", views.turnoscreate, name="turnoscreate"),
    path("turnosindex", views.turnosindex, name="turnosindex"),
    path("turnoshow/<int:turno_id>", views.turnoshow, name="turnoshow"),
    path("turnosupdate/<int:turno_id>", views.turnosupdate, name="turnosupdate"),
    path("turnosdelete/<int:turno_id>", views.turnosdelete, name="turnosdelete"),

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
]