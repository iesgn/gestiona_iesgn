from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^alumnos$', views.listarAlumnos),
	url(r'^profesores$', views.listarProfesores),
	url(r'^update/(?P<usuario>[a-z.]+)$', views.update),
	url(r'^alumnos/add$', views.addAlumnos),
	url(r'^profesores/add$', views.addProfesores),
	url(r'^perfil$', views.perfil),

  ]
