from django.shortcuts import render,redirect
from django.contrib.staticfiles.views import serve
from django.http import Http404
from django.conf import settings
import os
import markdown

def actualizar(request):
    path = os.path.join(settings.STATICFILES_DIRS[0], 'content_iesgn/')
    os.system("cd %s && git pull" % path)
    return redirect(settings.SITE_URL)

def doc(request,tipo):
    
    visibility="public"
    
    if request.session.get("username"):
        visibility="auth"
    
    if request.session.get("profesor"):
        visibility="profesor"
    datos=getInfoVisibility(tipo,visibility)
    if len(datos)==0:
        raise Http404 
    info={"datos":datos,"tipo":tipo}
    if tipo=="documentacion":
        return render(request,"listardoc.html",info)
    if tipo=="blog":
        return render(request,"listarblog.html",info)
    if tipo=="noticias":
        return render(request,"listarnoticias.html",info)
    

def show(request,tipo,url):
    dato=getDoc(tipo,url,request.session)
    if dato==None:
        try:
            return serve(request, 'content_iesgn'+"/"+tipo+"/"+url)
        except:
            raise Http404
    info={"dato":dato,"tipo":tipo}
    return render(request,"mostrardoc.html",info)


def getInfo(tipo):
    path = os.path.join(settings.STATICFILES_DIRS[0], 'content_iesgn/%s/'%tipo)
    datos=[]
    for root, dirs, files in os.walk(path):
        for file in files:
            if root==path:
                with open(path+file, "r", encoding="utf-8") as input_file:
                    text = input_file.read()
                md = markdown.Markdown(extensions = ['meta'])
                html = md.convert(text)
                meta=md.Meta
                datos.append({"html":html,"meta":meta})
    datos.sort(key=lambda item:int(item['meta']['order'][0]), reverse=True)
    return datos

def getDoc(tipo,url,session):
    datos=getInfo(tipo)
    for dato in datos:
        if dato.get("meta").get("url")[0]==url:
            if dato.get("meta").get("visibility")[0]=="public":
                return dato
            elif dato.get("meta").get("visibility")[0]=="auth" and session.get("username"):
                return dato
            elif dato.get("meta").get("visibility")[0]=="profesor" and session.get("profesor"):
                return dato
    return None

def getInfoVisibility(tipo,visibility):
    datos=getInfo(tipo)
    respuesta=[]
    for dato in datos:
        if visibility=="profesor":
            respuesta.append(dato)
        elif visibility=="auth" and (dato.get("meta").get("visibility")[0]=="auth" or dato.get("meta").get("visibility")[0]=="public"):
            respuesta.append(dato)
        elif visibility=="public" and dato.get("meta").get("visibility")[0]=="public":
            respuesta.append(dato)
            
    return respuesta

    

