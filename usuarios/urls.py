from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.listarAlumnos),
	url(r'^error$', views.listar),
	url(r'^update/(?P<usuario>[0-9]+)$', views.update),
	url(r'^del/(?P<usuario>[0-9]+)$', views.delete),
	url(r'^add$', views.add),

  ]
