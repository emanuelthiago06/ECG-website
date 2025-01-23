import re
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import ECG_form
from django.utils import timezone
from datetime import datetime, timedelta
from .models import ECG_models, vcg_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import default_storage
import csv
import random
from django.contrib.auth.models import User
from src import make_img_from_signal_v2
from django.db.models import Max
import json
#from src.make_img_from_signal import generate_image_from_vcg
import cv2

# Create your views here.

ALLOW_START = False

def index(request):
    return render(request, "index.html")

def create_view(request):
    context = {}
    form = ECG_form(request.POST or None)
    if form.is_valid():
        form.save()

    context['form'] = form
    return render(request, 'create_view.html', context)

def grafico_hora(request):
    current_user = request.user
    user_id = current_user.id

    if request.method == 'POST' and 'clean_database' in request.POST:
        # Delete all objects in the model
        vcg_model.objects.filter(user_id=user_id).delete()
        return render(request, 'grafico.html', {'message': 'Database cleaned successfully.'})

    ahora= datetime.now()
    data = []
    data2 = []
    data3 = []
    labels =[]
    titulo= "Ultimos 60 minutos"
    ultima_hora = ahora-timedelta(hours=1)
    #queryset = ECG_models.objects.all()
    queryset = vcg_model.objects.filter(user_id=user_id)
    pred = vcg_model.objects.filter(user_id=user_id).aggregate(Max('pred'))['pred__max']
    try:
        if pred > 0.5:
            pred = "Infarto Detectado"
        else:
            pred = "Paciente Saudável"
    except:
        pred = "Paciente Saudável"

    for query in queryset:
        data.append(query.amp_1)
        data2.append(query.amp_2)
        data3.append(query.amp_3)
        labels.append(str(query.data.strftime("%Y-%m-%d %H:%M")))
    return render(request, 'grafico.html', {'labels': labels,'data': data,'data2': data2,'data3': data3,"pred":pred})


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import ECG_models
from .serializers import Temp_serializer
from .serializers import Temp_serializer2


@csrf_exempt
def Temp_serializer_agregar_data(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = ECG_models.objects.all()
        serializer = Temp_serializer2(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Temp_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    

@csrf_exempt
def upload_file_view(request):
    if request.method == "POST":
        identifier = random.randint(1, 10000)
        body = json.loads(request.body)
        # file = request.FILES.get("file")
        # user_name = request.POST.get("user")
        file = body["file"]
        user_name = body["user"]
        user = User.objects.filter(username=user_name)[0]
        v1 = []
        v2 = []
        v3 = []

        if not file:
            return JsonResponse({"error": "Nenhum arquivo enviado"}, status=400)

        # Processa o arquivo linha por linha
        for line in file:
            decoded_line = line.decode("utf-8").strip()
            try:
                decoded_line = decoded_line.split('\t')
                column1 = float(decoded_line[0])
                column2 = float(decoded_line[1][1:])
                column3 = float(decoded_line[2][1:])
                v1.append(column1)
                v2.append(column2)
                v3.append(column3)
                time_now = datetime.now()
                vcg_object = vcg_model(
                    key = identifier,
                    amp_1 = column1,
                    amp_2 = column2,
                    amp_3 = column3,
                    data = time_now,
                    user_id= user.id 
                )
                vcg_object.save()
            except:
                print(f"Erro linha : {decoded_line}")
        img = make_img_from_signal_v2.generate_image_from_vcg(v1,v2,v3)
        cv2.imshow("img",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return JsonResponse({"message": "Arquivo processado com sucesso!"}, status=200)

    return JsonResponse({"error": "Método não permitido"}, status=405)


V1 = []
V2 = []
V3 = []
IDENTIFIER = 12

@csrf_exempt
def upload_from_esp_view(request):
    global V1, V2, V3, IDENTIFIER, ALLOW_START

    if request.method == "POST":
        body = json.loads(request.body)
        lines = body.get("lines", [])
        user_name = body["user"]
        position = body["position"]

        if position == "inicio":
            IDENTIFIER = random.randint(1, 10000)
            ALLOW_START = True
            V1, V2, V3 = [], [], []

        if not ALLOW_START:
            return JsonResponse({"error": "Bit de start não recebido"}, status=400)

        user = User.objects.filter(username=user_name).first()
        if not user:
            return JsonResponse({"error": "Usuário não encontrado"}, status=404)

        for line in lines:
            numbers_line = list(map(float, line.split()))
            V1.append(numbers_line[0])
            V2.append(numbers_line[1])
            V3.append(numbers_line[2])

        if position == "fim":
            for i in range(len(V1)):
                time_now = datetime.now()
                vcg_object = vcg_model(
                    key=IDENTIFIER,
                    amp_1=V1[i],
                    amp_2=V2[i],
                    amp_3=V3[i],
                    data=time_now,
                    user_id=user.id
                )
                vcg_object.save()
            img = make_img_from_signal_v2.generate_image_from_vcg(V1, V2, V3)
            pred = make_img_from_signal_v2.classify_img(img)
            vcg_model.objects.filter(key=IDENTIFIER).update(pred=pred)
            V1, V2, V3 = [], [], []
        return JsonResponse({"message": "Pacote processado com sucesso!"}, status=200)

    return JsonResponse({"error": "Método não permitido"}, status=405)