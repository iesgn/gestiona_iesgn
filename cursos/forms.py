# -*- coding: utf-8 -*-
from usuarios.libldap import gnLDAP
from django import forms


def getSelect(grupo):
	ldap=gnLDAP()
	filtro={"grupo":grupo}
	lista=ldap.gnBuscar(filtro=filtro)
	lista2=[]
	for usuario in lista:
		lista2.append((usuario["uid"][0],usuario["givenname"][0]+" "+usuario["sn"][0]))

	return lista2


class BuscarUsuario(forms.Form):
	grupo=forms.CharField(widget=forms.HiddenInput())
	def __init__(self, *args, **kwargs):
		super(BuscarUsuario, self).__init__(*args, **kwargs)
		if args[0].has_key("grupo"):
			self.fields['usuarios']=forms.MultipleChoiceField(choices=getSelect("antiguosalumnos"),required=False,widget=forms.MultipleChoiceField(attrs={'class': "form-control js-example-basic-multiple"}))

        


