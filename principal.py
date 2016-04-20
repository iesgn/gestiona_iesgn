from bottle import app, route, template, run, static_file, error,request,response,redirect,error
import sesion
from gestiona import *
from libldap import LibLDAP
from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(app(), session_opts)


@route('/')
def index():
    return my_template("index.tpl")

@route('/login',method="post")
def do_login():
    
    username = request.forms.get('username')
    password = request.forms.get('password')
    lldap=LibLDAP(username,password)

    if lldap.isbind:
        sesion.set("user",username) 
        sesion.set("pass",password)    
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
        busqueda='(givenname=*)'
        info["params"]={"q":"","t":"0"}
        
        lldap=LibLDAP()
        resultados=lldap.buscar(busqueda)
        info["resultados"]=resultados
        
        return my_template('usuarios.tpl',info=info)
    else:
        redirect('/')

@route('/usuarios',method='post')
def usuarios2():
    if sesion.islogin():
        info={}
        tipo="*" if request.forms.get("t")=="0" or request.forms.get("t") is None else request.forms.get("t")
        givenname="*" if request.forms.get("q") is None else request.forms.get("q")+"*"
        busqueda='(&(givenname=%s)(description=%s))'%(givenname,tipo)
        givenname=givenname[:-1]
        info["params"]={"q":givenname,"t":tipo}
        lldap=LibLDAP()
        resultados=lldap.buscar(busqueda)
        info["resultados"]=resultados
        
        return my_template('usuarios.tpl',info=info)
    else:
        redirect('/')



@route('/usuarios/add')
def add():
    if sesion.islogin():
        return my_template('add.tpl')
    else:
        redirect('/')


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')


@error(404)
def error404(error):
    return "Nada"

run(app=app,host='0.0.0.0', port=8080,reloader=True)
