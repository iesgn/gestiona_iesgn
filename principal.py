from bottle import route, template, run, static_file, error,request,response,redirect,error
from wtforms import Form, BooleanField, StringField, validators
import sesion
from gestiona import *
from libldap import LibLDAP


@route('/')
def index():
    return my_template("index.tpl")

@route('/login',method="post")
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    lldap=LibLDAP(username,password)

    if lldap.isbind:
        sesion.set(username)
        redirect('/')
    else:
        info={"error":True}
        return my_template('index.tpl',info=info)

@route('/logout')
def do_logout():
    sesion.delete()
    redirect('/')


@route('/usuarios')
def usuarios():
    if sesion.islogin():
        info={}
        if(request.GET):
            tipo="*" if request.GET.get("t")=="0" else request.GET.get("t")
            givenname="*" if request.GET.get("q") is None else request.GET.get("q")
            busqueda='(&(givenname=%s)(description=%s))'%(givenname,tipo)
            info["params"]={"q":givenname,"t":tipo}
        else:
            busqueda='(givenname=*)'
            info["params"]={"q":"","t":""}
        lldap=LibLDAP()
        resultados=lldap.buscar(busqueda)
        info["resultados"]=resultados
        
        return my_template('usuarios.tpl',info=info)
    else:
        redirect('/')



@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')


@error(404)
def error404(error):
    return "Nada"

run(host='0.0.0.0', port=80)
