from DnD_AI.models import *
from DnD_AI.default import *
from django.core.management.base import BaseCommand

def create_every_template_weapon():
    for weapon_name in DEFAULT_WEAPON_STATS:
        if not Weapon.objects.filter(name=weapon_name).exists():
            Weapon.objects.create(name=weapon_name, 
                                  is_template=True, 
                                  damage=DEFAULT_WEAPON_STATS[weapon_name]['damage'], 
                                  range=DEFAULT_WEAPON_STATS[weapon_name]['range'], 
                                  image=DEFAULT_WEAPON_STATS[weapon_name]['image'],
                                  is_ranged=DEFAULT_WEAPON_STATS[weapon_name]['is_ranged'],
                                  physical_description=DEFAULT_WEAPON_STATS[weapon_name]['physical_description'],
                                  damage_type=DEFAULT_WEAPON_STATS[weapon_name]['damage_type'],
                                  weapon_type=DEFAULT_WEAPON_STATS[weapon_name]['weapon_type'])

class Command(BaseCommand):
    help = 'Creates the default weapons in the database'

    def handle(self, *args, **kwargs):
        create_every_template_weapon()
        self.stdout.write(self.style.SUCCESS('Successfully created every template weapon'))