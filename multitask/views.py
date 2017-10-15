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
				info["usuarios"]=[]
				for usuario in doc["memberships"]:
					if usuario["roles"][0]["id"]==9 and usuario.has_key("user"):
						info["usuarios"].append(usuario)
			#Lista Categorias

        	r=requests.get(url_base+'/projects/'+info["idproyecto"]+'/issue_categories.json',auth=(request.session["username"],request.session["password"]),verify=False)
        	if r.status_code == 200:
        		doc=r.json()
        		info["categorias"]=doc["issue_categories"]

        	return render(request,"tarea.html",info)
    	elif request.POST["paso"]=="step3":
    		opcion=request.POST["opcion"]
    		grupo=request.POST["grupo"]
    		alumnos=request.POST.getlist("alumnos")
        	idproyecto=sesion.POST["idproyecto"]
        	nombreproyecto=sesion.POST["nombreproyecto"]
        	tittle=request.POST["tittle"]
        	desc=request.POST["desc"]
        	categoria=request.POST["categoria"]
        	fecha2=request.POST["fecha2"]
        	resultado=""
       
        if fecha2!="":
        	lfecha=fecha2.split("/")
	        if len(lfecha[1])==1:
	        	lfecha[1]='0'+lfecha[1]
	        if len(lfecha[0])==1:
	        	lfecha[0]='0'+lfecha[0]
	        fecha2=lfecha[2]+"-"+lfecha[1]+"-"+lfecha[0]


        if opcion=="grupo":
        	r=requests.get(url_base+'groups/'+grupo+'.json?include=users',auth=(request.session["username"],request.session["password"]),verify=False)
        	if r.status_code == 200:
        		doc=r.json()
        		alumnos=[]
        		for user in doc["group"]["users"]:
        			alumnos.append(str(user["id"]))
        

        resultado=""
        for alum in alumnos:
        	r=requests.get(url_base+'/users/'+alum+'.json',auth=(request.session["username"],request.session["password"]),verify=False)
        	if r.status_code==200:
        		doc=r.json()
        		nombre=doc["user"]["firstname"]+" "+doc["user"]["lastname"]
        	payload = {'issue': {'project_id': idproyecto,'subject': tittle,'description': desc,'category_id': int(categoria),'assigned_to_id': int(alum),'due_date':fecha2}}
		
        	parameters_json = json.dumps(payload)
        	headers = {'Content-Type': 'application/json'}
        	r = requests.post(url_base+'issues.json', auth=(request.session["username"],request.session["password"]), data=parameters_json, headers=headers,verify=False)
        	resultado=resultado+nombre+":"+r.reason+"<br/>"
        info={"idproyecto":idproyecto,"nombreproyecto":nombreproyecto,"resultado":resultado}
        return template(request,"final.html",info)
	else:
		r=requests.get(url_base+'projects.json',auth=(request.session["username"],request.session["password"]),verify=False)
		if r.status_code == 200:
			doc=r.json()
			info={"proyectos":doc["projects"]}
			return render(request,"proyectos.html",info)