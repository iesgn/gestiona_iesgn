from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^(?P<curso>[a-z0-9]+)$', views.cursos),
	url(r'^delete/(?P<curso>[a-z0-9]+)/(?P<usuario>[a-zA-Z0-9.]+)$', views.eliminar),
  ]
