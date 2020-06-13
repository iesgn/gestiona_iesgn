from django.shortcuts import render
from django.http import Http404
from gestiona_iesgn.views import test_profesor,test_login
from django.conf import settings
import os
import markdown

def doc(request,tipo):
	#datos=getInfo(tipo)
	datos=getInfoVisibility(tipo,"public")
	if len(datos)==0:
		raise Http404 
	info={"datos":datos,"tipo":tipo}
	return render(request,"listardoc.html",info)

def show(request,tipo,url):
	dato=getDoc(tipo,url,request.session)
	if dato==None:
		raise Http404 
	info={"dato":dato,"tipo":tipo}
	return render(request,"mostrardoc.html",info)


def getInfo(tipo):
	path = os.path.join(settings.STATICFILES_DIRS[0], 'content_iesgn/%s/'%tipo)
	datos=[]
	for root, dirs, files in os.walk(path):
		for file in files:
			with open(path+file, "r", encoding="utf-8") as input_file:
				text = input_file.read()
			md = markdown.Markdown(extensions = ['meta'])
			html = md.convert(text)
			meta=md.Meta
			datos.append({"html":html,"meta":meta})
	print(datos)
	datos.sort(key=lambda item:int(item['meta']['order'][0]), reverse=True)
	return datos

def getDoc(tipo,url,session):
	datos=getInfo(tipo)
	for dato in datos:
		if dato.get("meta").get("url")[0]==url:
			if dato.get("meta").get("visibility")[0]=="public":
				return dato
			elif dato.get("meta").get("visibility")[0]=="auth" and session.username:
				return dato
			elif dato.get("meta").get("visibility")[0]=="profesor" and session.profesor:
				return dato
	return None

def getInfoVisibility(tipo,visibility):
	datos=getInfo(tipo)
	respuesta=[]
	for dato in datos:
		if dato.get("meta").get("visibility")[0]==visibility:
			respuesta.append(dato)
	return respuesta



