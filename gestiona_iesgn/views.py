from django.shortcuts import render,redirect
import socket
from usuarios.libldap import LibLDAP
from django.conf import settings
from django.http import Http404
from info.views import getInfoVisibility
def index(request):
    info={}
    ## Generamos últimas noticias
    visibility="public"
    if request.session.get("username"):
        visibility="auth"
    if request.session.get("profesor"):
        visibility="profesor"
    datos=getInfoVisibility("noticias",visibility)
    info["noticias"]=datos
    ####
    ## Generamos últimas entradas del blog
    datos=getInfoVisibility("blog",visibility)
    info["blog"]=datos[:5]

    if request.method=="GET":
        return render(request,'index.html',info)
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        lldap=LibLDAP(username,password)
        if username!="" and lldap.isbind:
                busqueda='(uid=%s)'%username
                resultados=lldap.buscar(busqueda)
                
                # Solo dejamos loguearse a los alumnos y profesores
                # No dejamos a los AA y a los AP
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
        ldap.logout()

def salir(request):
    del request.session["username"]
    del request.session["password"]
    try:
        del request.session["profesor"]
    except:
        pass
    return redirect(settings.SITE_URL)

def test_profesor(request):
    if not request.session.get("profesor",False):
        raise Http404  


def test_login(request):
    if not request.session.get("username",False):
        raise Http404  
