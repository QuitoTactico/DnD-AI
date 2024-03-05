from .models import *
from random import randint
from .default import *

def roll_dice(): 
    return randint(1, 20)

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
            