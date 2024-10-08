from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.template import loader
import django.contrib.auth as dauth

# Create your views here.

def login(request):
    template = loader.get_template("login.html")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = dauth.authenticate(username=username, password=password)
        if user is not None:
            dauth.login(request, user)
            return redirect('/')
        else:
            return HttpResponse(template.render({
                'error_message': 'Não foi possível autenticar'
            }, request))

    return HttpResponse(template.render({}, request))

def register(request):
    template = loader.get_template("register.html")

    if request.method == 'POST':
        display_name = request.POST.get('display_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if display_name == "" or username == "" or password == "":
            return HttpResponse(template.render({
                'error_message': 'Preencha todos os campos!'
            }, request))

        existing_user = User.objects.filter(username=username)
        if existing_user:
            return HttpResponse(template.render({
                'error_message': 'Já existe um usuário com esse username!'
            }, request))


        try:
            User.objects.create_user(username=username, password=password, first_name=display_name)
            print("aa")
            return redirect("/login")
        except Exception as ex:
            print(ex)
            return HttpResponse(template.render({
                'error_message': 'Ocorreu um erro inesperado: ' + str(ex)
            }, request))

    return HttpResponse(template.render({}, request))