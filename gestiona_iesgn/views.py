from functools import wraps
from django.shortcuts import render, redirect
import json
import os
from usuarios.libldap import LibLDAP
from django.conf import settings
from info.views import getInfoVisibility


def _load_enlaces():
    path = os.path.join(settings.BASE_DIR, 'gestiona_iesgn', 'enlaces.json')
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return [e for e in data if e.get('visible', True)]


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("username"):
            return redirect(settings.SITE_URL + "/")
        return view_func(request, *args, **kwargs)
    return wrapper


def profesor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("profesor"):
            return redirect(settings.SITE_URL + "/")
        return view_func(request, *args, **kwargs)
    return wrapper


def index(request):
    info={}
    visibility="public"
    if request.session.get("username"):
        visibility="auth"
    if request.session.get("profesor"):
        visibility="profesor"
    datos=getInfoVisibility("noticias",visibility)
    info["noticias"]=datos
    datos=getInfoVisibility("blog",visibility)
    info["blog"]=datos[:5]
    info["enlaces"]=_load_enlaces()

    if request.method=="GET":
        return render(request,'index.html',info)
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        lldap=LibLDAP(username,password)
        if username!="" and lldap.isbind:
                busqueda='(uid=%s)'%username
                resultados=lldap.buscar(busqueda)
                tipos=["asir1","asir2","smr1","smr2","profesores"]
                if not lldap.isMemberOfGroups(request.POST["username"],tipos):
                    info["error"]=True
                    return render(request,"index.html",info)
                request.session["username"]=username
                request.session["password"]=password
                if lldap.isMemberOfGroup(request.POST["username"],"profesores"):
                    request.session["profesor"]=True
                else:
                    request.session["profesor"]=False
                return render(request,"index.html")
        else:
               info["error"]=True
               return render(request,"index.html",info)

def salir(request):
    del request.session["username"]
    del request.session["password"]
    try:
        del request.session["profesor"]
    except:
        pass
    return redirect(settings.SITE_URL)

def dual(request):
    return redirect("/gestiona/info/paginas/dual")
