from bottle import app, route, template, run, static_file, error,request,response,redirect,error
#from sesion import Sesion
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
    #s=Sesion()
    #s.start()

    return my_template("index.tpl")

@route('/login',method="post")
def do_login():
    #s=Sesion()
    #s.load()
    username = request.forms.get('username')
    password = request.forms.get('password')
    lldap=LibLDAP(username,password)

    if lldap.isbind:
        s = request.environ.get('beaker.session')
        s["user"]=username
        #s.set("user",username)
        redirect('/')
    else:
        info={"error":True}
        return my_template('index.tpl',info=info)

@route('/logout')
def do_logout():
    #s=Sesion()
    #s.delete()
    redirect('/')


@route('/usuarios')
def usuarios():
    if sesion.islogin():
        info={}
        tipo="*" if request.forms.get("t")=="0" or request.forms.get("t") is None else request.forms.get("t")
        givenname="*" if request.forms.get("q") is None else request.forms.get("q")+"*"
        busqueda='(&(givenname=%s)(description=%s))'%(givenname,tipo)
        print busqueda
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

run(host='0.0.0.0', port=8080)
