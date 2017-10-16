from django.shortcuts import render
from django.http import Http404

# Create your views here.

def doc(request,doc):
	try:
		return render(request,doc+".html")
	except:
		raise Http404 