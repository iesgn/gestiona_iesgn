"""gestiona_iesgn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from gestiona_iesgn.views import index,salir

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',index),
    url(r'^logout/$',salir),
    url(r'^usuarios/', include('usuarios.urls')),
    url(r'^cursos/', include('cursos.urls')),
    url(r'^documentacion/', include('documentacion.urls')),
    url(r'^multitask/', include('multitask.urls')),
    url(r'^correos/', include('correos.urls')),

]
