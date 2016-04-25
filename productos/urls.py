# -*- encoding: utf-8 -*-
from django.conf.urls import url
from productos import views

urlpatterns = [
    url(r'^inventario/$', views.inventario, name='inventario'),
    url(r'^categorias/$', views.categorias, name='categorias'),
    url(r'^categorias/(?P<category_id>\d+)/up/$', views.categorias_up, name='categorias_arriba'),
    url(r'^categorias/(?P<category_id>\d+)/down/$', views.categorias_down, name='categorias_abajo'),

]