from django.conf.urls import url
from usuarios import views

urlpatterns = [
    url(r'^rakings/$', views.calificaciones, name='calificaciones')
]