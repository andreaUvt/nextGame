# Generated by Django 5.1.3 on 2024-11-17 08:55

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Game",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("metacritic", models.IntegerField(blank=True, null=True)),
                ("released", models.DateField(blank=True, null=True)),
                ("tba", models.BooleanField(default=False)),
                ("updated", models.DateTimeField()),
                (
                    "background_image",
                    models.URLField(blank=True, max_length=500, null=True),
                ),
                (
                    "background_image_additional",
                    models.URLField(blank=True, max_length=500, null=True),
                ),
                ("website", models.URLField(blank=True, max_length=500, null=True)),
                ("rating", models.FloatField()),
                ("rating_top", models.IntegerField()),
                ("ratings", models.JSONField(blank=True, default=dict)),
                ("reactions", models.JSONField(blank=True, default=dict)),
                ("added", models.IntegerField()),
                ("added_by_status", models.JSONField(blank=True, default=dict)),
                ("playtime", models.IntegerField()),
                ("screenshots_count", models.IntegerField()),
                ("movies_count", models.IntegerField()),
                ("creators_count", models.IntegerField()),
                ("achievements_count", models.IntegerField()),
                ("parent_achievements_count", models.IntegerField()),
                ("reddit_url", models.URLField(blank=True, max_length=500, null=True)),
                (
                    "reddit_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("reddit_description", models.TextField(blank=True, null=True)),
                ("reddit_logo", models.URLField(blank=True, max_length=500, null=True)),
                ("reviews_text_count", models.IntegerField(blank=True, null=True)),
                ("ratings_count", models.IntegerField()),
                ("suggestions_count", models.IntegerField()),
                ("alternative_names", models.JSONField(blank=True, default=list)),
                (
                    "metacritic_url",
                    models.URLField(blank=True, max_length=500, null=True),
                ),
                ("parents_count", models.IntegerField()),
                ("additions_count", models.IntegerField()),
                ("game_series_count", models.IntegerField()),
                ("reviews_count", models.IntegerField()),
                ("stores", models.JSONField(blank=True, default=list)),
                ("developers", models.JSONField(blank=True, default=list)),
                ("genres", models.JSONField(blank=True, default=list)),
                ("tags", models.JSONField(blank=True, default=list)),
                ("description_raw", models.TextField()),
            ],
        ),
    ]