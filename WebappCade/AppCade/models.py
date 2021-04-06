from django.db import models
from .validators import validate_file_extension
# Create your models here.
class Document(models.Model):
    docfile = models.FileField(upload_to='documents', validators=[validate_file_extension])
    name = models.CharField(max_length=40, default=docfile.name)
    description = models.TextField(max_length=400, default="") #dimensione temporanea

    def __str__(self):
        return self.name

#Classi da Implementare
class CadeModelManager(models.Model):
    #id=models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    #path cartella modello
    path = models.CharField(max_length=200, default="")
    def __str__(self):
        return self.name

class CadeModel(models.Model):
    #file.model a cui fa riferimento (compass = compass.model)
    modfile = models.FileField(upload_to="models")
    #nome del CadeModelexit()
    name = models.CharField(max_length=200)
    #File di testo usato per creare modfile
    txt_file = models.ForeignKey(Document, on_delete=models.CASCADE)
    #Permette di capire quali slicemodel sono allineati
    cademodelmanager = models.ForeignKey(CadeModelManager, on_delete=models.CASCADE)
    def __str__(self):
        return self.name