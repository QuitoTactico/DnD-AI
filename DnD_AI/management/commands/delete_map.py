from DnD_AI.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Delete an entire map using an initial and final point. Rectancle selection'

    def handle(self, *args, **kwargs):

        print('Select your desired campaign from these:\n')
        for campaign_sample in Campaign.objects.all():
            print(campaign_sample)

        while True:
            campaign_id = int(input('Campaign id: '))
            campaign = Campaign.objects.filter(id=campaign_id)
            if campaign.count() == 1:
                campaign = campaign.first()
                break
            else:
                print('Invalid campaign id. Try again.')

        campaign_id = campaign.id

        # Elimina todos los tiles que coinciden con campaign_id
        tiles_counter = Tile.objects.filter(campaign_id=campaign_id).delete()[0]

        # Elimina todos los tesoros que coinciden con campaign_id
        treasures_counter = Treasure.objects.filter(campaign_id=campaign_id).delete()[0]
        
        # Elimina todos los npc que coinciden con campaign_id
        npc_counter = Character.objects.filter(campaign_id=campaign_id, is_playable=False).delete()[0]

        # Elimina todos los monstruos que no son bosses clave y que coinciden con campaign_id
        monsters_counter = Monster.objects.filter(campaign_id=campaign_id, is_boss=False, is_key=False).delete()[0]

        # Elimina todos los monstruos clave que no son bosses y que coinciden con campaign_id
        key_monsters_counter = Monster.objects.filter(campaign_id=campaign_id, is_boss=False, is_key=True).delete()[0]

        # Elimina todos los jefes no clave que coinciden con campaign_id
        optional_bosses_counter = Monster.objects.filter(campaign_id=campaign_id, is_boss=True, is_key=False).delete()[0]


        self.stdout.write(self.style.SUCCESS(f'Successfully deleted the map of the campaign [{campaign_id}]: {campaign.name}'))

        # deletion stats
        self.stdout.write(self.style.SUCCESS(f'Deleted tiles: {tiles_counter}'))
        self.stdout.write(self.style.SUCCESS(f'Deleted treasures: {treasures_counter}'))
        self.stdout.write(self.style.SUCCESS(f'Deleted npcs: {npc_counter}'))
        self.stdout.write(self.style.SUCCESS(f'Deleted common monsters: {monsters_counter}'))
        self.stdout.write(self.style.SUCCESS(f'Deleted key monsters: {key_monsters_counter}'))
        self.stdout.write(self.style.SUCCESS(f'Deleted optional bosses: {optional_bosses_counter}'))
        total_deletions = tiles_counter + treasures_counter + monsters_counter + key_monsters_counter + optional_bosses_counter
        self.stdout.write(self.style.SUCCESS(f'Total deletions: {total_deletions}'))