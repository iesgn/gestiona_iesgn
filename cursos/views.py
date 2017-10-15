# -*- coding: utf-8 -*-
from django.shortcuts import render
from usuarios.libldap import gnLDAP
import operator
# Create your views here.

def cursos(request,curso):
	ldap=gnLDAP()
	filtro={"grupo":curso}
	lista=ldap.gnBuscar(filtro=filtro)
	info={"titulo":ldap.grupo[curso],"resultados":lista}
	return render(request,"listar_cursos.html",info)