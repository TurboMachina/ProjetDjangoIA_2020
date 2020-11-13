from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('move', views.apply_move),
    path("joinGame/<str:game_id>/", views.join_game),
    path("createGame/", views.create_game),
    path("listJoinableGame/", views.joinable_games)
]