from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required # permet de limiter les views aux utilisateurs connectés
from django.db.models import Count
import json
from game.models import *
from django.contrib.auth.models import User
from game import business

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
    result = business.start_game(game_id, request.user)
    return render(request, result["template_link"], result["context"])


def choose_color(request, game_id) :
    return render(request, "game/chooseColor.html", {"form" : Color_player_form(), "game_id" : game_id})


def join_game(request, game_id) :
    game = Game.objects.get(id=game_id)
    players = game.players.all()
    if request.user in players :
        return render(request, "game/errorPage.html", {"error_message" : "you are already in this game"})

    if len(players) == 2 :
        return render(request, "game/errorPage.html", {"error_message" : "already two players"})
    
    form = Color_player_form(request.POST)
    if not form.is_valid() :
        return render(request, "errorPage.html", {"errorMessage" : "not a valid color"})
    
    hex_color = int(form.cleaned_data["hex_color"].replace("#", ""), 16)
    if UserGame.objects.filter(game__id=game_id, color=hex_color).exists() :
        return render(request, "errorPage.html", {"error_message" : "this color is already taken"})
    UserGame.objects.create(userId=request.user, game=game, color=hex_color, userNumber=2)
    return redirect("resume_game", game_id)
    return render(request, "game/gameJoined.html", {"game_id", game_id})


def index(request):
    if request.method == "GET":
        return render(request, "game/index.html")

def apply_move(request, game_id) :
    game = business.apply_move(game_id, request.user, json.loads(request.body)["move"])
    return JsonResponse(game)

