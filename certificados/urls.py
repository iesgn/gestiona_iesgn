from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.add),
	url(r'^(?P<usuario>[0-9a-z.]+)/usuario/(?P<file>[0-9a-z.]+)$', views.download),
	url(r'^(?P<usuario>[0-9a-z.]+)/equipo/(?P<direc>[0-9a-z.]+)/(?P<file>[0-9a-z.]+)$', views.download),
	
  ]
