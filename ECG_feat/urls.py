from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name= "index"),
    path('create_view/', views.create_view, name = "create_view"),
    path('snippets/',views.Temp_serializer_agregar_data,name ="listed"),
    path('grafico/', views.grafico_hora, name = "grafico_hora"),
    path('upload-file/', views.upload_file_view, name='upload-file'),
    path('upload-esp/', views.upload_from_esp_view, name='upload-esp'),
]