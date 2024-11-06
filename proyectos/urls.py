from django.urls import path,re_path

from . import views

urlpatterns = [
	re_path(r'^$', views.show),
	path('<path:url>',views.server),
	
  ]
