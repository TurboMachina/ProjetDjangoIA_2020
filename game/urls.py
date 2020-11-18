from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("chooseColor/<str:game_id>/", views.choose_color),
    path("joinGame/<str:game_id>/", views.join_game),
    path("createGame/", views.create_game),
    path("listJoinableGame/", views.joinable_games),
    path("myGames/", views.my_games),
    path("resumeGame/<str:game_id>/", views.resume_game),
    path("move/<str:game_id>/", views.apply_move)
]