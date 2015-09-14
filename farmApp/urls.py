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
from rest_framework.authtoken.views import obtain_auth_token

admin.autodiscover()

from productos.viewsets import CategoryViewSet, ProductViewSet
from usuarios.viewsets import UserViewSet, DirectionViewSet, PedidoPeriodicoViewSet, PreguntaViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categorias', CategoryViewSet)
router.register(r'productos', ProductViewSet)
router.register(r'direcciones', DirectionViewSet)
router.register(r'usuarios', UserViewSet)
router.register(r'pedidos/periodicos', PedidoPeriodicoViewSet)
router.register(r'preguntas', PreguntaViewSet)

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^api/', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^api-token-auth/', obtain_auth_token, name='api-token'),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'usuarios.views.home', name='homepage'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),   
]
