from django.shortcuts import render
from django.contrib.staticfiles.views import serve
from django.http import Http404
from django.conf import settings
import json,os

def show(request):
    path = os.path.join(settings.STATICFILES_DIRS[0], 'content_iesgn/proyectos/proyectos.json')
    with open(path) as fichero:
        datos=json.load(fichero)
    info={"datos":datos}
    return render(request,"mostrarproy.html",info)
def server(request,url):
    print(url)
    try:
        return serve(request, 'content_iesgn/'+url)
    except:
        raise Http404
    
# Create your views here.
