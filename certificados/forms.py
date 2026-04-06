# -*- coding: utf-8 -*-
from django import forms

class UploadFileFormEquipo(forms.Form):
    csr_equipo = forms.FileField(label="Petición de certificado de equipo. Sube el fichero csr:",
                                 widget=forms.ClearableFileInput(attrs={"class": "form-control"}))
class UploadFileFormUsuario(forms.Form):
    csr_usuario = forms.FileField(label="Petición de certificado de usuario. Sube el fichero csr:",
                                  widget=forms.ClearableFileInput(attrs={"class": "form-control"}))