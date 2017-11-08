from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.add),
	url(r'^(?P<usuario>[0-9a-z.]+)/(?P<file>[0-9a-z.]+)$', views.download),
	
  ]
