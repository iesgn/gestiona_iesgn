# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from usuarios.libldap import LibLDAP
from usuarios.forms import BuscarUsuario,newUserForm,clasesProfesores
from gestiona_iesgn.views import test_profesor
from django.contrib import messages
import operator
import binascii
import hashlib


def listarAlumnos(request):
    configuracion={
        "tipos":list(xrange(1,5))+[6],
        "AP":{"AP":"alumnos"},
        "titulo":"Listado de Alumnos"
    }
    return listarUsuarios(request,configuracion)

def listarProfesores(request):
    configuracion={
        "tipos":[5,7],
        "AP":{"AP":"profesores"},
        "titulo":"Listado de Profesores"
    }
    return listarUsuarios(request,configuracion)


def listarUsuarios(request,configuracion):
    test_profesor(request)
    if request.method=="GET":
        form=BuscarUsuario(configuracion["AP"])
        tipos=configuracion["tipos"]
        givenname="*"
        sn="*"
    else:
        form=BuscarUsuario(request.POST)
        tipo1=request.POST["clase"]
        if tipo1=='0':
            tipos=configuracion["tipos"]
        else:
            tipos=[int(tipo1)]
        givenname="*" if request.POST["nombre"]=="" else request.POST["nombre"]+"*"
        sn="*" if request.POST["apellidos"]=="" else request.POST["apellidos"]+"*"    
    lista=clase(getLista(givenname,sn,tipos))
    lista.sort(key=operator.itemgetter('uidnumber'))
    lista.sort(key=operator.itemgetter('sn'))
    info={"titulo":configuracion["titulo"],"resultados":lista,'form':form}
    return render(request,"listar.html",info)


def clase(lista):
    resultado=[]
    clase=["","1º ASIR","2º ASIR","1º SMR","2º SMR","Profesor","A.A.","A.P."]
    for usuario in lista:
        usuario["description"][0]=clase[int(usuario["description"][0])]
        resultado.append(usuario)
    return resultado


def getLista(givenname,sn,tipos):
    lldap=LibLDAP()    
    resultado=[]
    for i in tipos:
        busqueda='(&(givenname=%s)(sn=%s)(description=%s))'%(givenname,sn,str(i))
        r=lldap.buscar(busqueda)
        resultado.extend(r)
    lista=[]
    for res in resultado:
        lista.append(res.get_attributes())
    return lista



#############################################################################################################

def addAlumnos(request):
    configuracion={
        "AP":{"AP":"alumnos"},
        "titulo":"Nuevo Alumno"
    }
    return add(request,configuracion)

def addProfesores(request):
    configuracion={
        "AP":{"AP":"profesores"},
        "titulo":"Nuevo Profesor"
    }
    return add(request,configuracion)

def add(request,configuracion):
    test_profesor(request)
    form=newUserForm(configuracion["AP"]) if request.method=="GET" else newUserForm(request.POST)
    
    if form.is_valid():
        # Calcular max uidnumbre
        # Toda la lista desde clase 1 hasta 9
        lista=getLista("*","*",xrange(1,10))
        lista.sort(key=operator.itemgetter('uidnumber'))
        datos=dict(form.data)
        print datos
        del datos["csrfmiddlewaretoken"]
        # Tengo un diccionario donde cada campo es una lista
        # Quito las listas
        datos=quito_listas_en_resultado(datos)

        datos["uidnumber"]=str(int(lista[-1]["uidnumber"][0])+1)
        datos["cn"]=datos["givenname"]+" "+datos["sn"]
        datos["loginshell"]="/bin/bash"
        
        if configuracion["AP"]=="profesores":
            datos["gidnumber"]="2000"
        else:
            datos["gidnumber"]="2001"
        datos["homedirectory"]="/home/%s/%s"%(configuracion["AP"]["AP"],datos["uid"])
        datos["objectclass"]= ['inetOrgPerson', 'posixAccount', 'top']
        the_hash = hashlib.md5(datos["userpassword"]).hexdigest()
        the_unhex = binascii.unhexlify(the_hash)
        datos["userpassword"]="{MD5}"+the_unhex.encode('base64')
        lldap=LibLDAP(request.session["username"],request.session["password"])
        if lldap.isbind:
            try: 
                #lldap.add(datos["uid"],datos)
                print datos
            except:
                messages.add_message(request, messages.INFO, 'No se ha podido añadir el nuevo usuario. Quizás no tengas privilegios, o el nombre de usuario está duplicado.')
                return redirect("/usuarios/%s" % configuracion["AP"]["AP"])
        else:
            messages.add_message(request, messages.INFO, 'No se ha podido añadir el nuevo usuario. Usuario autentificado incorrecto.')
            return redirect("/usuarios/%s" % configuracion["AP"]["AP"])
        messages.add_message(request, messages.INFO, 'Se ha añadido el nuevo usuario.')
        return redirect("/usuarios/%s" % configuracion["AP"]["AP"])
    
    info={"titulo":configuracion["titulo"],'form':form}
    return render(request,"new.html",info)

def update(request,usuario):
    test_profesor(request)
    lldap=LibLDAP()
    busqueda='(uidnumber=%s)'%(usuario)
    print busqueda
    r=lldap.buscar(busqueda)
    datos=r[0].get_attributes()
    datos=quito_listas_en_resultado(datos,utf8=False)
    if not request.POST:
        form=newUserForm(datos)
    else:
        form=newUserForm(request.POST)
    info={'form':form}

    return render(request,"new.html",info)


def quito_listas_en_resultado(datos,utf8=True):
    for campo,valor in datos.items():
        if utf8:
            resultado=valor[0].encode('utf-8')
        else:
            resultado=valor[0]
        del datos[campo]
        datos[campo.encode('utf-8')]=resultado
    return datos
