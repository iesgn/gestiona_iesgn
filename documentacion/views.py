from django.shortcuts import render

# Create your views here.

def vpn(request):
	return render(request,"vpn.html")