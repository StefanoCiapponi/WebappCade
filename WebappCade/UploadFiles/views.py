from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Document
from .forms import DocumentForm

# Create your views here.

def list(request):
    #handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'], name = request.POST['name'], description = request.POST['description'])
            newdoc.save()
            
            #redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()

    #Load documents for the list page
    documents = Document.objects.all()  

    #render list page with documents and the form
    return render(
        request,
        'UploadFiles/list.html',
        {'documents':documents, 'form':form}
    )

def index(request):
    return render(request, 'UploadFiles/index.html')