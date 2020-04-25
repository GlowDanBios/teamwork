from django.shortcuts import render, HttpResponse, get_object_or_404
import PIL.Image
from io import BytesIO
import os
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Project
from django.contrib.auth import authenticate, login, logout
from random import randint

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    return redirect('/')


def join_project(request):
    join_id = request.GET.get('join_id', None)
    if join_id:
        proj = Project.objects.get(join_id=join_id)
        proj.users.add(request.user)
        return redirect(f'/project?id={proj.id}')


def new_project(request):
    return render(request, 'new_project.html')
def create_project(request):
    name = request.GET.get('name', None)
    if name is not None:
        join_id = randint(1000000000, 9999999999)
        while Project.objects.filter(join_id=join_id):
            join_id = randint(1000000000, 9999999999)
        proj = Project(name=name, join_id=join_id)
        proj.save()
        os.mkdir('mainapp/static/proj' + str(proj.id))
        proj.users.add(request.user)
        return redirect(f'/project?id={proj.id}')


def delete_project(request):
    pid = request.GET.get('id', None)
    print(pid)
    if pid:
        proj = Project.objects.get(id=pid)
        proj.delete()
    return redirect('/')

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
        if 'proj'+id not in os.path.join(BASE_DIR, os.listdir('mainapp/static')):
            os.path.join(BASE_DIR, os.mkdir('mainapp/static/proj'+id))
        if img:
            mg = PIL.Image.open(BytesIO(img))
            i = (len(os.path.join(BASE_DIR, os.listdir('mainapp/static/proj'+id))))
            if i > 30:
                for j in os.path.join(BASE_DIR, os.listdir('mainapp/static/proj'+id)):
                    os.path.join(BASE_DIR, os.remove('mainapp/static/proj'+id + '/' + j))
            k = len(os.path.join(BASE_DIR, os.listdir('mainapp/static/proj'+id)))
            if k < 10:
                mg.save(os.path.join(BASE_DIR, f'mainapp/static/proj{id}/canvas0{k}.png'), 'PNG')
            else:
                mg.save(os.path.join(BASE_DIR, f'mainapp/static/proj{id}/canvas{k}.png'), 'PNG')
            return HttpResponse(status=200)
    return HttpResponse(status=400)


def get_updates(request):
    id = request.GET.get('id', None)
    if id:
        file = '/' + os.listdir(os.path.join(BASE_DIR, 'mainapp/static/proj'+id))[-1]
        return HttpResponse(content=json.dumps({'i': os.path.join(BASE_DIR, 'mainapp/static/proj'+id)[1:] + file}))
    return HttpResponse(status=400)