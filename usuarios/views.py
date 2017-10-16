# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from usuarios.libldap import LibLDAP,gnLDAP
from usuarios.forms import BuscarUsuario,newUserForm,updateUserForm,deleteUserForm,deleteUserForm2
from gestiona_iesgn.views import test_profesor,test_login
from django.contrib import messages

import binascii
import hashlib


def listarAlumnos(request):
    configuracion={
        "grupo":"alumnos",
        "AP":{"AP":"alumnos"},
        "titulo":"Listado de Alumnos"
    }
    return listarUsuarios(request,configuracion)

def listarProfesores(request):
    configuracion={
        "grupo":"allprofesores",
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
        filtro["grupo"]=configuracion["grupo"]
        filtro["givenname"]=""
        filtro["sn"]=""
    else:
        form=BuscarUsuario(request.POST)
        filtro["grupo"]=request.POST["grupo"]
        filtro["givenname"]="" if request.POST["nombre"]=="" else request.POST["nombre"]
        filtro["sn"]="" if request.POST["apellidos"]=="" else request.POST["apellidos"]    
    lista=ldap.gnBuscar(filtro=filtro)
    lista=getGrupo(lista)
    info={"titulo":configuracion["titulo"],"resultados":lista,'form':form}

    
    
    return render(request,"listar.html",info)


def getGrupo(lista):
    resultado=[]

    ldap=gnLDAP()
    for usuario in lista:
        usuario["grupo"]=ldap.memberOfGroup(usuario["uid"][0])
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
        # Toda la lista desde clase 1 hasta 9 ####

        ldap=gnLDAP(request.session["username"],request.session["password"])
        lista=ldap.gnBuscar(cadena="(cn=*)",ordenarpor="udinumber")
        datos=dict(form.data)
        grupo=datos["grupo"][0]
        del datos["csrfmiddlewaretoken"]
        del datos["AP"]
        del datos["grupo"]

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
        if ldap.isbind:
            ldap.modUserGroup(datos["uid"],grupo,"add")
            try: 
                
                ldap.add(datos["uid"],datos)
      
                
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
    ldap=gnLDAP(request.session["username"],request.session["password"])
    lista=ldap.gnBuscar(cadena="(uid=%s)"%usuario)
    if len(lista)==0:
        return redirect("/")
    datos=quito_listas_en_resultado(lista[0],utf8=False)
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
    datos["grupo"]=ldap.memberOfGroup(usuario,key=True)
    form=updateUserForm(datos) if request.method=="GET" else updateUserForm(request.POST)
    if request.method=="POST" and form.is_valid():
        new=dict(form.data)
        grupo=new["grupo"]
        del new["csrfmiddlewaretoken"]
        del new["AP"]
        del new["grupo"]
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
        
        if ldap.isbind:
            oldgrupo=ldap.memberOfGroup(datos["uid"],key=True)

            
            try: 
                
                if str(grupo[0])!=oldgrupo:
                    ldap.modUserGroup(datos["uid"],grupo[0],"add")
                    ldap.modUserGroup(datos["uid"],oldgrupo,"del")
                ldap.modify(datos["uid"],new,old)
                
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
    test_login(request)
    lldap=gnLDAP()
    busqueda='(uid=%s)'%(request.session["username"])
    datos=lldap.gnBuscar(cadena=busqueda)
    return update(request,datos[0]["uid"][0])

###########################################################################################################

def delete(request):
    test_login(request)
    if request.method=="POST" and request.POST.get("uid",False):
        uid=request.POST["uid"]
        lldap=gnLDAP()
        busqueda='(uid=%s)'%(uid)
        datos=lldap.gnBuscar(cadena=busqueda)
        grupo=lldap.memberOfGroup(uid,key=True)
        if grupo=="profesores" or grupo=="antiguosprofesores":
            info={"error":"No se puede borrar un profesor."}
        elif len(datos)==0:
            info={"error":"No existe ese usuario"}
        else:
            form=deleteUserForm2({'uiddel':uid})
            info={'form':form,'grupo':lldap.memberOfGroup(uid),'nombre':datos[0]["cn"][0]}
        return render(request,"delete.html",info)
    elif request.method=="POST" and request.POST.get("uiddel",False):
        if request.POST["confirmar"]=="no":
            return redirect("/")
        if request.POST["confirmar"]=="si":
            info={"error":"Usuario borrado con éxito."}
            return render(request,"delete.html",info)


    else:
        form=deleteUserForm()
        info={'form':form}
        return render(request,"delete.html",info)