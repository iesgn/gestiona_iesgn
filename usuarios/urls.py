from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.listarUsuarios),
	url(r'^update/(?P<usuario>[\- 0-9A-Za-z.]+)$', views.update),
	url(r'^add$', views.add),
	url(r'^perfil$', views.perfil),
	url(r'^del$', views.delete),

  ]
