from django.shortcuts import render,HttpResponseRedirect
from .forms import UploadFileForm
from django.conf import settings
import os
import os.path
# Create your views here.

def add(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['csr'])
            return redirect(settings.SITE_URL+'/certificados')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
	path=file_path = os.path.join(settings.BASE_DIR, 'cert')
	print path
	if not os.path.isdir(path):
		os.mkdir(path)
    #with open('some/file/name.txt', 'wb+') as destination:
    #    for chunk in f.chunks():
    #        destination.write(chunk)