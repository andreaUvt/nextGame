# Generated by Django 5.1.3 on 2025-01-09 09:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nextGameApp", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="favorite_games",
            field=models.ManyToManyField(
                blank=True, related_name="favorited_by", to="nextGameApp.game"
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="played_games",
            field=models.ManyToManyField(
                blank=True, related_name="played_by", to="nextGameApp.game"
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="to_play_games",
            field=models.ManyToManyField(
                blank=True, related_name="to_play_by", to="nextGameApp.game"
            ),
        ),
    ]
