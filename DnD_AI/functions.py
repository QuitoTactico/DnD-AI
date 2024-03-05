from .models import *
from random import randint
from .default import *

def roll_dice(): 
    return randint(1, 20)

def create_every_template_weapon():
    for weapon in DEFAULT_WEAPON_STATS:
        if not Weapon.objects.filter(name=weapon).exists():
            Weapon.objects.create(name=weapon, 
                                  is_template=True, 
                                  damage=DEFAULT_WEAPON_STATS[weapon]['damage'], 
                                  range=DEFAULT_WEAPON_STATS[weapon]['range'], 
                                  image=DEFAULT_WEAPON_STATS[weapon]['image'],
                                  is_ranged=DEFAULT_WEAPON_STATS[weapon]['is_ranged'],
                                  physical_description=DEFAULT_WEAPON_STATS[weapon]['physical_description'],
                                  damage_type=DEFAULT_WEAPON_STATS[weapon]['damage_type'])
            