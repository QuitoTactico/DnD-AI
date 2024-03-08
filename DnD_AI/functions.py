from .models import *
from random import randint
from .default import *

def roll_dice(): 
    return randint(1, 20)


# no está listo
def attack(attacker:Character|Monster, objective:Character|Monster, dice:int):
    if attacker.weapon.damage_type == 'Physical':
        attack = attacker.strength + attacker.weapon.damage
        defense = objective.physical_resistance
    elif attacker.weapon.damage_type == 'Magical': 
        attack = attacker.intelligence + attacker.weapon.damage
        defense = objective.magical_resistance
    else:
        attack = attacker.intelligence + attacker.weapon.damage
        defense = objective.constitution
    


# no está listo
def combat(character:Character, monster:Monster, character_dice:int, monster_dice:int = roll_dice()) -> None:
    monster_attack = monster.strength
    if character.dexterity > monster.dexterity:
    
        monster_attack = monster.strength
        character.health -= 1