from bottle import route, template, run, static_file, error
@route('/')
def index():
    return template("index.tpl")

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(host='0.0.0.0', port=8080)
