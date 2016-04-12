from bottle import route, template, run, static_file, error,request,response,redirect,error
import sesion

@route('/')
def index():
    return sesion.my_template("index.tpl")

@route('/login',method="post")
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if sesion.comprobar(username,password):
        sesion.set(username)
        redirect('/')
    else:
        info={"error":True}
        return sesion.my_template('index.tpl',info=info)

@route('/logout')
def do_logout():
    sesion.delete()
    redirect('/')

@route('/usuarios')
def usuarios():
    if sesion.islogin():
        info={"login":sesion.get()}
        return template('usuarios.tpl',info=info)
    else:
        redirect('/')

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@error(404)
def error404(error):
    return "Nada"

run(host='0.0.0.0', port=80)
