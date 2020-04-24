from django.shortcuts import render, HttpResponse
import PIL.Image
from io import BytesIO
import os
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('/auth')


def auth(request):
    return render(request, 'registration/login.html')


def log_in(request):
    username = request.POST["login"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'registration/fail.html', {'error': 'login or password is incorrect'})


def log_out(request):
    logout(request)
    return redirect('/auth')


def reg(request):
    return render(request, 'registration/reg.html')


def new_account(request):
    username = request.POST["login"]
    password = request.POST["password"]
    password_repeat = request.POST["password_repeat"]
    try:
        user = User.objects.get(username=username)
        return render(request, 'registration/fail.html', {'error': 'there is already a user with this username'})
    except:
        if password == password_repeat:
            User.objects.create_user(username=username, password=password)
            user = authenticate(username=username, password=password)
            return redirect('/')
        else:
            return render(request, 'registration/fail.html', {'error': 'the input passwords are different'})


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