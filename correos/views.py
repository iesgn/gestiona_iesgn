# -*- coding: utf-8 -*-
from django.shortcuts import render
from correos.forms import CorreoForm,BuscarDestinatariosForm

# Create your views here.
def add(request):
    #if request.method=='POST' and not request.POST.has_key("correo"):
#        form2 = BuscarDestinatariosForm(request.POST)
#        form = CorreoForm({'Asunto':request.POST.get("Asunto"),'Contenido':request.POST.get("Contenido"),'Destinatarios':SelectProfes(int(request.POST.get("Profesores"))),'Fecha':time.strftime("%d/%m/%Y")})#

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
#    else:
    form = CorreoForm({'Destinatarios':[]})
    form2 = BuscarDestinatariosForm()
    info={'form2':form2,'form':form}
    return render(request, 'add_correos.html',info)

#def SelectProfes(id):
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
