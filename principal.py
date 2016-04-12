from bottle import route, template, run, static_file, error,request,response,redirect,error
import sesion
@route('/')
def index():
    info={"login":sesion.get()}
    return template("index.tpl",info=info)

@route('/login',method="post")
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if username=="pepe" and  password=="asdasd":
        sesion.set(username)
        redirect('/')
    else:
        info={"login":sesion.get(),"error":True}
        return template('index.tpl',info=info)

@route('/logout')
def do_logout():
    sesion.delete()
    redirect('/')

@route('/restricted')
def restricted_area():
    username = sesion.get()
    if username:
        return template("Hello {{name}}. Welcome back.", name=username)
    else:
        return "You are not logged in. Access denied."

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@error(404)
def error404(error):
    return "Nada"

run(host='0.0.0.0', port=8080)
