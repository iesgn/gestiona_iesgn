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
    asunto=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': "form-control"}))
    destinatarios=forms.MultipleChoiceField(choices=[],required=False,widget=forms.SelectMultiple(attrs={'class': "form-control js-example-basic-multiple"}))
    contenido=forms.CharField(max_length=100,required=False,widget=forms.Textarea(attrs={'class': "form-control",'cols': 100, 'rows': 15}))
    def __init__(self, *args, **kwargs):
        dest = kwargs.pop('dest')
        super(CorreoForm, self).__init__(*args, **kwargs)
        self.fields['destinatarios']=forms.MultipleChoiceField(initial=getSelect(),choices=getSelect(),required=False,widget=forms.SelectMultiple(attrs={'class': "form-control js-example-basic-multiple"}))


class BuscarDestinatariosForm(forms.Form):
    Alumnos = forms.ChoiceField(choices=[],required=False,widget=forms.Select(attrs={'class': "form-control",'onchange': 'this.form.submit();'}))
    def __init__(self, *args, **kwargs):
            super(BuscarDestinatariosForm, self).__init__(*args, **kwargs)
            lista=["Ninguno","Todos","ETCP","Bilingüe","Consejo Escolar"]
            
            lista2=[]
            for i in xrange(0,len(lista)):
                lista2.append((i,lista[i]))
            
            self.fields['Alumnos'].choices=lista2
