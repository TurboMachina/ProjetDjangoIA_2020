from django.db import models
from django.contrib.postgres.fields import ArrayField

class User(models.Model) : 
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)


