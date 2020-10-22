from django.shortcuts import render
from gestiona_iesgn.views import test_profesor
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import datetime
url_base="https://dit.gonzalonazareno.org/redmine/"
key="7c66d06567766f7f1412615eef7c48720de02ffa"
# Create your views here.


def usuario_id(user):
    params={"name":user,"key":key}
    r=requests.get(url_base+'users.json',params=params,verify=False)
    if r.status_code == 200:
        doc=r.json()
        return doc["users"][0]["id"]
            

def categorias(user):
    params={"assigned_to_id":usuario_id(user),"project_id":"24","status_id":"*","key":key}
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
    #user="josedom"
    #request.session["profesor"]=True
    user="javier.crespillo"
    request.session["profesor"]=False
    if request.session.get("profesor"):
        
        info={}
        return render(request,"profesor.html",info)
    else:
        datos=notas_alumno(user)
        info={"alumno":user,"datos":datos}
        return render(request,"indice.html",info)

def notas_alumno(user):
    datos={}
    for cat in categorias(user):
        datos[cat[0]]={"1ev":[],"2ev":[]}
        params={"sort":"created_on","category_id":cat[1],"assigned_to_id":usuario_id(user),"project_id":"24","status_id":"*","key":key}
        r=requests.get(url_base+'issues.json',params=params,verify=False)
        if r.status_code == 200:
            doc=r.json()
            for tarea in doc["issues"]:
                dat=[]
                dat.append(tarea["subject"])
                for campo in tarea["custom_fields"]:
                    if campo["name"]=="Nota":
                        dat.append(campo["value"])
                    if campo["name"]=="Peso":
                        dat.append(campo["value"])
                if tarea["status"]["name"].lower()=="resuelta":
                    dat.append(True)
                else:
                    dat.append(False)
                #dat.append(tarea["created_on"])
                date_time_obj = datetime.datetime.strptime(tarea["created_on"], '%Y-%m-%dT%H:%M:%SZ')
                if date_time_obj.month>=9:
                    datos[cat[0]]["1ev"].append(dat)
                else:
                    datos[cat[0]]["2ev"].append(dat)
    return datos