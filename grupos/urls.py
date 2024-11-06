from django.urls import  re_path

from . import views

urlpatterns = [
	re_path(r'^(?P<curso>[a-z0-9]+)$', views.cursos),
	re_path(r'^delete/(?P<curso>[a-z0-9]+)/(?P<usuario>[a-zA-Z0-9.]+)$', views.eliminar),
  ]
