# -*- coding: utf-8 -*-
from django import forms
grupos = (
    ('all','Todos'),
    ('alumnos','Todos Alumnos'),
    ('soloalumnos','Alumnos matriculados')
    ('asir1', '1º ASIR'),
    ('asir2', '2º ASIR'),
    ('smr1', '1º SMR'),
    ('smr2', '2º SMR'),
    ('antiguosalumnos', 'Antiguo Alumno'),
    ('allprofesores','Todos los profesores'),
    ('profesores','Profesores'),
    ('antiguosprofesores', 'Antiguos Profesores'),
    ('openstackusers','Usuarios OpenStack'),

)



class BuscarUsuario(forms.Form):
    nombre=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': "form-control"}))
    apellidos=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': "form-control"}))
    grupo=forms.ChoiceField(choices=grupos,required=False,widget=forms.Select(attrs={'class': "form-control",'onchange': 'this.form.submit();'}))
    
#class newUserForm(forms.Form):
#    uid=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
#    userpassword=forms.CharField(max_length=100,required=True,widget=forms.PasswordInput(attrs={'class': "form-control"}))
#    givenname=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
#    sn=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
#    mail=forms.CharField(max_length=100,required=True,widget=forms.EmailInput(attrs={'class': "form-control"}))
#    l=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
#    AP=forms.CharField(widget=forms.HiddenInput())
#    def __init__(self, *args, **kwargs):
#        super(newUserForm, self).__init__(*args, **kwargs)
#        if args[0].has_key("AP") and args[0]["AP"]=="profesores":
#            self.fields['grupo']=forms.ChoiceField(choices=gruposProfesores[1:],required=False,widget=forms.Select(attrs={'class': "form-control"}))#

#        else:
#            self.fields['grupo']=forms.ChoiceField(choices=gruposAlumnos[1:],required=False,widget=forms.Select(attrs={'class': "form-control"}))#
#

#class updateUserForm(forms.Form):
#    uid=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': "form-control",'readonly':'readonly'}))
#    userpassword=forms.CharField(max_length=100,required=False,widget=forms.PasswordInput(attrs={'class': "form-control"}))
#    givenname=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
#    sn=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
#    mail=forms.CharField(max_length=100,required=True,widget=forms.EmailInput(attrs={'class': "form-control"}))
#    l=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
#    AP=forms.CharField(widget=forms.HiddenInput())
#    def __init__(self, *args, **kwargs):
#        super(updateUserForm, self).__init__(*args, **kwargs)
#        if args[0].has_key("AP") and args[0]["AP"]=="profesores":
#            self.fields['grupo']=forms.ChoiceField(choices=gruposProfesores[1:],required=False,widget=forms.Select(attrs={'class': "form-control"}))
#        else:
#            self.fields['grupo']=forms.ChoiceField(choices=gruposAlumnos[1:],required=False,widget=forms.Select(attrs={'class': "form-control"}))#
#

#class deleteUserForm(forms.Form):
#    uid=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': "form-control"}))#

#class deleteUserForm2(forms.Form):
#    uiddel=forms.CharField(widget=forms.HiddenInput())
