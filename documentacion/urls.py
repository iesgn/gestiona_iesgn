from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^(?P<doc>[a-z0-9]+)$', views.doc),
	
  ]
