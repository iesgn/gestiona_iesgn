# -*- coding: utf-8 -*-
from usuarios.libldap import gnLDAP
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

def getSelect(grupo):
	ldap=gnLDAP()
	filtro={"grupo":curso}
	lista=ldap.gnBuscar(filtro=filtro)
	return lista


class BuscarUsuario(forms.Form):
	alumno=forms.ChoiceField(choices=(),required=False,widget=FilteredSelectMultiple(attrs={'class': "form-control"}))
	grupo=forms.CharField(widget=forms.HiddenInput())
	class Media:
		css = {'all':('admin/css/widgets.css','css/overrides.css'),}
		js = ('admin/js/vendor/jquery/jquery.js','/admin/jsi18n/','admin/js/jquery.init.js')
	def __init__(self, *args, **kwargs):
		super(BuscarUsuario, self).__init__(*args, **kwargs)
		if args[0].has_key("grupo"):
			self.fields['grupo']=forms.ChoiceField(choices=getSelect(args[0]["grupo"]),required=False,widget=forms.Select(attrs={'class': "form-control",'onchange': 'this.form.submit();'}))

        


