from django.shortcuts import render, redirect
from django import forms
from ai import business
from ai.error import Error

# Create your views here.

class IAForm(forms.Form) :
    epsilonGreedy = forms.FloatField(1, 0)
    learningRate = forms.FloatField(1, 0)
    gamma = forms.FloatField(1, 0)

def create_ia(request) :
    if request.method == "GET" :
        return render(request, "ai/createIA.html", {"form" : IAForm()})
    
    if request.method == "POST" :
        try :
            ia = business.create_IA(IAForm(request.POST))
        except Error as error :
            return render(request, "ai/errorPage.html", {"error_message" : error.message, "form" : IAForm()})
        return render(request, "ai/IACreated.html", {"ia" : ia})


def list_ia_trainable(request) :
    IAList = business.list_ia_trainable()
    return render(request, "game/listIATrainable.html", {"IAList", IAList})


class IATrainForm(forms.Form) :
    numberOfGames = forms.IntegerField(min_value=0)

def train_form_ia(request, ia_id) :
    return render(request, "game/trainFormIa.html", {"ia_id" : ia_id, "form" : IATrainForm()})


def train_ia(request, ia_id) :
    ia = business.train_ia(ia_id, IATrainForm(request.POST))
    return redirect("/game/")

