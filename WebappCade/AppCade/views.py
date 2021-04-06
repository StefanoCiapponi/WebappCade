from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from cade.cade import CADE
from gensim.models.word2vec import Word2Vec
from .models import Document, CadeModelManager, CadeModel
from django.db import models
from .forms import DeleteDocumentForm, DocumentForm, SelectDocumentsForm, DeleteModelForm
import os
from django.conf import settings
from django.core.files import File

# Create your views here.
def CreateModel(request):
    d = CadeModelManager.objects.aggregate(models.Max('id')) #da 8 non so perchè
    key = d['id__max']
    if key==None:
        key = 1
    else:
        key=key+1
    
    if request.method == 'POST':
        form = SelectDocumentsForm(request.POST)
        #form
        if form.is_valid():
            
            documents = form.cleaned_data.get('documents') #ID
            name = form.cleaned_data.get('name')
            if name=="":
                name = key
            

            #crea directory per il nuovo modello e istanzia Aligner usando la directory come path
            path = settings.MEDIA_ROOT+"/models/"+name
            aligner = CADE(opath=path)

            #creo CadeModelManager (pacchetto di vari CadeModel)
            cmm = CadeModelManager()
            cmm.name = name
            cmm.path = path
            cmm.save()

            #creo name_compass.txt
            document_paths= [document.docfile.path for document in documents]
            compass_path = settings.MEDIA_ROOT+"/documents/compass_"+name+".txt"
            compass_instruction="cat "+" ".join(document_paths)+" >"+compass_path
            os.system(compass_instruction)

            #creo modello compass e assegno a un CadeModel associato al CadeModelManager
            aligner.train_compass(compass_path, overwrite=False, save=True)
            compass=Document(   docfile=compass_path, 
                                name="compass_"+name, 
                                description="")
            compass.save()
            compass_model = CadeModel(  modfile = path+"/compass.model",
                                        txt_file=compass,
                                        cademodelmanager=cmm,
                                        name="compass.model")
            compass_model.save()

            #creo modelli dei vari slice e assegno a CadeModel associati al CadeModelManager
            for document_path,document in zip(document_paths, documents):
                #print("DOCUMENT PATH: "+os.path.splitext(os.path.basename(document_path))[0]+".model ID: "+id)
                model_name=os.path.splitext(os.path.basename(document_path))[0]+".model"
                aligner.train_slice(document_path, save=True)
                
                cm=CadeModel(   modfile=path+"/"+model_name,
                                txt_file=document,
                                cademodelmanager=cmm,
                                name=model_name)
                cm.save()
            
    else:
        #form
        form = SelectDocumentsForm()
        #print(form.as_ul)
    return render(
        request,
        'AppCade/CreateModel.html',
        {'form': form, 'key':key}
    )

def DeleteModel(request):
    if request.method == 'POST':
        form = DeleteModelForm(request.POST)
        if form.is_valid():
            cmms = form.cleaned_data.get('models') 
            cademodels=CadeModel.objects.all().filter(cademodelmanager__in=cmms)
            print(cademodels)
            for cm in cademodels:
                print(cm)
                os.system("rm "+cm.modfile.path)
                cm.delete()
            for cmm in cmms:
                os.system("rm -r "+cmm.path)
                cmm.delete()

            print(cademodels)
            #Cancello cogni CadeModelManager, ogni CadeModel che ne fa parte e ogni file .model associato
    else:
        form = DeleteModelForm()
        
    return render(
        request,
        'AppCade/Delete.html',
        {'form':form, 'model':True,
        'document':False}
    )

def UploadedDocuments(request):
    documents = Document.objects.all()
    return render(request, 'AppCade/UploadedDocuments.html', {'documents':documents})

def DeleteDocument(request):
    if request.method == 'POST':
        form = DeleteDocumentForm(request.POST)
        if form.is_valid():
            documents = form.cleaned_data.get('documents') #ID
            print(documents)
            for document in documents:
                os.system("rm "+document.docfile.path)
                document.delete()
            #for cm in cademodels:
            #    print(cm)
            #    os.system("rm "+cm.modfile.path)
            #    cm.delete()
    else:
        form = DeleteDocumentForm()
        
    return render(
        request,
        'AppCade/Delete.html',
        {'form':form, 'model':False,
        'document':True}
    )

def UploadDocument(request):
    #handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'], name = request.POST['name'], description = request.POST['description'])
            newdoc.save()
            
            #redirect to the document list after POST
            return HttpResponseRedirect(reverse('uploaddocument'))
    else:
        form = DocumentForm()

    #Load documents for the list page
    documents = Document.objects.all()  

    #render list page with documents and the form
    return render(
        request,
        'AppCade/list.html',
        {'documents':documents, 'form':form}
    )

def index(request):
    return render(request, 'AppCade/index.html')