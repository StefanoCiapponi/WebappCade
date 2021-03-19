from django.db import models

# Create your models here.
class Document(models.Model):
    name = models.CharField(max_length=40, default="")
    docfile = models.FileField(upload_to='documents')
    description = models.TextField(max_length=400, default="") #dimensione temporanea

    def __str__(self):
        return self.name