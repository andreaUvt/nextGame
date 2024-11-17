from django.core.management.base import BaseCommand
from nextGameApp.utils import import_games

class Command(BaseCommand):
    help = 'Command for importing currently available genres from tmdb api service.'

    def handle(self, *args, **options):
        import_games()
        self.stdout.write(self.style.SUCCESS('Games imported!'))