# -*- coding: utf-8 -*-
from usuarios.libldap import gnLDAP
from django import forms


def getSelect(grupo):
	ldap=gnLDAP()
	filtro={"grupo":grupo}
	lista=ldap.gnBuscar(filtro=filtro)
	return lista


class BuscarUsuario(forms.Form):
	usuarios=forms.MultipleChoiceField(choices=(),required=False)
	grupo=forms.CharField(widget=forms.HiddenInput())
	def __init__(self, *args, **kwargs):
		super(BuscarUsuario, self).__init__(*args, **kwargs)
		if args[0].has_key("grupo"):
			self.fields['grupo']=forms.ChoiceField(choices=getSelect(args[0]["grupo"]),required=False,widget=forms.Select(attrs={'class': "form-control",'onchange': 'this.form.submit();'}))

        


