# -*- coding: utf-8 -*-
from bottle import template,request
import sesion

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
	
	info["login"]=sesion.get("user") if sesion.islogin() else ""
	

	return template(name,info=info)

def lista_uid(resultados):
	uid=[]
	for r in resultados:
		uid.append(r.get_attr_values('uidNumber')[0])
	
	return max(map(int,uid))+1
	
def lista_usuarios_tipo(lista,tipo):
	resultado=[]
	for usu in lista:
		if usu.get_attr_values("description")[0]==tipo:
			resultado.append(usu.get_attr_values("sn")[0]+" "+usu.get_attr_values("givenname")[0]+","+usu.get_attr_values("uid")[0])
	return sorted(resultado)