# -*- encoding: utf-8 -*-
from django.conf.urls import url
from usuarios import views

urlpatterns = [
    url(r'^rakings/$', views.calificaciones, name='calificaciones'),
    url(r'^inapam/$', views.inapams, name='inapams'),
    url(r'^inapam/(?P<inapam_id>\d+)/approve/$', views.inapams_approve, name='inapams_aprobado'),
    url(r'^inapam/(?P<inapam_id>\d+)/reject/$', views.inapams_reject, name='inapams_rechazado'),
    url(r'^inapam/(?P<inapam_id>\d+)/update/$', views.inapams_update, name='inapams_actualizar'),
]