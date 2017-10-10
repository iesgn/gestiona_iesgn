# -*- coding: utf-8 -*-
from django.shortcuts import render
from usuarios.views import getLista
import operator
# Create your views here.

def cursos(request,curso):
	clases=["1º ASIR","2º ASIR","1º SMR","2º SMR"]
	lista=getLista("*","*",[int(curso)])
	lista.sort(key=operator.itemgetter('sn'))
	info={"titulo":clases[int(curso)],"resultados":lista}
	return render(request,"listar.html",info)