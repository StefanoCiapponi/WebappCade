from django import forms
from django.forms import ModelForm, Form
from .models import Document
from .models import CadeModelManager
from django.db.models import Q

class DocumentForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea,required=False)
    class Meta:
        model = Document
        fields = ['name', 'docfile', 'description']

class SelectDocumentsForm(Form):
    name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'id': 'name', 'onkeyup':'checknames()'}))
    #document_names = [(str(document.id), str(document.name))  for document in Document.objects.all() if "compass" not in document.name]
    documents=forms.ModelMultipleChoiceField(queryset=Document.objects.all().filter(~Q(name__contains="compass")), widget=forms.CheckboxSelectMultiple)
    #documents = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
    #                                        choices=document_names)
                
class DeleteDocumentForm(Form): 
    #MODIFICARE COM MULTIPLECHOICEFIELD
    #document_names = [(str(document.id), str(document.name))  for document in Document.objects.all()]
    #documents = forms.MultipleChoiceField(  widget=forms.CheckboxSelectMultiple,
    #                                        choices=document_names)
    documents=forms.ModelMultipleChoiceField(queryset=Document.objects.all().filter(~Q(name__contains="compass")), widget=forms.CheckboxSelectMultiple)
    
class DeleteModelForm(Form):
    #MODIFICARE COM MULTIPLECHOICEFIELD
    #model_names = [(str(cmm.id), str(cmm.name))  for cmm in CadeModelManager.objects.all()]
    #models = forms.MultipleChoiceField(  widget=forms.CheckboxSelectMultiple,
    #                                choices=model_names)
    models=forms.ModelMultipleChoiceField(queryset=CadeModelManager.objects.all(), widget=forms.CheckboxSelectMultiple)
    