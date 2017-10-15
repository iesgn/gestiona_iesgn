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
		if args[0].has_key("grupo") and args[0]["grupo"]=="openstackusers":
			grupos=["asir1","asir2","smr1","smr2","profesores"]
			lista=[]
			for grupo in grupos:
				lista.extend(getSelect(grupo))
			lista2=getSelect("openstackusers")
			lista3 = [x for x in lista if x not in lista2]
			self.fields['usuarios']=forms.MultipleChoiceField(choices=lista3,required=False,widget=forms.SelectMultiple(attrs={'class': "form-control js-example-basic-multiple"}))

		elif args[0].has_key("grupo"):
			self.fields['usuarios']=forms.MultipleChoiceField(choices=getSelect("antiguosalumnos"),required=False,widget=forms.SelectMultiple(attrs={'class': "form-control js-example-basic-multiple"}))

        


