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
from django.contrib import admin
from django.urls import path,re_path,include
from gestiona_iesgn.views import index,salir,dual

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$',index),
    re_path(r'^logout/$',salir),
    re_path(r'^usuarios/', include('usuarios.urls')),
    re_path(r'^grupos/', include('grupos.urls')),
    re_path(r'^info/', include('info.urls')),
    re_path(r'^portal/', include('info.urls')),
    re_path(r'^multitask/', include('multitask.urls')),
    re_path(r'^correos/', include('correos.urls')),
    re_path(r'^cert/', include('certificados.urls')),
    re_path(r'^proyectos/', include('proyectos.urls')),
    re_path(r'^notas/', include('notas.urls')),
    path('dual',dual),
    re_path(r'^empresas/', include("empresas.urls")),
    path('vpn/', include('vpn.urls')),
    
    
]
