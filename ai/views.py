#-----------------------------------------------------------------------------------------------
# Views of the AI
#-----------------------------------------------------------------------------------------------

from django.shortcuts import render, redirect
from django import forms
from ai import business
from ai.error import Error
from django.contrib.auth.decorators import login_required


class IAForm(forms.Form) :
    epsilonGreedy = forms.FloatField(label="epsilon greedy")
    learningRate = forms.FloatField(label="learning rate")
    gamma = forms.FloatField(label="gamma")

@login_required(login_url="/connection/")
def create_ia(request) :
    if request.method == "GET" :
        return render(request, "ai/createIA.html", {"form" : IAForm()})
    
    if request.method == "POST" :
        try :
            ia = business.create_ia(IAForm(request.POST))
        except Error as error :
            return render(request, "ai/errorPage.html", {"error_message" : error.message, "form" : IAForm()})
        return render(request, "ai/IACreated.html", {"ia" : ia})


@login_required(login_url="/connection/")
def list_ia(request) :
    IAList = business.list_ia()
    return render(request, "ai/listIA.html", {"listIA": IAList})

