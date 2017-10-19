# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.widgets import HiddenInput,Textarea,TextInput
from usuarios.libldap import gnLDAP

def getSelect():
	ldap=gnLDAP()
	
	lista=ldap.gnBuscar(cadena="(uid=*)")
	lista2=[]
	for usuario in lista:
		lista2.append((usuario["uid"][0],usuario["givenname"][0]+" "+usuario["sn"][0]))
	return lista2

class CorreoForm(forms.Form):
	asunto=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': "form-control"}))
	contenido=forms.CharField(max_length=100,widget=forms.Textarea(attrs={'class': "form-control",'cols': 100, 'rows': 15}))
	def clean(self):
		super(CorreoForm, self).clean()
		asunto = self.cleaned_data.get("asunto")
		if not asunto:
			del self._errors['asunto']
		contenido = self.cleaned_data.get("contenido")
		if not contenido:
			del self._errors['contenido']

		return self.cleaned_data

class BuscarDestinatariosForm(forms.Form):
	
	def __init__(self, *args, **kwargs):
			dest = kwargs.pop('dest')
			alum = kwargs.pop('alum')
			
			super(BuscarDestinatariosForm, self).__init__(*args, **kwargs)
			lista=[("0","Ninguno"),
				("1","Alumnos")
				("asir1","1º ASIR"),
				("asir2","2º ASIR"),
				("smr1","1º SMR"),
				("smr2","2º SMR"),
				("antiguosalumnos","Antiguos Alumnos"),
				("profesores","Profesores"),
				("antiguosprofesores","Antiguos Profesores"),
				]
			ldap=gnLDAP()
			
			self.fields["alumnos"] = forms.ChoiceField(initial=alum,choices=lista,required=False,widget=forms.Select(attrs={'class': "form-control",'onchange': 'this.form.submit();'}))
			self.fields["destinatarios"]=forms.MultipleChoiceField(initial=dest,choices=getSelect(),required=False,widget=forms.SelectMultiple(attrs={'class': "form-control js-example-basic-multiple"}))

			
