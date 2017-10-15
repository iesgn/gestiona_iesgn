from django.shortcuts import render
from gestiona_iesgn.views import test_profesor
from django.views.decorators.csrf import csrf_exempt
import requests
import json
url_base="https://dit.gonzalonazareno.org/redmine/"

# Create your views here.

@csrf_exempt
def inicio(request):
	test_profesor(request)
	if request.method=="POST":
		if request.POST["paso"]=="step2":
			info={}
			info["idproyecto"]=request.POST["proyecto"]
			#Nombre del proyecto
			r=requests.get(url_base+'projects/'+info["idproyecto"]+'.json',auth=(request.session["username"],request.session["password"]),verify=False)
			if r.status_code == 200:
				doc=r.json()
				info["nombreproyecto"]=doc["project"]["name"]
			
			#Lista de grupos
			r=requests.get(url_base+'groups.json',auth=(request.session["username"],request.session["password"]),verify=False)
			if r.status_code == 200:
				doc=r.json()
				info["grupos"]=doc["groups"]
			#Lista de usuarios del proyecto
			r=requests.get(url_base+'projects/'+info["idproyecto"]+'/memberships.json',auth=(request.session["username"],request.session["password"]),verify=False)
			if r.status_code == 200:
				doc=r.json()
				info["usuarios"]=doc["memberships"]
			#Lista Categorias

        	r=requests.get(url_base+'/projects/'+info["idproyecto"]+'/issue_categories.json',auth=(request.session["username"],request.session["password"]),verify=False)
        	if r.status_code == 200:
        		doc=r.json()
        		info["categorias"]=doc["issue_categories"]

        	return render("tarea.html",info)
	else:
		r=requests.get(url_base+'projects.json',auth=(request.session["username"],request.session["password"]),verify=False)
		if r.status_code == 200:
			doc=r.json()
			info={"proyectos":doc["projects"]}
			return render(request,"proyectos.html",info)