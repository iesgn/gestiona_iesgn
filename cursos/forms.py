# -*- coding: utf-8 -*-
from usuarios.libldap import gnLDAP
from django import forms


def getSelect(grupo):
	ldap=gnLDAP()
	filtro={"grupo":grupo}
	lista=ldap.gnBuscar(filtro=filtro)
	return lista


class BuscarUsuario(forms.Form):
	grupo=forms.CharField(widget=forms.HiddenInput())
	def __init__(self, *args, **kwargs):
		super(BuscarUsuario, self).__init__(*args, **kwargs)
		if args[0].has_key("grupo"):
			self.fields['usuarios']=forms.MultipleChoiceField(choices=(),required=False)

        


