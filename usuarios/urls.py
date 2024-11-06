from django.urls import re_path

from . import views

urlpatterns = [
	re_path(r'^$', views.listarUsuarios),
	re_path(r'^update/(?P<usuario>[\- 0-9A-Za-z.]+)$', views.update),
	re_path(r'^add$', views.add),
	re_path(r'^perfil$', views.perfil),
	re_path(r'^del$', views.delete),

  ]
