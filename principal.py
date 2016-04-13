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
        filtro = getFiltro(request.GET)
        lldap=LibLDAP()
        resultados=lldap.buscar('(givenname=%s*)'%filtro.get("givenname"))
        info={"resultados":resultados}
        info["params"]=filtro
        return my_template('usuarios.tpl',info=info)
    else:
        redirect('/')

@route('/prueba')
def prueba():
    class RegistrationForm(Form):
        username     = StringField('Username', [validators.Length(min=4, max=25)])
        email        = StringField('Email Address', [validators.Length(min=6, max=35)])
        accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])

    form=RegistrationForm()
    info={"form":form}
    return my_template('prueba.tpl',info=info)


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')


@error(404)
def error404(error):
    return "Nada"

run(host='0.0.0.0', port=80)
