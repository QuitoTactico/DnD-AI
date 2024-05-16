from DnD_AI.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Helps to generate a map for an existing campaign'

    def handle(self, *args, **kwargs):

        print('Select your desired campaign from these:\n')
        for campaign_sample in Campaign.objects.all():
            print(campaign_sample)

        
        campaign_id = int(input('Campaign id: '))
        campaign = Campaign.objects.get(id=campaign_id)

        

        try:
            tiles = Tile.objects.filter(campaign_id=campaign.id)

            tile_positions = set()
            tile_types = set()

            for tile in tiles:
                position = (tile.x, tile.y)
                tile_type = tile.tile_type

                if position in tile_positions:
                    self.stdout.write(self.style.ERROR(f'Duplicate tile found at position ({tile.x}, {tile.y})'))
                    break
                else:
                    tile_positions.add(position)
                    tile_types.add(tile_type)

                    print(tile.x, tile.y, tile_type)

            if len(tile_types) > 0:
                self.stdout.write(f'Tile types found: {", ".join(tile_types)}')
            else:
                self.stdout.write('No tile types found')

            self.stdout.write(self.style.SUCCESS(f'Successfully checked a {campaign.size_x}x{campaign.size_y} map for the campaign [{campaign_id}]: {campaign.name}'))
        except:
            self.stdout.write(self.style.ERROR(f'An error occurred while checking the map for the campaign [{campaign_id}]: {campaign.name}'))
