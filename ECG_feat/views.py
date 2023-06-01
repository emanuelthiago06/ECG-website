import re
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import ECG_form
# Create your views here.

def index(request):
    return HttpResponse("First page")

def create_view(request):
    context = {}
    form = ECG_form(request.POS or None)
    if form.is_valid():
        form.save()

    context['form'] = form
    return render(request, 'create_view.html', context)