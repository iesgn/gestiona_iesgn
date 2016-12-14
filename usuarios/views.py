from django.shortcuts import render,redirect
from usuarios.libldap import LibLDAP

# Create your views here.
def listar(request):
    if request.session.get("profesor",False):
        tipo="1"
        givenname="*"
        busqueda='(&(givenname=%s)(description=%s))'%(givenname,tipo)
        lldap=LibLDAP()
        resultados=lldap.buscar(busqueda)
        lista=[]
        for res in resultados:
            lista.append(res.get_attributes())
        info={"resultados":lista}
        return render(request,"listar.html",info)
    else:
        return redirect('/')
