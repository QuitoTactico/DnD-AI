from DnD_AI.models import *
from DnD_AI.default import *
from django.core.management.base import BaseCommand

def put_models_on_campaign():
    campaign = Campaign.objects.filter(is_completed=False).first()
    for model in [Character, Monster, Treasure, History, Tile]:
        for instance in model.objects.filter(campaign=None):
            instance.campaign = campaign
            instance.save()

class Command(BaseCommand):
    help = "Puts every model that hasn't been put on a campaign, on the test campaign, or any other campaign that is not completed"

    def handle(self, *args, **kwargs):
        put_models_on_campaign()
        self.stdout.write(self.style.SUCCESS('Successfully put every model on a campaign'))