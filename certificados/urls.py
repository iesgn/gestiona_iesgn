from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.add),
	url(r'^(?P<usuario>[0-9a-z.]+)/(?P<tipo>[0-9a-z.]+)/(?P<file>[0-9a-z.]+)$', views.download),
	url(r'^(?P<usuario>[0-9a-z.]+)/(?P<tipo>[0-9a-z.]+)/(?P<direc>[0-9.]+)/(?P<file>[0-9a-z.]+)$', views.download),
	
  ]
