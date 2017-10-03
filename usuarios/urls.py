from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.listar),
	url(r'^update/(?P<usuario>[0-9]+)$', views.update),

  ]
