from django.urls import path, re_path
from . import views

urlpatterns = [
  path('',views.doc),
  re_path(r'^actualizar',views.actualizar),
	re_path(r'^(?P<tipo>[a-z0-9]+)$', views.doc),
  path('<str:tipo>/pagina/<int:pagina>',views.doc),
	#re_path(r'^(?P<tipo>[a-z0-9]+)/(?P<url>[a-z0-9-]+)$', views.show),
  path('<str:tipo>/<path:url>',views.show),
  ]
