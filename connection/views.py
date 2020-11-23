from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class ConnectionForm(forms.Form) :
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class RegisterForm(ConnectionForm):
    email = forms.CharField(label="Email", widget=forms.EmailInput())


def index(request):
    if request.method == "GET": # get connection page
        return render(request, "connection/index.html", { "form": ConnectionForm() })

    if request.method == "POST": # post a connection
        form = ConnectionForm(request.POST) #auto fill form with info in POST
        
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user :
                login(request, user)
                return redirect("/game/")
            else : return render(request, "connection/index.html", {"form" : ConnectionForm(), "error_message" : "wrong username or password"})
        return HttpResponse("KO")

def register(request):
    if request.method == "GET":
        return render(request, "connection/register.html", {"form": RegisterForm()})

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            try :
                User.objects.create_user(form.cleaned_data["username"], form.cleaned_data["email"], form.cleaned_data["password"])
            except :
                return render(request, "connection/register.html", {"form" : RegisterForm(), "error_message" : "username or email already taken"})
            return redirect("/connection/")
        return HttpResponse("KO")


def logout_view(request):
    logout(request)
    return redirect("/connection/")