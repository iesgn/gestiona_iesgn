from bottle import route, template, run, static_file, error,request,response
import sesion
@route('/')
def index():
    return template("index.tpl")

@route('/login',method="post")
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if username=="pepe" and  password=="asdasd":
        sesion.set(username)
        return template("<p>Welcome {{name}}! You are now logged in.</p>", name=username)
    else:
        return "<p>Login failed.</p>"

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

run(host='0.0.0.0', port=8080)
