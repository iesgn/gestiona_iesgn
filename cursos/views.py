# -*- coding: utf-8 -*-
from django.shortcuts import render
#from usuarios.views import getLista
import operator
# Create your views here.

def cursos(request,curso):
	clases=["","1º ASIR","2º ASIR","1º SMR","2º SMR"]
	tipos=[1,2,3,4,6]
	tipos.remove(int(curso))
	lista=getLista("*","*",[int(curso)])
	lista.sort(key=operator.itemgetter('sn'))
	#lista2=getLista("*","*",tipos)
	lista2.sort(key=operator.itemgetter('sn'))
	todos=[]
	#for alum in lista2:
	#	todos.append(alum["uid"][0],alum["cn"][0])
	info={"titulo":clases[int(curso)],"resultados":lista,"todos":todos}
	return render(request,"listar_cursos.html",info)