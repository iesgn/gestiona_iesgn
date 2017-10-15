# -*- coding: utf-8 -*-
from django.shortcuts import render
from usuarios.libldap import gnLDAP
from cursos.forms import BuscarUsuario
import operator
# Create your views here.

def cursos(request,curso):
	ldap=gnLDAP()
	filtro={"grupo":curso}
	lista=ldap.gnBuscar(filtro=filtro)
	info={"titulo":ldap.grupo[curso],"resultados":lista}
	form=BuscarUsuario()
	return render(request,"listar_cursos.html",info,form=form)