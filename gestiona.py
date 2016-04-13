# -*- coding: utf-8 -*-
from bottle import template
from sesion import get

def tipos(tipo):

	vtipos={"0":"Todos","1":"1ºASIR","2":"2ºASIR","3":"1ºSMR","4":"2ºSMR","5":"Profesor","6":"Antiguo Alumno","7":"Antiguo Profesor","8":"Otro"}
	if tipo not in vtipos.keys():
		tipo="8"
	return vtipos[tipo]



def getFiltro(filtro):
	print filtro.dict
	respuesta={}
	for key,value in filtro.dict.items():
		
		if value[0]!=None:
			respuesta[key]=value[0]
		else:
			repuesta[key]=""
	return respuesta

def my_template(name,info={}):
	info["login"]=get()
	return template(name,info=info)