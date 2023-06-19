import re
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import ECG_form
from django.utils import timezone
from datetime import datetime, timedelta
from .models import ECG_models
# Create your views here.

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

    if request.method == 'POST' and 'clean_database' in request.POST:
        # Delete all objects in the model
        ECG_models.objects.all().delete()
        return render(request, 'grafico.html', {'message': 'Database cleaned successfully.'})

    ahora= datetime.now()
    data = []
    labels =[]
    titulo= "Ultimos 60 minutos"
    #min = []
    #max = []
    #avg = []
    ultima_hora = ahora-timedelta(hours=1)
    queryset = ECG_models.objects.all()
    #queryset = T_Vs_t.objects.all()[:1440] #1440 pts son las ultimas 24 hrs, considerando que la info se registra cada un min

    for maumau in queryset:
        data.append(maumau.amp)
        labels.append(str(maumau.data.strftime("%Y-%m-%d %H:%M")))
    return render(request, 'grafico.html', {'labels': labels,'data': data})


################################

################################FUNCIONA

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