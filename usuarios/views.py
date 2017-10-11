# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from usuarios.libldap import LibLDAP,gnLDAP
from usuarios.forms import BuscarUsuario,newUserForm,updateUserForm
from gestiona_iesgn.views import test_profesor
from django.contrib import messages

import binascii
import hashlib


def listarAlumnos(request):
    configuracion={
        "AP":{"AP":"alumnos"},
        "titulo":"Listado de Alumnos"
    }
    return listarUsuarios(request,configuracion)

def listarProfesores(request):
    configuracion={
        "AP":{"AP":"profesores"},
        "titulo":"Listado de Profesores"
    }
    return listarUsuarios(request,configuracion)


def listarUsuarios(request,configuracion):
    test_profesor(request)
    filtro={}
    ldap=gnLDAP()
    if request.method=="GET":
        form=BuscarUsuario(configuracion["AP"])
        filtro["givenname"]=""
        filtro["sn"]=""
    else:
        form=BuscarUsuario(request.POST)
        filtro["grupo"]=request.POST["grupo"]
        filtro["givenname"]="" if request.POST["nombre"]=="" else request.POST["nombre"]
        filtro["sn"]="" if request.POST["apellidos"]=="" else request.POST["apellidos"]    
    lista=ldap.gnBuscar(filtro=filtro)
    lsita=getGrupo(lista)
    info={"titulo":configuracion["titulo"],"resultados":lista,'form':form}
    return render(request,"listar.html",info)


def getGrupo(lista):
    resultado=[]
    grupo={'asir1':'1º ASIR',
    'asir2':'2º ASIR',
    'smr1':'1º SMR',
    'smr2':'2º SMR',
    'antiguosalumnos':'A.A.',
    'profesores':'Profesor',
    'antiguosprofesores':'A.P.'}
    ldap=gnLDAP(base_dn="ou=Group,dc=gonzalonazareno,dc=org")
    for usuario in lista:
        lista=ldap.gnBuscar(cadena="(member=uid=%s,ou=People,dc=gonzalonazareno,dc=org)" % usuario["uid"][0])
        usuario["description"][0]=lista
        resultado.append(usuario)
    return resultado





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

        #lista=getLista("*","*",xrange(1,10))
        #lista.sort(key=operator.itemgetter('uidnumber'))
        
        datos=dict(form.data)
        del datos["csrfmiddlewaretoken"]
        del datos["AP"]
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
                lldap.add(datos["uid"],datos)
            except Exception as err:
                messages.add_message(request, messages.INFO, 'No se ha podido añadir el nuevo usuario. Error:' + str(err))
                return redirect("/usuarios/%s" % configuracion["AP"]["AP"])
        else:
            messages.add_message(request, messages.INFO, 'No se ha podido añadir el nuevo usuario. Usuario autentificado incorrecto.')
            return redirect("/usuarios/%s" % configuracion["AP"]["AP"])
        messages.add_message(request, messages.INFO, 'Se ha añadido el nuevo usuario.')
        return redirect("/usuarios/%s" % configuracion["AP"]["AP"])
    
    info={"titulo":configuracion["titulo"],'form':form}
    return render(request,"new.html",info)

####################################################################################################


def update(request,usuario):
    if not "perfil" in request.path: 
        test_profesor(request)
    lldap=LibLDAP()
    busqueda='(uidnumber=%s)'%(usuario)
    r=lldap.buscar(busqueda)
    datos=r[0].get_attributes()
    datos=quito_listas_en_resultado(datos,utf8=False)
    if datos["gidnumber"]=='2000':
        configuracion={
        "titulo":"Modificar Profesor",
        "AP":"profesores",
        }

    else:
        configuracion={
        "titulo":"Modificar Alumno",
        "AP":"alumnos",
        }
    datos["AP"]=configuracion["AP"]
    form=updateUserForm(datos) if request.method=="GET" else updateUserForm(request.POST)
    if request.method=="POST" and form.is_valid():
        new=dict(form.data)
        del new["csrfmiddlewaretoken"]
        del new["AP"]
        del datos["AP"]
        # Tengo un diccionario donde cada campo es una lista
        # Quito las listas
        new=quito_listas_en_resultado(new)
        old={}
        new["cn"]=new["givenname"]+" "+new["sn"]
        if new["userpassword"]!='':
            the_hash = hashlib.md5(new["userpassword"]).hexdigest()
            the_unhex = binascii.unhexlify(the_hash)
            new["userpassword"]="{MD5}"+the_unhex.encode('base64')
        else:
            the_hash = hashlib.md5(request.session["password"]).hexdigest()
            the_unhex = binascii.unhexlify(the_hash)
            new["userpassword"]="{MD5}"+the_unhex.encode('base64')
        the_hash = hashlib.md5(request.session["password"]).hexdigest()
        the_unhex = binascii.unhexlify(the_hash)
        datos["userpassword"]="{MD5}"+the_unhex.encode('base64')
        
        for campo in new.keys():
            if new[campo]==datos[campo]:
                del new[campo]
        for campo in new:
            old[campo]=datos[campo]
        
        ### Obtengo path de retorno
        if "perfil" in request.path:
            url="/"
        else:
            url="/usuarios/"+configuracion["AP"]

        ##3 Hago la modificación
        lldap=LibLDAP(request.session["username"],request.session["password"])
        if lldap.isbind:
            try: 
                lldap.modify(datos["uid"],new,old)
            except Exception as err:
                messages.add_message(request, messages.INFO, 'No se ha podido modificar el usuario. Error'+str(err))
                return redirect("%s" % url)
        else:
            messages.add_message(request, messages.INFO, 'No se ha podido modificar el usuario. Usuario autentificado incorrecto.')
            return redirect("%s" % url)

        messages.add_message(request, messages.INFO, 'Se ha modificado el usuario.')
        return redirect("%s" % url)

    configuracion["titulo2"]="Si no escribes ninguna contraseña se mantendrá la que el usuario posee actualmente."
    info={'titulo':configuracion["titulo"],'titulo2':configuracion["titulo2"],'form':form}
    if "perfil" in request.path:
        info["perfil"]=True
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

def perfil(request):
    lldap=LibLDAP()
    busqueda='(uid=%s)'%(request.session["username"])
    r=lldap.buscar(busqueda)
    datos=r[0].get_attributes()
    return update(request,datos["uidnumber"][0])