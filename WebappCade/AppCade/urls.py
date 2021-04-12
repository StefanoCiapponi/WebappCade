from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('uploaddocument/', views.UploadDocument, name='uploaddocument'),
    path('uploadedfiles/', views.UploadedDocuments, name='uploadedfiles'),
    path('createmodel/', views.CreateModel, name='createmodel'),
    path('deletemodel/', views.DeleteModel, name='deletemodel'),
    path('deletedocument/', views.DeleteDocument, name='deletedocument')
]