from django.db import models

class User(models.Model) : 
    id = models.IntegerField()
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)

class UserGame(models.Model) : 
    userId = models.ForeignKey(User,on_delete = models.CASCADE)
    game = models.ForeignKey(Game,on_delete = models.CASCADE)
    color = models.IntegerField()
    userNumber = models.IntegerField()
    posUserX = models.IntegerField()
    posUserY = models.IntegerField()


