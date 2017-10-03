# -*- coding: utf-8 -*-
from django import forms
clases = (
    ('0','Todos'),
    ('1', '1º ASIR'),
    ('2', '2º ASIR'),
    ('3', '1º SMR'),
    ('4', '2º SMR'),
    ('5', 'Profesor'),
    ('6', 'Antiguo Alumno'),
    ('7', 'Antiguo Porfesor'),
    ('8', 'Otros'),
)



class BuscarUsuario(forms.Form):
    nombre=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': "form-control"}))
    apellidos=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': "form-control"}))
    clase=forms.ChoiceField(choices=clases,required=False,widget=forms.Select(attrs={'class': "form-control"}))

class newUserForm(forms.Form):
    username=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
    contrasena=forms.CharField(max_length=100,required=True,widget=forms.PasswordInput(attrs={'class': "form-control"}))
    nombre=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
    apellidos=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
    email=forms.CharField(max_length=100,required=True,widget=forms.EmailField(attrs={'class': "form-control"}))
    ciudad=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
