# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from usuarios.libldap import gnLDAP
from cursos.forms import BuscarUsuario
from gestiona_iesgn.views import test_profesor
from django.http import Http404
from django.conf import settings
import operator
# Create your views here.

def cursos(request,curso):
	test_profesor(request)
	ldap=gnLDAP()
	if not curso in ldap.grupo.keys():
		raise Http404  
	if request.method=="POST":
		ldap=gnLDAP(request.session["username"],request.session["password"])
		for usuario in request.POST.getlist("usuarios"):
			grupos=ldap.memberOfGroup(usuario,key=True)
			try:
				if len(grupos)==1:
					if grupo[0]=="antiguosalumnos":
						ldap.modUserGroup(str(usuario),"antiguosalumnos","del")
					if grupo[0]=="antiguosprofesores":
						ldap.modUserGroup(str(usuario),"antiguosprofesores","del")
			
				ldap.modUserGroup(str(usuario),str(curso),"add")
			except:
				pass

	
	filtro={"grupo":curso}
	lista=ldap.gnBuscar(filtro=filtro)
	form=BuscarUsuario(filtro)
	info={"titulo":ldap.grupo[curso],"resultados":lista,"form":form}
	return render(request,"listar_cursos.html",info)

def eliminar(request,curso,usuario):
	test_profesor(request)
	ldap=gnLDAP(request.session["username"],request.session["password"])
	try:
		ldap.modUserGroup(str(usuario),str(curso),"del")
	except:
		pass
	ldap=gnLDAP()
	grupos=ldap.memberOfGroup(usuario,key=True)
	if len(grupos)==0:
		ldap=gnLDAP(request.session["username"],request.session["password"])
		if curso=="profesores":
			ldap.modUserGroup(str(usuario),"antiguosprofesores","add")
		else:
			ldap.modUserGroup(str(usuario),"antiguosalumnos","add")
	return redirect(settings.SITE_URL+"/cursos/"+curso)


	