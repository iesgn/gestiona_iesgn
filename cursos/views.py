# -*- coding: utf-8 -*-
from django.shortcuts import render
from usuarios.libldap import gnLDAP
from cursos.forms import BuscarUsuario
from gestiona_iesgn.views import test_profesor
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

def eliminar(request,curso,usuario):
	test_profesor(request)
	ldap=gnLDAP()
	ldap.modUserGroup(str(usuario),str(curso),"del")
	ldap.modUserGroup(str(usuario),"antiguosalumnos","add")
	return redirect("/cursos/"+curso)