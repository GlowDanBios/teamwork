from django.shortcuts import render, HttpResponse, get_object_or_404
import PIL.Image
from io import BytesIO
import os
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Project
from django.contrib.auth import authenticate, login, logout


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        projects = Project.objects.filter(users__pk=request.user.id)
        print(projects)
        return render(request, 'index.html', {'projects': projects})
    else:
        return redirect('/auth')


def project(request):
    pid = request.GET.get('id', None)
    if pid:
        proj = get_object_or_404(Project, pk=pid)
        if len(Project.objects.filter(id=pid, users__pk=request.user.id)) > 0:
            return render(request, 'project.html', {'proj': proj})
    return redirect('')


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
        id = request.headers['Data'].split(':')[1].replace('}', '')
        if 'proj'+id not in os.listdir('mainapp/static'):
            os.mkdir('mainapp/static/proj'+id)
        if img:
            mg = PIL.Image.open(BytesIO(img))
            i = (len(os.listdir('mainapp/static/proj'+id)))
            if i > 30:
                for j in os.listdir('mainapp/static/proj'+id):
                    os.remove('mainapp/static/proj'+id + '/' + j)
            k = len(os.listdir('mainapp/static/proj'+id))
            if k < 10:
                mg.save(f'mainapp/static/proj{id}/canvas0{k}.png', 'PNG')
            else:
                mg.save(f'mainapp/static/proj{id}/canvas{k}.png', 'PNG')
            return HttpResponse(status=200)
    return HttpResponse(status=400)


def get_updates(request):
    id = request.GET.get('id', None)
    if id:
        file = os.listdir('mainapp/static/proj'+id)[-1]
        return HttpResponse(content=json.dumps({'i': 'static/proj'+id + '/' + file}))
    return HttpResponse(status=400)
