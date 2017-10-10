from django.shortcuts import render
from usuarios.views import getLista
import operator
# Create your views here.

def cursos(request,curso):
	lista=getLista("*","*",[int(curso)])
	lista.sort(key=operator.itemgetter('sn'))
	print lista