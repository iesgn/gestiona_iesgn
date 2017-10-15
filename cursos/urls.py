from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^(?P<curso>[a-z0-9]+)$', views.cursos),
	url(r'^delete/(?P<usuario>[a-z0-9.]+)$', views.delete),
  ]
