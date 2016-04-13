from bottle import template
from sesion import get

def my_template(name,info={}):
	info["login"]=get()
	return template(name,info=info)