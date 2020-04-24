from django.shortcuts import render, HttpResponse
import PIL.Image
from io import BytesIO
import os
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('/auth')


def auth(request):
    print(request)
    return render(request, 'registration/login.html')


def login(request):
    username = request.POST["login"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        print(f'user {username} has logged in with password {password}')
        return index(request)
    else:
        return render(request, 'registration/fail.html')


def get_img(request):
    if request.method == "POST":
        img = request.body
        if img:
            mg = PIL.Image.open(BytesIO(img))
            i = (len(os.listdir('mainapp/static')))
            if i > 100:
                for j in os.listdir('mainapp/static'):
                    os.remove('mainapp/static/'+j)
            k = len(os.listdir('mainapp/static'))
            if k < 10:
                mg.save(f'mainapp/static/canvas0{k}.png', 'PNG')
            else:
                mg.save(f'mainapp/static/canvas{k}.png', 'PNG')
            return HttpResponse(status=200)
    return HttpResponse(status=400)


def get_updates(request):
    file = os.listdir('mainapp/static')[-1]
    return HttpResponse(content=json.dumps({'i': 'static/'+file}))
