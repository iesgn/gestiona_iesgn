from django.shortcuts import render
from gestiona_iesgn.views import test_profesor
from django.views.decorators.csrf import csrf_exempt
import requests
import json
url_base="https://dit.gonzalonazareno.org/redmine/"
key="0399e7851259ae2f377e34497432ee3b80204cb2"
# Create your views here.


def usuario_id(user):
    params={"name":user,"key":"0399e7851259ae2f377e34497432ee3b80204cb2"}
    r=requests.get(url_base+'users.json',params=params,verify=False)
    if r.status_code == 200:
        doc=r.json()
        return doc["users"][0]["id"]
            

def categorias(user):
    params={"assigned_to_id":usuario_id(user),"project_id":"24","status_id":"*","key":"0399e7851259ae2f377e34497432ee3b80204cb2"}
    r=requests.get(url_base+'issues.json',params=params,verify=False)
    if r.status_code == 200:
        doc=r.json()
        categorias=[]
        for tarea in doc["issues"]:
            cat=[tarea["category"]["name"],tarea["category"]["id"]]
            if cat not in categorias:
                categorias.append(cat)
        return categorias

@csrf_exempt
def inicio(request):
    #user=request.session["username"]
    user="f.tirado"
    datos={}
    for cat in categorias(user):
        datos[cat[0]]=[]
        params={"sort":"created_on","category_id":cat[1],"assigned_to_id":usuario_id(user),"project_id":"24","status_id":"*","key":"0399e7851259ae2f377e34497432ee3b80204cb2"}
        r=requests.get(url_base+'issues.json',params=params,verify=False)
        if r.status_code == 200:
            doc=r.json()
            for tarea in doc["issues"]:
                dat=[]
                dat.append(tarea["subject"])
                for campo in tarea["custom_fields"]:
                    if campo["name"]=="Nota":
                        dat.append(campo["value"])
                datos[cat[0]].append(dat)
    info={"alumno":user,"datos":datos}
    return render(request,"indice.html",info)