from django.shortcuts import render,redirect
from correos.forms import CorreoForm,BuscarDestinatariosForm
from usuarios.libldap import LibLDAP

from django.core.mail import EmailMessage
from django.conf import settings
from gestiona_iesgn.views import test_profesor

# Create your views here.
def add(request):
	test_profesor(request)
	if request.method=='POST' and "correo" not in request.POST:
		form2 = BuscarDestinatariosForm(dest=SelectUsuarios(request.POST.get("usuarios")),alum=request.POST.get("usuarios"))
		form = CorreoForm(request.POST)
	elif request.method=='POST' and "correo" in request.POST:
		
		form2 = BuscarDestinatariosForm(dest=SelectUsuarios(request.POST.get("usuarios")),alum=request.POST.get("usuarios"))
		form = CorreoForm(request.POST)	

		if form.is_valid():
			lldap=LibLDAP()
			correos=[]
			for usuario in request.POST.getlist("destinatarios"):
				busqueda='(uid=%s)'%(usuario)
				datos=lldap.buscar(busqueda,["mail"])
				correos.append(datos[0]["mail"][0])
			replayto="informatica.gonzalonazareno.org" if request.POST.get("replyto")=="" else request.POST.get("replyto")
			email = EmailMessage(
 				   request.POST["asunto"],
				   request.POST["contenido"],
    				'informatica@gonzalonazareno.org',
				    ['informatica@gonzalonazareno.org'],
				    correos,
				    reply_to=[replayto],
				    )
			email.send()
			lldap.logout()
			return redirect(settings.SITE_URL+'/')
	else:
		lldap=LibLDAP()
		busqueda='(uid=%s)'%(request.session["username"])
		datos=lldap.buscar(busqueda,["mail"])
		form = CorreoForm({"replyto":datos[0]["mail"][0]})
		form2 = BuscarDestinatariosForm(dest=[],alum="")
		lldap.logout()

	info={'form2':form2,'form':form}
	return render(request, 'add_correos.html',info)

def SelectUsuarios(grupo):
	if grupo=="0":
		return []
	else:
		filtro={"grupo":grupo}	
	ldap=LibLDAP()
	filtro=ldap.conv_filtro(filtro)
	lista=ldap.buscar(filtro,"uid")
	lista2=[]
	for usuario in lista:
		lista2.append(usuario["uid"][0])
	return lista2
