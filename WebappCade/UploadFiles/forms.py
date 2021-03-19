from django import forms
from django.forms import ModelForm
from .models import Document
#class DocumentForm(forms.Form):
#    docfile = forms.FileField(
#        label='select a file',
#        help_text='max. 42 megabytes'
#    )

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'docfile', 'description']
