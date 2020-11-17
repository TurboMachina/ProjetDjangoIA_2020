from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required # permet de limiter les views aux utilisateurs connectés
from django.db.models import Count
import json
from game.models import *
from django.contrib.auth.models import User

from django import forms
import random


class NewGameForm(forms.Form):
    player1 = forms.CharField(label="Player 1")
    player2 = forms.CharField(label="Player 2")

class Color_player_form(forms.Form) :
    hex_color = forms.CharField(label='your color', max_length=7, widget=forms.TextInput(attrs={'type': 'color'}))

#TODO déplacer le code dans le fichier business
#TODO faire les pages html
def create_game(request) :
    if request.method == "GET" :
        color_form = Color_player_form()
        return render(request, "game/createGame.html", { "form" : color_form })
    
    if request.method == "POST" :
        form = Color_player_form(request.POST)
        if not form.is_valid() :
            return render(request, "game/errorPage.html", { "errorMessage" : "color is not valid" }) #TODO à changer moche
        
        game = Game.objects.create()
        user = User.objects.get(pk=request.user.id)
        UserGame.objects.create(userId=user, game=game, color=int(form.cleaned_data["hex_color"].replace("#", ""), 16), userNumber=1)
        return render(request, "game/gameCreated.html", {"game" : game})


def joinable_games(request) :
    if request.method == "GET" :
        games = Game.objects.annotate(Count("players"))
        games = games.filter(players__count__lte=2, gameState__isnull=True).exclude(players=request.user)
        return render(request, "game/listJoinableGames.html", {"games" : games})


def my_games(request) :
    if request.method == "GET" :
        games = Game.objects.filter(players=request.user)
        return render(request, "game/listGames.html", {"games" : games})


def resume_game(request, game_id) :
    game = Game.objects.filter(id=game_id, players__id=request.user.id).first()
    if not game :
        return render(request, "game/errorPage.html", {"error_message" : "you are not a player of this game"})
    return render(request, "game/game.html", {"game" : game})


def start_game(request, game_id) :
    game = Game.objects.filter(id=game_id, players__id=request.user.id).first()
    if not game :
        return render(request, "game/errorPage.html", {"error_message" : "you are not allow to start this game"})
    #TODO start game : map to DTO and start


def choose_color(request, game_id) :
    return render(request, "chooseColor.html", {"form" : Color_player_form(), "game_id" : game_id})


def join_game(request, game_id) :
    game = Game.objects.get(id=game_id)
    if request.user in game.players :
        return render(request, "game/errorPage.html", {"error_message" : "you are already in this game"})

    if len(game.players) == 2 :
        return render(request, "game/errorPage.html", {"error_message" : "already two players"})
    
    form = Color_player_form(request.POST)
    if not form.is_valid() :
        return render(request, "errorPage.html", {"errorMessage" : "not a valid color"})
    
    UserGame.objects.create(userId=request.user, game=game, color=form.cleaned_data["hex_color"], userNumber=2)
    return redirect("game/resumeGame/" + game_id + "/")
    return render(request, "game/gameJoined.html", {"game_id", game_id})


def index(request):
    if request.method == "GET":
        form = NewGameForm()
        return render(request, "game/index.html", { "form": form })

    if request.method == "POST": 
        form = NewGameForm(request.POST)

        if form.is_valid():
            game_state = {
                "game_id" : 11,
                "board" : [[1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,2]],
                "players" : [{
                        "id" :  10,
                        "name" : "Alice",
                        "color" : "cyan",
                        "position" : [0,0]
                    },{
                        "id" :  20,
                        "name" : "Bob",
                        "color" : "orange",
                        "position" : [7,7]
                    }],
                "current_player" : 1,
                "code" : 0
            }
            return render(request, 'game/new_game.html', game_state)

        return HttpResponse("KO")

def apply_move(request) :
    random_board = [[random.randint(0,2) for i in range(8)]for i in range(8)]
    game_state = {
        "game_id" : 11,
        "board" : random_board,
        "players" : [{
                "id" :  10,
                "name" : "Alice",
                "color" : "cyan",
                "position" : [0,0]
            },{
                "id" :  20,
                "name" : "Bob",
                "color" : "orange",
                "position" : [7,7]
            }],
        "current_player" : 1,
        "code" : 0
    }
    return JsonResponse(game_state)





    