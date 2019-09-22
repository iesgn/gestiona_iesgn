from django.shortcuts import render,redirect
from usuarios.libldap import LibLDAP
from usuarios.forms import BuscarUsuario,newUserForm,updateUserForm,deleteUserForm,deleteUserForm2
from gestiona_iesgn.views import test_profesor,test_login
from django.contrib import messages
from django import forms
from django.conf import settings

import binascii
import hashlib
import base64


def listarUsuarios(request):
    test_profesor(request)
    filtro={}
    ldap=LibLDAP()
    if request.method=="GET":
        form=BuscarUsuario()
        filtro["grupo"]='all'
        filtro["givenName"]=""
        filtro["sn"]=""
    else:
        form=BuscarUsuario(request.POST)
        filtro["grupo"]=request.POST["grupo"]
        filtro["givenName"]="" if request.POST["nombre"]=="" else request.POST["nombre"]
        filtro["sn"]="" if request.POST["apellidos"]=="" else request.POST["apellidos"]    
    filtro=ldap.conv_filtro(filtro)
    lista=ldap.buscar(filtro,["sn","uid","givenname"])
    ldap.logout()
    lista=sorted(lista,key=lambda d: d["sn"])
    lista=getGrupo(lista)
    info={"resultados":lista,'form':form}
    return render(request,"listar.html",info)


def getGrupo(lista):
    resultado=[]

    ldap=LibLDAP()
    for usuario in lista:
        usuario["grupo"]="<br/>".join(ldap.memberOfGroup(usuario["uid"][0]))
        resultado.append(usuario)
    return resultado

#############################################################################################################


def add(request):
    test_profesor(request)
    form=newUserForm() if request.method=="GET" else newUserForm(request.POST)
    
    if form.is_valid():
        # Calcular max uidnumbre
        # Toda la lista desde clase 1 hasta 9 #####
        ldap=LibLDAP(request.session["username"],request.session["password"])
        lista=ldap.buscar("(cn=*)",["uidNumber"])
        lista=sorted(lista,key=lambda d: d["uidNumber"])

        datos=dict(form.data)
        grupo=datos["grupo"][0]
        del datos["csrfmiddlewaretoken"]
        del datos["grupo"]#
        # Tengo un diccionario donde cada campo es una lista
        # Quito las listas
        datos=quito_listas_en_resultado(datos)#
        datos["uidNumber"]=str(int(lista[-1]["uidNumber"][0])+1)
        datos["cn"]=datos["givenName"]+" "+datos["sn"]
        datos["loginshell"]="/bin/bash"
        
        if grupo=="profesores":
            datos["gidNumber"]="2000"
            directory="profesores"
        else:
            datos["gidNumber"]="2001"
            directory="alumnos"
        datos["homedirectory"]="/home/%s/%s"%(directory,datos["uid"])
        datos["objectclass"]= ['inetOrgPerson', 'posixAccount', 'top']
        the_hash = hashlib.md5(datos["userPassword"].encode('utf-8')).hexdigest()
        the_unhex = binascii.unhexlify(the_hash)
        datos["userPassword"]="{MD5}"+base64.b64encode(the_unhex).decode("utf-8")
        if ldap.isbind:
            mensaje='Se ha añadido el nuevo usuario.'    
            try: 
                ldap.add(datos["uid"],datos)
                ldap.modUserGroup(datos["uid"],grupo,"add")
            except Exception as err:
                mensaje='No se ha podido añadir el nuevo usuario. Error:' + str(err)
        else:
            mensaje='No se ha podido añadir el nuevo usuario. Usuario autentificado incorrecto.'
        messages.add_message(request, messages.INFO, mensaje)
        return redirect(settings.SITE_URL+"/usuarios/")
    
    info={'form':form}
    return render(request,"new.html",info)

######################################################################################################
#

def update(request,usuario):
    if not "perfil" in request.path: 
        test_profesor(request)
    ldap=LibLDAP(request.session["username"],request.session["password"])
    lista=ldap.buscar("(uid=%s)"%usuario,["uid","cn","givenName","loginShell","userPassword","l","sn","homeDirectory","mail"])
    if len(lista)==0:
        return redirect(settings.SITE_URL+"/")
    datos=quito_listas_en_resultado(lista[0])
    form=updateUserForm(datos) if request.method=="GET" else updateUserForm(request.POST)
    if request.method=="POST" and form.is_valid():
        new=dict(form.data)
    
        del new["csrfmiddlewaretoken"]

        # Tengo un diccionario donde cada campo es una lista
        # Quito las listas
        new=quito_listas_en_resultado(new)

        new["cn"]=new["givenName"]+" "+new["sn"]
        if new["userPassword"]!='':
            nuevapass=new["userPassword"]
            the_hash = hashlib.md5(new["userPassword"].encode('utf-8')).hexdigest()
            the_unhex = binascii.unhexlify(the_hash)
            new["userPassword"]="{MD5}"+base64.b64encode(the_unhex).decode("utf-8")
        else:
            the_hash = hashlib.md5(request.session["password"].encode('utf-8')).hexdigest()
            the_unhex = binascii.unhexlify(the_hash)
            new["userPassword"]="{MD5}"+base64.b64encode(the_unhex).decode("utf-8")
        the_hash = hashlib.md5(request.session["password"].encode('utf-8')).hexdigest()
        the_unhex = binascii.unhexlify(the_hash)
        datos["userPassword"]="{MD5}"+ base64.b64encode(the_unhex).decode("utf-8")
        
        for campo in list(new):
            if new[campo]==datos[campo]:
                del new[campo]
        
        ### Obtengo path de retorno
        if "perfil" in request.path:
            url=settings.SITE_URL+"/"
        else:
            url=settings.SITE_URL+"/usuarios/"
        ##3 Hago la modificación
        
        if ldap.isbind:
            
            #try: 
                
            ldap.modify(datos["uid"],new)
            try:
                request.session["password"]=nuevapass
            except:
                pass
                
            #except Exception as err:
            #    messages.add_message(request, messages.INFO, 'No se ha podido modificar el usuario. Error'+str(err))
            #    return redirect("%s" % url)
        else:
            messages.add_message(request, messages.INFO, 'No se ha podido modificar el usuario. Usuario autentificado incorrecto.')
            return redirect("%s" % url)#
        messages.add_message(request, messages.INFO, 'Se ha modificado el usuario.')
        return redirect("%s" % url)#
    
    info={'form':form}
    return render(request,"update.html",info)

def quito_listas_en_resultado(datos):
    datos2={}
    for campo,valor in datos.items():
        if type(valor)==list and len(valor)==1:
            resultado=valor[0]
        else:
            resultado=valor

        datos2[campo]=resultado
    return datos2#
def perfil(request):
    test_login(request)
    lldap=LibLDAP()
    busqueda='(uid=%s)'%(request.session["username"])
    datos=lldap.gnBuscar(cadena=busqueda)
    return update(request,datos[0]["uid"][0])#

#############################################################################################################

def delete(request):
    test_login(request)
    if request.method=="POST" and request.POST.get("uid",False):
        uid=request.POST["uid"]
        ldap=LibLDAP()
        busqueda='(uid=%s)'%(uid)
        datos=ldap.buscar(busqueda,["cn"])
        grupo=ldap.memberOfGroup(uid,key=True)
        
        if grupo=="profesores" or grupo=="antiguosprofesores":
            info={"error":"No se puede borrar un profesor."}
        elif len(datos)==0:
            info={"error":"No existe ese usuario"}
        else:
            if len(grupo)==0:
                grupo="Sin grupo"
            else:
                grupo=ldap.memberOfGroup(uid)
            form=deleteUserForm2({'uiddel':uid})
            info={'form':form,'grupo':grupo,'nombre':datos[0]["cn"][0]}
        return render(request,"delete.html",info)
    elif request.method=="POST" and request.POST.get("uiddel",False):
        if request.POST["confirmar"]=="no":
            return redirect(settings.SITE_URL+"/")
        if request.POST["confirmar"]=="si":
            ldap=LibLDAP(request.session["username"],request.session["password"])
            grupos=ldap.memberOfGroup(request.POST["uiddel"],key=True)
            
            try:
                for grupo in grupos:
                    ldap.modUserGroup(str(request.POST["uiddel"]),grupo,"del")
                ldap.delete(request.POST["uiddel"])
                
                info={"error":"Usuario borrado con éxito."}
            except Exception as err:
                info={"error":'No se ha podido borrar el usuario. Error'+str(err)}#
            return render(request,"delete.html",info)#

    else:
        form=deleteUserForm()
        info={'form':form}
        return render(request,"delete.html",info)