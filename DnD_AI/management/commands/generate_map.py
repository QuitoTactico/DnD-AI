from DnD_AI.models import *
from DnD_AI.map_creator import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Helps to generate a map for an existing campaign'

    def handle(self, *args, **kwargs):

        print('Select your desired campaign from these:\n')
        for campaign_sample in Campaign.objects.all():
            print(campaign_sample)

        campaign_id = int(input('Campaign id: '))
        campaign = Campaign.objects.get(id=campaign_id)

        result = generate_dungeon_map(campaign)
    
        if result:
            self.stdout.write(self.style.SUCCESS(f'Successfully created a {campaign.size_x}x{campaign.size_y} map for the campaign [{campaign_id}]: {campaign.name}'))
        else:
            self.stdout.write(self.style.ERROR(f'An error occurred while generating the map for the campaign [{campaign_id}]: {campaign.name}'))
