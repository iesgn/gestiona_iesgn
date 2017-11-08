from django import forms

class UploadFileForm(forms.Form):
    csr = forms.FileField()