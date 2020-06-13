from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^actualizar',views.actualizar),
	url(r'^(?P<tipo>[a-z0-9]+)$', views.doc),
	url(r'^(?P<tipo>[a-z0-9]+)/(?P<url>[a-z0-9-]+)$', views.show),
  ]
