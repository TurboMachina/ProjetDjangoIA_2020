from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("chooseColor/<str:game_id>/", views.choose_color),
    path("joinGame/<str:game_id>/", views.join_game),
    path("createGame/", views.create_game),
    path("listJoinableGames/", views.joinable_games),
    path("myGames/", views.my_games),
    path("resumeGame/<str:game_id>/", views.resume_game),
    path("move/<str:game_id>/", views.apply_move),
    path("startGame/<str:game_id>/", views.start_game),
    path("listIaTrainable/", views.list_ia_trainable)
]