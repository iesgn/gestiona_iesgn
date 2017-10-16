from django.shortcuts import render
from django.http import Http404
from gestiona_iesgn.views import test_profesor,test_login

# Create your views here.

def doc(request,doc):
	islogin=["ca"]
	isprofesor=[]
	if doc in islogin:
		test_login(request)
	if doc in isprofesor:
		test_profesor(request)
	try:
		return render(request,doc+".html")
	except:
		raise Http404 