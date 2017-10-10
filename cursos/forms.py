# -*- coding: utf-8 -*-

class BuscarUsuario(forms.Form):
    alumno=forms.ChoiceField(choices=(),required=False,widget=forms.MultipleChoiceField(attrs={'class': "form-control"}))
    
    def __init__(self, *args, **kwargs):
        super(BuscarUsuario, self).__init__(*args, **kwargs)
        if args[0].has_key("AP") and args[0]["AP"]=="profesores":
            self.fields['clase']=forms.ChoiceField(choices=clasesProfesores,required=False,widget=forms.Select(attrs={'class': "form-control",'onchange': 'this.form.submit();'}))

        else:
            self.fields['clase']=forms.ChoiceField(choices=clasesAlumnos,required=False,widget=forms.Select(attrs={'class': "form-control",'onchange': 'this.form.submit();'}))
