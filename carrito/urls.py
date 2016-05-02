# -*- encoding: utf-8 -*-
from django.conf.urls import url
from carrito import views

urlpatterns = [
    url(r'^pedidos/$', views.pedidos, name='pedidos'),
    url(r'^pedidos/(?P<sale_id>\d+)/$', views.detalle_pedido, name='pedido_detalle'),
    url(r'^pedidos/(?P<sale_id>\d+)/recetas/$', views.pedido_ver_recetas, name='pedido_ver_recetas'),
    url(r'^pedidos/(?P<sale_id>\d+)/approved/$', views.detalle_aprobar, name='pedido_aprovado'),
    url(r'^pedidos/(?P<sale_id>\d+)/cancel/$', views.detalle_cancelar, name='pedido_cancelar'),
    url(r'^pedidos/(?P<sale_id>\d+)/reject/$', views.detalle_rechazar_receta, name='pedido_rechazar_receta'),
    url(r'^pedidos/(?P<sale_id>\d+)/delivered/$', views.detalle_entregar, name='pedido_entregado'),
    url(r'^pedidos/(?P<sale_id>\d+)/review/$', views.revisar_pago, name='pedido_revisar_pago'),
    url(r'^enviar/pedidos/(?P<sale_id>\d+)/$', views.send_sale_for_email, name='enviar_pedido'),
    url(r'^recibos/$', views.recibos, name='recibos'),
    url(r'^crear/recibo/$', views.post_recibos, name='crear_recibo'),
    url(r'^envios/$', views.envios, name='envios'),
    url(r'^crear/envio/$', views.post_envios, name='crear_envio'),
    url(r'^envios/(?P<send_id>\d+)/$', views.detalle_envio, name='envio_detalle'),
    url(r'^crear/detalle/envio/(?P<detail_sale_id>\d+)/$', views.post_detalle_envio, name='crear_envio_detalle'),
    url(r'^quitar/detalle/envio/(?P<detail_send_id>\d+)/$', views.delete_detalle_envio, name='delete_envio_detalle'),
]