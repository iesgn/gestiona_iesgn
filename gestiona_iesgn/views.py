from functools import wraps
from django.shortcuts import render, redirect
import json
import os
from usuarios.libldap import LibLDAP
from ldap3.utils.conv import escape_filter_chars
from django.conf import settings
def _load_config():
    path = os.path.join(settings.BASE_DIR, 'gestiona_iesgn', 'enlaces.json')
    with open(path, encoding='utf-8') as f:
        return json.load(f)


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
    config = _load_config()
    info["enlaces"] = [e for e in config["tarjetas"] if e.get("visible", True)]

    if request.method=="GET":
        return render(request,'index.html',info)
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        lldap=LibLDAP(username,password)
        if username!="" and lldap.isbind:
                busqueda='(uid=%s)' % escape_filter_chars(username)
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
                return render(request,"index.html",info)
        else:
               info["error"]=True
               return render(request,"index.html",info)

def salir(request):
    del request.session["username"]
    del request.session["password"]
    try:
        del request.session["profesor"]
    except KeyError:
        pass
    return redirect(settings.SITE_URL)

def dual(request):
    return redirect(settings.SITE_URL + "/info/paginas/dual")

def dual_page(request):
    return render(request, "dual.html")

def proyectos_page(request):
    path = os.path.join(settings.BASE_DIR, 'gestiona_iesgn', 'proyectos.json')
    with open(path, encoding='utf-8') as f:
        datos = json.load(f)
    static = settings.SITE_URL_STATIC
    for curso in datos:
        for alumno in curso['alumnos']:
            for campo, dato in alumno.items():
                if isinstance(dato, dict) and dato.get('info'):
                    info = dato['info']
                    if isinstance(info, str) and not info.startswith('http'):
                        dato['info'] = static + 'proyectos/' + info
                    elif isinstance(info, list):
                        dato['info'] = [
                            v if v.startswith('http') else static + 'proyectos/' + v
                            for v in info if v
                        ]
    return render(request, "proyectos.html", {"datos": datos})
