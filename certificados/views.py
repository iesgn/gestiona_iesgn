# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse
from .forms import UploadFileFormEquipo,UploadFileFormUsuario
from django.conf import settings
from gestiona_iesgn.views import test_login
from wsgiref.util import FileWrapper
from django.core.mail import EmailMessage
from django.contrib import messages
import os
import os.path
# Create your views here.

def add(request):
	test_login(request)
	if request.method == 'POST':
		if "csr_equipo" in request.FILES:
			form = UploadFileFormEquipo(request.POST, request.FILES)
			campo="csr_equipo"
			tipo="equipo"
		else:
			form = UploadFileFormUsuario(request.POST, request.FILES)
			campo="csr_usuario"
			tipo="usuario"
		if form.is_valid():
			if request.FILES[campo].content_type=="application/pkcs10":
				handle_uploaded_file(request.FILES[campo],request.session["username"],tipo)
				#asunto="Petición de certificado de "+tipo+" de " + str(request.session["username"])
#				cuerpo="El usuario %s ha subido un fichero csr:%s al programa gestiona, para gestionar la firma de su certificado de %s."%(request.session["username"],request.FILES[campo].name,tipo)
#				email = EmailMessage(
# 				   asunto,
#				   cuerpo,
#    				'informatica@gonzalonazareno.org',
#				    ['informatica@gonzalonazareno.org'],
#				    [],
#				    reply_to=['informatica.gonzalonazareno.org'],
#				    )
#				email.send()
			else:
				messages.add_message(request, messages.INFO, "Tienes que subir un fichero csr...")
			return redirect(settings.SITE_URL+'/certificados')
	else:
		path = os.path.join(settings.BASE_DIR, 'cert/%s'%request.session["username"])
		files["usuario"]=[]
		files["equipo"]=[]
		for base, dirs, files in os.walk('cert/josedom'):
			if len(files)>0:
				for f in files:
					if "usuario" in base:
							if "csr" in f:
								files["usuario"].insert(0,base+"/"+f)
							else:
								files["usuario"].insert(1,base+"/"+f)
					else:
						if "csr" in f:
							files["equipo"].insert(0,base+"/"+f)
						else:
							files["equipo"].insert(1,base+"/"+f)
		print files

		form_usuario = UploadFileFormUsuario()
		form_equipo = UploadFileFormEquipo()
		return render(request, 'files.html', {'files': files,'form_usuario':form_usuario,'form_equipo':form_equipo})
		

def handle_uploaded_file(f,nombre,tipo):
	path= os.path.join(settings.BASE_DIR, 'cert/%s/%s'%(nombre,tipo))
	
	if tipo=="equipo":
		try:
			dirs=os.listdir(path)
		except:
			dirs=[]
		if len(dirs)==0:
			dir=1
		else:
			dirs=map(int,dirs)
			dir=max(dirs)+1
		path=path+"/"+str(dir)
	if not os.path.isdir(path):
		os.makedirs(path)
	
	path_file=path+"/"+f.name
	with open(path_file, 'w') as destination:
		destination.write(f.read())

def download(request,usuario,file):
	test_login(request)
	if usuario==request.session["username"]:
		filename = str(os.path.join(settings.BASE_DIR, 'cert/%s'%(request.session["username"]+"/"+file)))
		print "*"*20
		print filename
		f=open(filename,'r')
		wrapper = FileWrapper(f)
		response = HttpResponse(wrapper, content_type='text/plain')
		response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
		response['Content-Length'] = os.path.getsize(filename)
		return response
	else:
		return redirect(settings.SITE_URL)