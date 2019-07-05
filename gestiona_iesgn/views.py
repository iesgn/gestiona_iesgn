from django.shortcuts import render,redirect
import socket
from usuarios.libldap import gnLDAP
from django.conf import settings
from django.http import Http404
def index(request):
    if request.method=="GET":
        hostname = socket.gethostname()
        info={"hostname":hostname}
        return render(request,'index.html',info)
    else:
        username = request.POST["username"]
        password = request.POST["password"].encode('utf-8')
        lldap=gnLDAP(username,password)
        if username!="" and lldap.isbind:
                busqueda='(uid=%s)'%username
                resultados=lldap.buscar(busqueda)
                info=resultados[0].get_attributes()
                # Solo dejamos loguearse a los alumnos y profesores
                # No dejamos a los AA y a los AP
                tipos=["asir1","asir2","smr1","smr2","profesores"]

                if not lldap.isMemberOfGroups(request.POST["username"],tipos):
                    info={"error":True}
                    return render(request,"index.html",info)
                request.session["username"]=username
                request.session["password"]=password
                if lldap.isMemberOfGroup(request.POST["username"],"profesores"):
                    request.session["profesor"]=True
                else:
                    request.session["profesor"]=False
                return render(request,"index.html")
        else:
               info={"error":True}
               return render(request,"index.html",info)

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
