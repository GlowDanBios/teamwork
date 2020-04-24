from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.


def index(request):
    return render(request, 'index.html')


def auth(request):
    print(request)
    return render(request, 'registration/login.html')


#folowwing code is only for cheking the work of authentification
def login(request):
    username = request.POST["login"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        print(f'user {username} has logged in with password {password}')
        return index(request)
    else:
        return render(request, 'registration/fail.html')
