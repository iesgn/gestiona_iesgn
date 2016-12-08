from django.shortcuts import render,redirect
from usuarios.libldap import LibLDAP 

def index(request):
    if request.method=="GET":
            return render(request,'index.html')
    else:
        username = request.POST["username"]
        password = request.POST["password"].encode('utf-8')
        lldap=LibLDAP(username,password)
        if lldap.isbind:
                request.session["username"]=username
                request.session["password"]=password
                busqueda='(uid=%s)'%username
                resultados=lldap.buscar(busqueda)
                info=resultados[0].get_attributes()
                return render(request,"index.html")
        else:
               info={"error":True}
               return render(request,"index.html",info)

def salir(request):
    del request.session["username"]
    del request.session["password"]
    return redirect('/')

