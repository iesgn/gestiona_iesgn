from django import forms

class UploadFileFormEquipo(forms.Form):
    csr_equipo = forms.FileField(label="Peición de certificado de equipo. Sube el fichero csr:")
class UploadFileFormUsuario(forms.Form):
    csr_usuario = forms.FileField(label="Peición de certificado de usuario. Sube el fichero csr:")