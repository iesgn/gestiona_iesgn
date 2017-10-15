# -*- coding: utf-8 -*-
from django.shortcuts import render
from usuarios.libldap import gnLDAP
import operator
# Create your views here.

def cursos(request,curso):
	ldap=gnLDAP()
	filtro["grupo"]=curso
	lista=ldap.gnBuscar(filtro=filtro)
	clases=["","1º ASIR","2º ASIR","1º SMR","2º SMR"]
	info={"titulo":clases[int(curso)],"resultados":lista}
	return render(request,"listar_cursos.html",info)