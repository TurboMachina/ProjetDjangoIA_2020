from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class ConnectionForm(forms.Form) :
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password")

class registerForm(ConnectionForm):
    email = forms.CharField(label="Email", widget=forms.EmailInput())


def index(request):
    if request.method == "GET": # get connection page
        form = ConnectionForm() # empty form
        return render(request, "connection/index.html", { "form": form })

    if request.method == "POST": # post a connection
        form = ConnectionForm(request.POST) #auto fill form with info in POST
        
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user :
                login(request, user)
                return HttpResponse("OK")
            else : return HttpResponse("not ok")
        return HttpResponse("KO")

def register(request):
    if request.method == "GET":
        form = registerForm()
        return render(request, "connection/register.html", {"form": form})

    if request.method == "POST":
        form = registerForm(request.POST)

        if form.is_valid():
            try :
                User.objects.create_user(form.cleaned_data["username"], form.cleaned_data["email"], form.cleaned_data["password"])
            except :
                return HttpResponse("username or email already taken")
            return HttpResponse("ok")
        return HttpResponse("KO")


def logout_view(request):
    logout(request)
    return HttpResponse("OK")