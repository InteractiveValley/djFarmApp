from django.conf.urls import url
from carrito import views

urlpatterns = [
    url(r'^pedidos/$', views.pedidos, name='pedidos'),
    url(r'^pedidos/(?P<sale_id>\d+)/$', views.detalle_pedido, name='pedido_detalle'),
    url(r'^pedidos/(?P<sale_id>\d+)/approved/$', views.detalle_aprobar, name='pedido_aprovado'),
    url(r'^pedidos/(?P<sale_id>\d+)/cancel/$', views.detalle_cancelar, name='pedido_cancelar'),
    url(r'^pedidos/(?P<sale_id>\d+)/reject/$', views.detalle_rechazar_receta, name='pedido_rechazar_receta'),
    url(r'^pedidos/(?P<sale_id>\d+)/delivered/$', views.detalle_entregar, name='pedido_entregado'),
    url(r'^enviar/pedidos/(?P<sale_id>\d+)/$', views.send_sale_for_email, name='enviar_pedido'),
    url(r'^recibos/$', views.recibos, name='recibos'),
    url(r'^crear/recibo/$', views.post_recibos, name='crear_recibo')
]