from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required # permet de limiter les views aux utilisateurs connectés
from django.db.models import Count
import json
from game.models import *
from django.contrib.auth.models import User
from game import business
from game.error import *

from django import forms
import random


class Color_player_form(forms.Form) :
    hex_color = forms.CharField(label='your color', max_length=7, widget=forms.TextInput(attrs={'type': 'color'}))

@login_required(login_url="/connection/")
def create_game(request) :
    if request.method == "GET" :
        color_form = Color_player_form()
        return render(request, "game/createGame.html", { "form" : color_form })
    
    if request.method == "POST" :
        form = Color_player_form(request.POST)
        try :
            game = business.create_game(form, request.user.id)
        except ForbidenColorError as error :
            return render(request, "game/createGame.html", {"form": Color_player_form(), "error_message" : error.message})
        except ColorInvalidError as error :
            return render(request, "game/errorPage.html", {"error_message" : error.message})
        return render(request, "game/gameCreated.html", {"game" : game})

@login_required(login_url="/connection/")
def joinable_games(request) :
    if request.method == "GET" :
        games = business.joinable_games(request.user)
        return render(request, "game/listJoinableGames.html", {"games" : games})

@login_required(login_url="/connection/")
def my_games(request) :
    if request.method == "GET" :
        games = business.my_games(request.user)
        return render(request, "game/listGames.html", {"games" : games})

@login_required(login_url="/connection/")
def resume_game(request, game_id) :
    try :
        game = business.resume_game(game_id, request.user.id)
    except NotPlayerError as error :
        return render(request, "game/errorPage.html", {"error_message" : error.message}, status=400)
    print(game.winner)
    return render(request, "game/game.html", {"game" : game, "game_id" : game_id})

@login_required(login_url="/connection/")
def start_game(request, game_id) :
    try :
        game = business.start_game(game_id, request.user)
    except StartGameError as error :
        return render(request, "game/errorPage.html", {"error_message" : error.message}, status=400)
    return redirect("/game/resumeGame/" + game_id)

@login_required(login_url="/connection/")
def choose_color(request, game_id) :
    return render(request, "game/chooseColor.html", {"form" : Color_player_form(), "game_id" : game_id})

@login_required(login_url="/connection/")
def join_game(request, game_id) :
    try :
        business.join_game(game_id, request.user, Color_player_form(request.POST))
    except ColorError as error :
        return render(request, "game/chooseColor.html", {"error_message" : error.message, "form" : Color_player_form(), "game_id" : game_id}, status=400)
    except Error as error :
        return render(request, "game/errorPage.html", {"error_message" : error.message})
    return redirect("/game/resumeGame/" + game_id + "/")


def index(request):
    if request.method == "GET":
        return render(request, "game/index.html")



def ComplexHandler(Obj):
    if hasattr(Obj, 'to_json'):
        return Obj.to_json()

@login_required(login_url="/connection/")
def apply_move(request, game_id) :
    try :
        game = business.apply_move(game_id, request.user, json.loads(request.body)["move"])
    except Error as error :
        return JsonResponse(data={"error_message" : error.message}, status=400)
    return JsonResponse(json.dumps(game, default=ComplexHandler), safe=False)


class Vs_ia_form(Color_player_form) :
    ia_color = forms.CharField(label='AI color', max_length=7, widget=forms.TextInput(attrs={'type': 'color'}))
  

def create_game_vs_ia_form(request, ia_id) :
    return render(request, "game/gameVsIaForm.html", {"ia_id" : ia_id, "form" : Vs_ia_form()})


def create_game_vs_ia(request, ia_id) :
    try :
        form = Vs_ia_form(request.POST)
        game = business.create_game(form, request.user.id)
        business.join_ia(game.id, ia_id, form)
    except Error as error :
        return render(request, "game/errorPage.html", {"error_message" : error.message})
    return redirect("/game/resumeGame/" + str(game.id) + "/")
