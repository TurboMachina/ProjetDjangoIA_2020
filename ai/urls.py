from django.urls import path

from . import views

urlpatterns = [
    path("createAI/", views.create_ia)
]