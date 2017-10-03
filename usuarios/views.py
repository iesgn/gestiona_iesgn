# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from usuarios.libldap import LibLDAP
from usuarios.forms import BuscarUsuario,newUserForm
from gestiona_iesgn.views import test_profesor
import operator


def listar(request):
    test_profesor(request)
    if request.method=="GET":
        form=BuscarUsuario()
        tipo1="1"
        tipo2="9"
        givenname="*"
        sn="*"
    else:
        form=BuscarUsuario(request.POST)
        if request.POST["clase"]=="0":
            tipo1="1"
            tipo2="9"
        else:
            tipo1=request.POST["clase"]
            tipo2=str(int(request.POST["clase"])+1)
        givenname="*" if request.POST["nombre"]=="" else request.POST["nombre"]+"*"
        sn="*" if request.POST["apellidos"]=="" else request.POST["apellidos"]+"*"
    lldap=LibLDAP()    
    resultado=[]
    for i in xrange(int (tipo1),int(tipo2)):
        busqueda='(&(givenname=%s)(sn=%s)(description=%s))'%(givenname,sn,str(i))
        r=lldap.buscar(busqueda)
        resultado.extend(r)
    busqueda='(&(givenname=%s)(sn=%s)(description=%s))'%(givenname,sn," ")
    r=lldap.buscar(busqueda)
    resultado.extend(r)
    lista=[]
    for res in resultado:
        lista.append(res.get_attributes())
    lista=clase(lista)
    lista.sort(key=operator.itemgetter('sn'))
    info={"resultados":lista,'form':form}
    return render(request,"listar.html",info)

def clase(lista):
    resultado=[]
    clase=["","1º ASIR","2º ASIR","1º SMR","2º SMR","Profesor","A.A.","A.P.","Otros"]
    for usuario in lista:
        try:
            usuario["description"][0]=clase[int(usuario["description"][0])]
        except:
            usuario["description"][0]="---"
        resultado.append(usuario)
    return resultado

def update(request):
    pass

def add(request):
    form=newUserForm(request.POST)
    if form.is_valid():
        pass
    
    info={'form':form}
    return render(request,"new.html",info)

