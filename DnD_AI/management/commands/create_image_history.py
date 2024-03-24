from DnD_AI.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates an image in the History model to be rendered on the console'

    def handle(self, *args, **kwargs):
        History.objects.create(author='SYSTEM', is_image=True, text="media/map/test.png").save()
    
        self.stdout.write(self.style.SUCCESS('Successfully created an image in the History model to be rendered on the console'))

