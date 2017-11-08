from django import forms

class UploadFileForm(forms.Form):
    csr = forms.FileField(label="Sube el fichero csr:")