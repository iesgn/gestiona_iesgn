from usuarios.libldap import gnLDAP
from django import forms


def getSelect(grupo):
	ldap=gnLDAP()
	filtro={"grupo":grupo}
	lista=ldap.gnBuscar(filtro=filtro)
	lista2=[]
	for usuario in lista:
		lista2.append((usuario["uid"][0],usuario["givenName"][0]+" "+usuario["sn"][0]))
	return lista2


class BuscarUsuario(forms.Form):
	grupo=forms.CharField(widget=forms.HiddenInput())
	def __init__(self, *args, **kwargs):
		super(BuscarUsuario, self).__init__(*args, **kwargs)
		lista=getSelect('all')
		lista2=getSelect(args[0]["grupo"])
		lista3 = [x for x in lista if x not in lista2]
		self.fields['usuarios']=forms.MultipleChoiceField(choices=lista3,required=False,widget=forms.SelectMultiple(attrs={'class': "form-control js-example-basic-multiple"}))

		
        


