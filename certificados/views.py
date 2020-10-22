from django.shortcuts import render,redirect,HttpResponse
from .forms import UploadFileFormEquipo,UploadFileFormUsuario
from django.conf import settings
from gestiona_iesgn.views import test_login
from wsgiref.util import FileWrapper
from django.core.mail import EmailMessage
from django.contrib import messages
import os
import os.path
import re
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
				asunto="Petición de certificado de "+tipo+" de " + str(request.session["username"])
				cuerpo="El usuario %s ha subido un fichero csr:%s al programa gestiona, para gestionar la firma de su certificado de %s."%(request.session["username"],request.FILES[campo].name,tipo)
				email = EmailMessage(
 				   asunto,
				   cuerpo,
    				'informatica@gonzalonazareno.org',
				    ['informatica@gonzalonazareno.org'],
				    [],
				    reply_to=['informatica.gonzalonazareno.org'],
				    )
				email.send()
			else:
				messages.add_message(request, messages.INFO, "Tienes que subir un fichero csr...")
			return redirect(settings.SITE_URL+'/cert/')
	else:
		path = os.path.join(settings.BASE_DIR, 'cert/%s'%request.session["username"])
		fil={"usuario":["",""],"equipo":{}}
		for base, dirs, files in os.walk(path):
			if len(files)>0:
				if "equipo" in base:
					num=re.search('.*/equipo/(.*)',base[base.index("/cert"):]).group(1)
					fil["equipo"][num]=["",""]
				for f in files:
					if "usuario" in base:
							if "csr" in f:
								fil["usuario"][0]=settings.SITE_URL+base[base.index("/cert"):],f
							else:
								if "revocar" in f:
									fil["usuario"][1]=settings.SITE_URL+base[base.index("/cert"):],"*"
								else:
									fil["usuario"][1]=settings.SITE_URL+base[base.index("/cert"):],f
					else:
						
						
						if "csr" in f:
							fil["equipo"][num][0]=settings.SITE_URL+base[base.index("/cert"):],f
						else:
							if "revocar" in f:
								fil["equipo"][num][1]=settings.SITE_URL+base[base.index("/cert"):],"*"
							else:
								fil["equipo"][num][1]=settings.SITE_URL+base[base.index("/cert"):],f
	
		form_usuario = UploadFileFormUsuario()
		form_equipo = UploadFileFormEquipo()
		return render(request, 'files.html', {'files': fil,'form_usuario':form_usuario,'form_equipo':form_equipo})
		

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
	with open(path_file, 'wb') as destination:
		destination.write(f.read())

def download(request,usuario,direc="",file=""):
	
	test_login(request)
	if usuario==request.session["username"]:
		if direc=="":
			filename = str(os.path.join(settings.BASE_DIR, 'cert/%s/usuario/%s'%(request.session["username"],file)))
		else:
			filename = str(os.path.join(settings.BASE_DIR, 'cert/%s/equipo/%s/%s'%(request.session["username"],direc,file)))
		f=open(filename,'r')
		wrapper = FileWrapper(f)
		if "csr" in file:
			response = HttpResponse(wrapper, content_type='application/pkcs10')
		if "crt" in file:
			response = HttpResponse(wrapper, content_type='application/x-x509-user-cert')
		response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
		response['Content-Length'] = os.path.getsize(filename)
		return response
	
	else:
		return redirect(settings.SITE_URL+"/")

def revocar(request,usuario,direc="",file=""):
	
	test_login(request)
	if usuario==request.session["username"]:
		if direc=="":
			filename = str(os.path.join(settings.BASE_DIR, 'cert/%s/usuario/%s'%(request.session["username"],file)))
			tipo="usuario"
		else:
			filename = str(os.path.join(settings.BASE_DIR, 'cert/%s/equipo/%s/%s'%(request.session["username"],direc,file)))
			tipo="equipo"
		os.rename(filename,filename+"_revocar")
		asunto="Petición de revocación de certificado de "+tipo+" de " + str(request.session["username"])
		file=str(file)
		cuerpo="El usuario "+str(usuario)+" ha solicitado la revocación de su certificado de "+tipo+":"+file
		email = EmailMessage(
 				   asunto,
				   cuerpo,
    				'informatica@gonzalonazareno.org',
				    ['informatica@gonzalonazareno.org'],
				    [],
				    reply_to=['informatica.gonzalonazareno.org'],
				    )
		email.send()
		return redirect(settings.SITE_URL+'/cert/')		
