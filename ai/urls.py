from django.urls import path

from . import views

urlpatterns = [
    path("createAI/", views.create_ia),
    path("listAI/", views.list_ia)
]