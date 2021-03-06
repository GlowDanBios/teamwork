from django.shortcuts import render, HttpResponse, get_object_or_404
import PIL.Image
from io import BytesIO
import os
import json
from random import randint

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Project, Message, Task, File
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Project_html:
    def __init__(self, name, users, path, id):
        self.name = name
        self.path = path
        self.users = users
        self.id = id


def index(request):
    if request.user.is_authenticated:
        projects = Project.objects.filter(users__pk=request.user.id)
        projects_html = []
        for project in projects:
            try:
                path = '/static/proj' + str(project.id) + '/' + sorted(os.listdir('mainapp/static/proj' + str(project.id)))[-1]
            except:
                path = '/static/whitelist.jpg'
            projects_html.append(Project_html(project.name, project.users.all(), path, project.id))
        return render(request, 'index.html', {'projects': projects_html})
    else:
        return redirect('/auth')


def project(request):
    pid = request.GET.get('id', None)
    if pid:
        proj = get_object_or_404(Project, pk=pid)
        users = proj.users.all()
        if len(Project.objects.filter(id=pid, users__pk=request.user.id)) > 0:
            return render(request, 'project.html', {'proj': proj, 'user':request.user, 'users': users})
    return redirect('/')


def auth(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect('/')
            else:
                form = AuthenticationForm(request, request.POST)
        return render(request, 'registration/login.html', {'form': form})

    else:
        form = AuthenticationForm()

        return render(request, 'registration/login.html', {
                'form': form
            })


def log_out(request):
    logout(request)
    return redirect('/auth')


def reg(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'registration/reg.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'registration/reg.html', {'form': form})


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
        file = sorted(os.listdir('mainapp/static/proj'+id))[-1]
        return HttpResponse(content=json.dumps({'i': 'static/proj'+id + '/' + file}))
    return HttpResponse(status=400)


def new_project(request):
    return render(request, 'new_project.html')


def delete_project(request):
    pid = request.GET.get('id', None)
    if pid:
        proj = Project.objects.get(id=pid)
        if request.user in proj.users.all():
            proj.delete()
    return redirect('/')


def join_project(request):
    if request.user.is_authenticated:
        join_id = request.GET.get('join_id', None)
        if join_id:
            proj = Project.objects.get(join_id=join_id)
            proj.users.add(request.user)
            return redirect(f'/project?id={proj.id}')
    return redirect('/')


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


def get_update_messages(request):
    pid = request.GET.get('id', None)
    if pid:
        proj = get_object_or_404(Project, pk=pid)
        messages = Message.objects.filter(project=proj)
        data = []
        for message in messages:
            data.append({'text': message.text, 'author': message.user.username, 'time': str(message.sent_at)[:5]})
        return HttpResponse(status=200, content=json.dumps(data))
    return HttpResponse(status=400)


def get_message(request):
    if request.method == 'POST':
        js = json.loads(request.body.decode('UTF-8'))
        text = js['text']
        user = js['user']
        proj = js['project']
        if text and user and proj:
            msg = Message()
            msg.text = text
            msg.user = get_object_or_404(User, pk=user)
            msg.project = get_object_or_404(Project, pk=proj)
            msg.save()
            return HttpResponse(status=200)
    return HttpResponse(status=400)


def new_task(request):
    if request.method == 'POST':
        js = json.loads(request.body.decode('UTF-8'))
        text = js['text']
        user = js['user']
        project = js['project']
        if text and user and project:
            t = Task()
            t.text = text
            t.user = get_object_or_404(User, pk=user)
            t.project = get_object_or_404(Project, pk=project)
            t.save()
            return HttpResponse(status=200)
    return HttpResponse(status=400)


def get_update_tasks(request):
    pid = request.GET.get('id', None)
    if pid:
        proj = get_object_or_404(Project, pk=pid)
        tasks = Task.objects.filter(project=proj)
        data = []
        for task in tasks:
            data.append({'id': task.id, 'text': task.text, 'author': task.user.id, 'checked': task.checked, 'user': task.user.username})
        return HttpResponse(status=200, content=json.dumps(data))
    return HttpResponse(status=400)


def check_task(request):
    if request.method == 'POST':
        js = json.loads(request.body.decode('UTF-8'))
        tid = js['tid']
        uid = js['uid']
        if tid and uid:
            task = get_object_or_404(Task, pk=tid)
            if task.user.id == uid:
                task.checked = not task.checked
                task.save()
                return HttpResponse(status=200)
    return HttpResponse(status=400)


def get_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        js = json.loads(request.headers['data'])
        uid = js['uid']
        pid = js['pid']
        f = File()
        f.file = file
        f.user = get_object_or_404(User, pk=uid)
        f.project = get_object_or_404(Project, pk=pid)
        f.save()
        return HttpResponse(status=200)
    return HttpResponse(status=400)


def get_file_updates(request):
    pid = request.GET.get('id', None)
    if pid:
        proj = get_object_or_404(Project, pk=pid)
        files = File.objects.filter(project=proj)
        data = []
        fls = []
        for file in files:
            fls.append(file.file.read())
            data.append({'id': file.id, 'userid': file.user.id, 'username': file.user.username, 'file': str(file.file), 'id': file.id })
        return HttpResponse(status=200, content=json.dumps(data))
    return HttpResponse(status=400)


def send_file(request):
    fid = request.GET.get('file', None)
    if fid:
        file = get_object_or_404(File, pk=fid)
        response = HttpResponse(file.file.read(), content_type="application/liquid")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(str(file.file))
        return response
