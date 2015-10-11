"""farmApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy

admin.autodiscover()

from productos.viewsets import CategoryViewSet, ProductViewSet, DiscountViewSet
from usuarios.viewsets import UserViewSet, DirectionViewSet, ScheduledOrderViewSet, QuestionViewSet, RatingViewSet
from carrito.viewsets import SaleViewSet, DetailSaleViewSet, ImageSaleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categorias', CategoryViewSet)
router.register(r'productos', ProductViewSet)
router.register(r'descuentos', DiscountViewSet)
router.register(r'direcciones', DirectionViewSet)
router.register(r'usuarios', UserViewSet)
router.register(r'pedidos/periodicos', ScheduledOrderViewSet)
router.register(r'preguntas', QuestionViewSet)
router.register(r'ventas', SaleViewSet)
router.register(r'detalle/ventas', DetailSaleViewSet)
router.register(r'images/ventas', ImageSaleViewSet)
router.register(r'ratings', RatingViewSet)


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^usuarios/register/user/conekta/', 'usuarios.views.user_conekta_create', name='user_conekta_create'),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'usuarios.views.home', name='homepage'),
    url(r'^pedidos/$', 'carrito.views.pedidos', name='pedidos'),
    url(r'^pedidos/(?P<sale_id>\d+)/$', 'carrito.views.detalle_pedido', name='pedido_detalle'),
    url(r'^pedidos/(?P<sale_id>\d+)/approved/$', 'carrito.views.detalle_aprobar', name='pedido_aprovado'),
    url(r'^pedidos/(?P<sale_id>\d+)/reject/$', 'carrito.views.detalle_rechazar', name='pedido_rechazado'),
    url(r'^pedidos/(?P<sale_id>\d+)/delivered/$', 'carrito.views.detalle_entregar', name='pedido_entregado'),
    url(r'^login/$', 'usuarios.views.login_frontend', name='login_frontend'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login/'}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, }),
]
