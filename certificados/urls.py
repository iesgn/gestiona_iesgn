from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.add),
	url(r'^(?P<usuario>[\w.@+-]+)/usuario/(?P<file>[\w.]{0,256})$', views.download),
	url(r'^(?P<usuario>[\w.@+-]+)/equipo/(?P<direc>[0-9a-z.]+)/(?P<file>[\w.]{0,256})$', views.download),
	url(r'^(?P<usuario>[\w.@+-]+)/equipo/(?P<direc>[0-9a-z.]+)/(?P<file>[\w.]{0,256})/del$', views.revocar),
	url(r'^(?P<usuario>[\w.@+-]+)/usuario/(?P<file>[\w.]{0,256})/del$', views.revocar),
	
  ]
