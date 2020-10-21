from django.db import models
from django.contrib.auth import models

# AbstractUser est la classe prévue de base en django pour gérer les utilisateurs
class User(models.User) : 
    pass

