from DnD_AI.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Delete some tiles from Models.Tile using an initial and final point. Rectancle selection'

    def handle(self, *args, **kwargs):

        print('Select your desired campaign from these:\n')
        for campaign_sample in Campaign.objects.all():
            print(campaign_sample)

        
        campaign_id = int(input('Campaign id: '))
        campaign = Campaign.objects.get(id=campaign_id)

        print('Possible tile types: grass, dirt, path, dungeon, boss, god, psycho, hell, spawn, portal. \nOr just ENTER to delete any type')
        tile_type = input('Tile type: ').lower()
        if tile_type in  ['','all', None, ' '] : tile_type = 'any'
        x_init, y_init = list(map(int,input('From (x y separed by one space): ').split(' ')))
        x_final, y_final = list(map(int,input('To   (x y separed by one space): ').split(' ')))

        for i in range(min(x_init, x_final), max(x_init, x_final)):
            for j in range(min(y_init, y_final), max(y_init, y_final)):

                tiles = Tile.objects.filter(campaign_id=campaign_id, x=i, y=j) if tile_type == 'any' else Tile.objects.filter(campaign_id=campaign_id, x=i, y=j, tile_type=tile_type) 
                for tile in tiles:
                    tile.delete()
                
                treasures = Treasure.objects.filter(campaign_id=campaign_id, x=i, y=j)
                for treasure in treasures:
                    treasure.delete()
                    
                monsters = Monster.objects.filter(campaign_id=campaign_id, x=i, y=j, is_boss=False, is_key=False)      
                for monster in monsters:
                        monster.delete()           
                
    
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted ({tile_type}) tiles from ({x_init},{y_init}) to ({x_final},{y_final }) in the campaign [{campaign_id}]: {campaign.name}'))
