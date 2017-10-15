# -*- coding: utf-8 -*-
from django.shortcuts import render
from usuarios.libldap import gnLDAP
from cursos.forms import BuscarUsuario
import operator
# Create your views here.

def cursos(request,curso):
	test_profesor(request)
	if request.method=="POST":
		print request.POST.getlist("usuarios")

	ldap=gnLDAP()
	filtro={"grupo":curso}
	lista=ldap.gnBuscar(filtro=filtro)
	form=BuscarUsuario(filtro)
	info={"titulo":ldap.grupo[curso],"resultados":lista,"form":form}
	return render(request,"listar_cursos.html",info)

def delete(request,usuario):
	pass