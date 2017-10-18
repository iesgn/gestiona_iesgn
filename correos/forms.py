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
    contenido=forms.CharField(max_length=100,required=False,widget=forms.Textarea(attrs={'class': "form-control",'cols': 100, 'rows': 15}))

class BuscarDestinatariosForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
            dest = kwargs.pop('dest')
            alum = kwargs.pop('alum')
            print dest
            super(BuscarDestinatariosForm, self).__init__(*args, **kwargs)
            lista=["Ninguno","Todos","1º ASIR","Bilingüe","Consejo Escolar"]
            ldap=gnLDAP()
            lista=[]
            for keys,values in ldap.grupo.items():
                if not "prof" in keys:
                    lista.append((keys,values))
            self.fields["alumnos"] = forms.ChoiceField(initial= alum,choices=sorted(lista),required=False,widget=forms.Select(attrs={'class': "form-control",'onchange': 'this.form.submit();'}))
            self.fields["destinatarios"]=forms.MultipleChoiceField(initial=dest,choices=getSelect(),required=False,widget=forms.SelectMultiple(attrs={'class': "form-control js-example-basic-multiple"}))

            
