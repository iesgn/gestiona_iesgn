# -*- coding: utf-8 -*-
from django.shortcuts import render
from correos.forms import CorreoForm,BuscarDestinatariosForm
from usuarios.libldap import gnLDAP


# Create your views here.
def add(request):
	if request.method=='POST' and not request.POST.has_key("correo"):
		form2 = BuscarDestinatariosForm(dest=SelectUsuarios(request.POST.get("alumnos"))+request.POST.get("destinatarios"),alum=request.POST.get("alumnos"))
		info={}
		info["asunto"]=request.POST.get("asunto")
		info["contenido"]=request.POST.get("contenido")		
		
		form = CorreoForm(request.POST)
#    elif request.method=='POST' and request.POST.has_key("correo"):
#        form2 = BuscarDestinatariosForm(request.POST.get("Profesores")) 
#        form = CorreoForm(request.POST)
#        if form.is_valid():
#            form.save()
#            correos=[]
#            for prof in request.POST["Destinatarios"]:
#                correos.append(Profesores.objects.get(id=prof).Email)
#

#            #send_mail(
#                   request.POST["Asunto"],
#                   request.POST["Contenido"],
#                   '41011038.edu@juntadeandalucia.es',
#                 #  'josedom24@gmail.com',
#                   correos,
#                   fail_silently=False,
#                  )
#            return redirect('/correo/list')
	else:
   
		form = CorreoForm()
		form2 = BuscarDestinatariosForm(dest=[],alum="")

	info={'form2':form2,'form':form}
	return render(request, 'add_correos.html',info)

def SelectUsuarios(grupo):
	ldap=gnLDAP()
	filtro={"grupo":grupo}
	lista=ldap.gnBuscar(filtro=filtro)
	lista2=[]
	for usuario in lista:
		lista2.append(usuario["uid"][0])
	return lista2

#    cursos=Cursos.objects.all().order_by("Curso")
#    departamentos=Departamentos.objects.all().order_by("Nombre")
#    areas=Areas.objects.all().order_by("Nombre")
#    if id==0:
#        return Profesores.objects.none()
#    if id==1:
#        return Profesores.objects.all()
#    if id==2:
#        return Profesores.objects.filter(Etcp=1)
#    if id==3:
#        return Profesores.objects.filter(Ce=1)
#    if id==4:
#        return Profesores.objects.filter(Bil=1)
#    if id>=5 and id<=21:
#        return [Cursos.objects.get(Curso=cursos[id-5].Curso).Tutor]
#    if id>=22 and id<=38:
#        return Cursos.objects.get(Curso=cursos[id-22].Curso).EquipoEducativo.all()
#    if id>=39 and id<=58:
#        return Profesores.objects.filter(Departamento=departamentos[id-39].id)
#    if id>=59 and id<=62:
#        lista=[]
#        for dep in Areas.objects.get(id=areas[id-59].id).Departamentos.all():
#            lista.extend(Profesores.objects.filter(Departamento=dep.id))
#        return lista
#    return Profesores.objects.none()#

