# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.widgets import HiddenInput,Textarea,TextInput
class CorreoForm(forms.Form):
    asunto=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': "form-control"}))
    destinatarios=forms.MultipleChoiceField(choices=[],required=False,widget=forms.SelectMultiple(attrs={'class': "form-control js-example-basic-multiple"}))
    contenido=forms.CharField(max_length=100,required=False,widget=forms.Textarea(attrs={'class': "form-control",'cols': 100, 'rows': 15}))


class BuscarDestinatariosForm(forms.Form):
    Alumnos = forms.ChoiceField(choices=[],required=False,widget=forms.Select(attrs={'class': "form-control",'onchange': 'this.form.submit();'}))
    def __init__(self, *args, **kwargs):
            super(BuscarDestinatariosForm, self).__init__(*args, **kwargs)
            lista=["Ninguno","Todos","ETCP","Bilingüe","Consejo Escolar"]
            
            lista2=[]
            for i in xrange(0,len(lista)):
                lista2.append((i,lista[i]))
            
            self.fields['Alumnos'].choices=lista2
