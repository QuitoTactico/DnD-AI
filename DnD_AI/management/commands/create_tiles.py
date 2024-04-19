from DnD_AI.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create some tiles for Models.Tile using an initial and final point. Rectancle selection'

    def handle(self, *args, **kwargs):

        print('Possible tile types: grass, dirt, path, dungeon, boss, god, psycho, hell')
        tile_type = input('Tile type: ').lower()
        campaign_id = int(input('Campaign id: '))
        x_init, y_init = list(map(int,input('From (x y separed by one space): ').split(' ')))
        x_final, y_final = list(map(int,input('To   (x y separed by one space): ').split(' ')))

        campaign = Campaign.objects.get(id=campaign_id)

        for i in range(min(x_init, x_final), max(x_init, x_final)):
            for j in range(min(y_init, y_final), max(y_init, y_final)):
                tile, created = Tile.objects.get_or_create(campaign=campaign, x=i, y=j)
                tile.tile_type = tile_type
                tile.save()
    
        self.stdout.write(self.style.SUCCESS(f'Successfully created ({tile_type}) tiles from ({x_init},{y_init}) to ({x_final},{y_final }) in the campaign {campaign_id}: {campaign.name}'))
