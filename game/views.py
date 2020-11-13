from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required # permet de limiter les views aux utilisateurs connectés
from django.db.models import Count
import json
from game.models import *

from django import forms
import random


class NewGameForm(forms.Form):
    player1 = forms.CharField(label="Player 1")
    player2 = forms.CharField(label="Player 2")

#TODO déplacer le code dans le fichier business
#TODO faire les pages html
def create_game(request) :
    if request.method == "GET" :
        return render(request, "game/createGame.html")
    
    if request.method == "POST" :
        game = Game.objects.create()
        UserGame.objects.create(userId=request.user, game=game)
        return render(request, "game/gameCreated.html", game)


def joinable_games(request) :
    if request.method == "GET" :
        games = Game.objects.annotate(Count("players"))
        games = games.filter(players__count__lte=2, board__isNull=True)
        return render(request, "game/listJoinableGames", games)


def my_games(request) :
    if request.method == "GET" :
        games = Game.objects.filter(players=request.user)
        return render(request, "game/listGames.html", games)


def resume_game(request, game_id) :
    game = Game.objects.get(id=game_id)
    if not request.user in game.players :
        return render(request, "game/errorPage.html", {"error_message" : "you are not a player of this game"})
    return render(request, "game/game.html", game)


def start_game(request, game_id) :
    game = Game.objects.get(id=game_id)
    #TODO start game : map to DTO and start


def join_game(request, game_id) :
    game = Game.objects.get(id=game_id)
    if request.user in game.players :
        return render(request, "game/errorPage.html", {"error_message" : "you are already in this game"})
    if len(game.players) == 2 :
        return render(request, "game/errorPage.html", {"error_message" : "already two players"})
    UserGame.objects.create(userId=request.user, game=game)
    return render(request, "game/gameJoined.html")


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





    