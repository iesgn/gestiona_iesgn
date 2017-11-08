from django.shortcuts import render,redirect
from .forms import UploadFileForm
from django.conf import settings
import os
import os.path
# Create your views here.

def add(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["csr"],request.session["username"])
            return redirect(settings.SITE_URL+'/certificados')
    else:
    	path= os.path.join(settings.BASE_DIR, 'cert/%s'%request.session["username"])
    	if  os.path.isdir(path):
    		files=os.listdir(path)
    		paths=[]
    		for file in files:
    			paths.append(path+"/"+file)
    		return render(request, 'files.html', {'files': zip(paths,files)})
    	else:
        	form = UploadFileForm()
    		return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f,nombre):
	path= os.path.join(settings.BASE_DIR, 'cert/%s'%nombre)
	if not os.path.isdir(path):
		os.makedirs(path)
	path_file=path+"/"+f.name
	with open(path_file, 'w') as destination:
		destination.write(f.read())
    