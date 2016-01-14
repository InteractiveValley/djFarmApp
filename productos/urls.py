# -*- encoding: utf-8 -*-
from django.conf.urls import url
from productos import views

urlpatterns = [
    url(r'^inventario/$', views.inventario, name='inventario')
]