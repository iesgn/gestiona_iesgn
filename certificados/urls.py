from django.urls import re_path

from . import views

urlpatterns = [
	re_path(r'^$', views.add),
	re_path(r'^(?P<usuario>[\w.@+-]+)/usuario/(?P<file>[\w.-]{0,256})$', views.download),
	re_path(r'^(?P<usuario>[\w.@+-]+)/equipo/(?P<direc>[0-9a-z.]+)/(?P<file>[\w.-]{0,256})$', views.download),
	re_path(r'^(?P<usuario>[\w.@+-]+)/equipo/(?P<direc>[0-9a-z.]+)/(?P<file>[\w.-]{0,256})/del$', views.revocar),
	re_path(r'^(?P<usuario>[\w.@+-]+)/usuario/(?P<file>[\w.-]{0,256})/del$', views.revocar),
	
  ]
