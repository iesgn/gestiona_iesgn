from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^alumnos$', views.listarAlumnos),
	url(r'^profesores$', views.listarProfesores),
	url(r'^update/(?P<usuario>[0-9]+)$', views.update),
	url(r'^alumnos/add$', views.addAlumnos),

  ]
