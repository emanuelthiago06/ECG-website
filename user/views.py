from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.http import HttpRequest, HttpResponse



def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request,"user/login.html")

def handle_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')
    return redirect('login')

def logout_user(request):
    logout(request)
    return redirect('login')
        

def sign_in(request):
    return render(request,"user/sign_in.html")        

        
@csrf_exempt         
def handle_sign_in(request):
    if request.method == 'POST':
        try:
            user_login = request.POST.get('username')
            user_password = request.POST.get('password')

            if User.objects.filter(username=user_login).exists():
                messages.error(request, "Usuário já existe")
                return redirect('sign_in')

            user = User.objects.create_user(
                username=user_login,
                password=user_password
            )
            user.save()

            messages.success(request, "Usuário criado com sucesso")
            return redirect('sign_in')

        except Exception as e:
            messages.error(request, e)
            return redirect('sign_in')

    return HttpResponse(status=400)
