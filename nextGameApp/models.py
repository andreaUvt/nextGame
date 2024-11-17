from django.db import models

# Create your models here.

class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    metacritic = models.IntegerField(null=True, blank=True)
    released = models.DateField(null=True, blank=True)
    tba = models.BooleanField(default=False)
    updated = models.DateTimeField()
    background_image = models.URLField(max_length=500, null=True, blank=True)
    background_image_additional = models.URLField(max_length=500, null=True, blank=True)
    website = models.URLField(max_length=500, null=True, blank=True)
    rating = models.FloatField()
    rating_top = models.IntegerField()
    ratings = models.JSONField(default=dict, blank=True)
    reactions = models.JSONField(default=dict, blank=True)
    added = models.IntegerField()
    added_by_status = models.JSONField(default=dict, blank=True)
    playtime = models.IntegerField()
    screenshots_count = models.IntegerField()
    movies_count = models.IntegerField()
    creators_count = models.IntegerField()
    achievements_count = models.IntegerField()
    parent_achievements_count = models.IntegerField()
    reddit_url = models.URLField(max_length=500, null=True, blank=True)
    reddit_name = models.CharField(max_length=255, null=True, blank=True)
    reddit_description = models.TextField(null=True, blank=True)
    reddit_logo = models.URLField(max_length=500, null=True, blank=True)
    reviews_text_count = models.IntegerField(null=True, blank=True)
    ratings_count = models.IntegerField()
    suggestions_count = models.IntegerField()
    alternative_names = models.JSONField(default=list, blank=True)
    metacritic_url = models.URLField(max_length=500, null=True, blank=True)
    parents_count = models.IntegerField()
    additions_count = models.IntegerField()
    game_series_count = models.IntegerField()
    reviews_count = models.IntegerField()
    stores = models.JSONField(default=list, blank=True)
    developers = models.JSONField(default=list, blank=True)
    genres = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)
    description_raw = models.TextField()

    def __str__(self):
        return self.name