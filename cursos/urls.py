from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^(?P<curso>[0-9]+)$', views.cursos),
	
  ]
