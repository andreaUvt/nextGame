from django.db import models
from django.contrib.auth.models import User
import uuid
from nextGameApp.views import Game

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500,blank=True,null=True)
    username = models.CharField(max_length=200, blank=True, null=True, unique=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="profiles/", default="profiles/user-default.png")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    steamid = models.CharField(max_length=100, blank=True, null=True)
    favorite_games = models.ManyToManyField(Game, blank=True, related_name="favorited_by")
    to_play_games = models.ManyToManyField(Game, blank=True, related_name="to_play_by")
    played_games = models.ManyToManyField(Game, blank=True, related_name="played_by")

    def __str__(self):
        return str(self.username)