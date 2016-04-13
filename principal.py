from bottle import route, template, run, static_file, error,request,response,redirect,error
import sesion
from gestiona import my_template
from libldap import LibLDAP

@route('/')
def index():
    return my_template("index.tpl")

@route('/login',method="post")
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    lldap=LibLDAP(username,password)
    print lldap.isbind
    print lldap.con
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

        return my_template('usuarios.tpl')
    else:
        redirect('/')

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@error(404)
def error404(error):
    return "Nada"

run(host='0.0.0.0', port=80)
