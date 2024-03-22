from .models import *
from random import randint
from .default import *

from bokeh.plotting import figure, show
from bokeh.models import Range1d, Span, CrosshairTool, HoverTool
from django.conf import settings
import os

def roll_dice(): 
    return randint(1, 20)


# BEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEETA, Just simulating btw
def level_up_option(level:int) -> str:
    '''# THIS OPTION WILL BE MADE IN FRONT BY COCK, PROBABLY, I'M JUST SIMULATING IT. CHANGE FULL_COMBAT() WHEN IT'S DONE. 
    
    just returns 'stats' or 'weapon' '''

    menu = f'''Duuuuude, wha du u waaaant, u are now level {level} omggg 
    1. Subir las stats bro
    2. Tirar facha modificando mi arma uwu

    -> '''
    print(menu)

    opcion = input().lower()
    if opcion not in ['stats', 'weapon']:
        print('pero qué te pasa ome, mera deforme nea')
        return level_up_option(level)
    else:
        print('waos')
        return opcion



def attack(attacker:Character|Monster, objective:Character|Monster, attacker_dice:int = roll_dice()) -> dict:
    '''### The attack function will calculate the result of an attack from an attacker to an objective. Any of them can be a character or a monster\n
    The attack will be calculated based on the attacker's attack stats, weapon damage, weapon damage type and the objective's defense. The intensity varies depending on the dice result, the higher the result, the higher the damage.\n
    If the dice result is 20, the attack will be a CRITICAL HIT, doubling the damage. \n
    returns a dictionary with the attack, the damage dealt, a boolean indicating if the objective was killed and a boolean indicating if the hit was critic.'''


    # Each plus point in the stats will increase the damage by 10% of the base damage
    if attacker.weapon.damage_type == 'Physical':
        attack = attacker.weapon.damage + int((attacker.weapon.damage*0.1)*attacker.strength)
        defense = objective.physical_resistance
    elif attacker.weapon.damage_type == 'Magical': 
        attack = attacker.weapon.damage + int((attacker.weapon.damage*0.1)*attacker.intelligence)
        defense = objective.magical_resistance
    else: # the attacker damage will be calculated as item damage
        attack = attacker.weapon.damage + int((attacker.weapon.damage*0.1)*attacker.recursiveness)
        defense = objective.constitution

    # The damage will be calculated as the difference between the attack and the defense, multiplied by the dice result
    # The dice result will be used to calculate the damage, the higher the result, the higher the damage
    # a dice result of 20 will double the damage, that's a CRITICAL HIT!
    damage_dealt = int((attack - defense)*(attacker_dice/20)) if attacker_dice != 20 else (attack - defense)*2
    objective.health -= damage_dealt

    objective_killed = False
    if objective.health < 0:
        objective.kill()
        objective_killed = True

    was_critical_hit = True if attacker_dice == 20 else False

    return {'attack': attack, 'damage_dealt': damage_dealt, 'objective_killed': objective_killed, 'was_critical_hit': was_critical_hit}
    

# The combat function will calculate the result of a combat_turn between a player and a monster
def combat_turn(player:Character, monster:Monster, player_dice:int = roll_dice(), monster_dice:int = roll_dice()) -> dict[dict, dict]:
    '''### The combat function will calculate the result of a combat between a player and a monster, both attacking (if the first attacked doesn't dies).\n
    The one with the highest dexterity will attack first. If the dexterity is the same, the dice result will be used to determine the first attack. If they're also the same, the order will be random. \n
    Calls to the attack function to calculate the damage dealt by the player and the monster. \n
    Returns a dictionary with player and monster dead status, and also two dictionaries: one for the player's attack results and another for the monster's attack results. \n

    Keys valid for the returned dictionary:
    - 'player_died'
    - 'monster_died'
    - 'player_result'
    - 'monster_result'\n
    
    Keys valid for 'player_results' and 'monster_results' dictionaries: 
    - 'attack'
    - 'damage_dealt'
    - 'objective_killed'
    - 'was_critical_hit'\n
    '''

    if player.dexterity > monster.dexterity:
        first = 'player'
    elif player.dexterity < monster.dexterity:
        first = 'monster'
    else:  # they have the same dexterity
        if player_dice > monster_dice:
            first = 'player'
        elif player_dice < monster_dice:
            first = 'monster'
        else: # damn, they have the same dexterity and the same dice result XD, let's make it random
            first = 'player' if randint(0, 1) == 1 else 'monster'

    player_died, monster_died = False, False
    if first == 'player':
        player_result = attack(player, monster, player_dice)
        monster_died = player_result['objective_killed']
        if not monster_died:
            monster_result = attack(monster, player, monster_dice)
            player_died = monster_result['objective_killed']
    else:
        monster_result = attack(monster, player, monster_dice)
        player_died = monster_result['objective_killed']
        if not player_died:
            player_result = attack(player, monster, player_dice)
            monster_died = player_result['objective_killed']

    return {'player_died': player_died, 'monster_died': monster_died, 'player_result': player_result, 'monster_result': monster_result}


# The full_combat function will calculate the result of a full combat between a player and a monster
# They will continue until someone dies
def full_combat(player:Character, monster:Monster):
    '''### The full_combat function will calculate the result of a full combat between a player and a monster. They will continue until someone dies.\n
    Calls to the combat_turn function to calculate the result of each turn. \n
    Returns a dictionary with the player and monster dead status, and also a list with the results of each turn. \n
    The list will contain dictionaries with the results of each turn, with the same keys as the combat_turn function. \n
    '''

    combat_results = []
    player_died, monster_died = False, False
    while not player_died and not monster_died:
        turn_result = combat_turn(player, monster)
        player_died = turn_result['player_died']
        monster_died = turn_result['monster_died']
        combat_results.append(turn_result)


        
        if player.exp > player.exp_top:
            # ---------------------------------------- COCK, MODIFY THIS WHEN YOU'RE DONE WITH THE LEVEL_UP OPTION MENU
            option = level_up_option()
            if option == 'stats':
                player.level_up_stat()
            if option == 'weapon':
                player.level_up_weapon()


    return {'player_died': player_died, 'monster_died': monster_died, 'combat_results': combat_results}


def create_map(player:Character, characters, monsters, host:str=None, show_map:bool=False):
    '''
    #logo_src = ColumnDataSource(dict(url = player.icon.url))
    #logo_src = ColumnDataSource(player.icon.url)
    logo_src = ColumnDataSource(data=dict(url=[player.icon.url]))
    map = figure(width = 500, height = 500, title="")
    map.toolbar.logo = None
    map.toolbar_location = None
    map.x_range=Range1d(start=0, end=1)
    map.y_range=Range1d(start=0, end=1)
    #map.xaxis.visible = None
    #map.yaxis.visible = None
    #map.xgrid.grid_line_color = None
    #map.ygrid.grid_line_color = None
    #map.image_url(url='url', x=0.05, y = 0.85, h=0.7, w=0.9, source=logo_src)
    map.image_url(url=player.icon.url, x=0.05, y = 0.85, h=0.7, w=0.9, source=logo_src)
    map.outline_line_alpha = 0 
    show(map)
    '''
    #logo_src = ColumnDataSource(data=dict(url=['/..'+player.icon.url]))
    #icon_path = PurePath(player.icon.url)
    #icon_path = icon_path.__str__()
    #('stretch_width', 'stretch_height', 'stretch_both', 'scale_width', 'scale_height', 'scale_both', 'fixed', 'inherit')
    map = figure(active_scroll='wheel_zoom', 
                 title="", 
                 aspect_scale=1, 
                 sizing_mode='scale_height', 
                 align='center', 
                 min_height=410, 
                 min_width=410)
    
    # añado herramientas bacanas al gráfico
    width = Span(dimension="width", line_dash="dotted", line_alpha=0.4, line_width=1)
    height = Span(dimension="height", line_dash="dotted", line_alpha=0.4, line_width=1)
    map.add_tools(CrosshairTool(overlay=[width, height]))
    TOOLTIPS = """
                <div>
                    <div>
                        <span style="font-size: 17px; font-weight: bold;">$name</span>
                    </div>
                    <div>
                        <span style="font-size: 15px;">Location</span>
                        <span style="font-size: 10px; color: #696;">(x, $y)</span>
                    </div>
                </div>
            """

    #map.add_tools(HoverTool(tooltips= [("name", "$name"), ('location', '(${$x-(10)}{0.}, $y{0.})')]))
    map.add_tools(HoverTool(tooltips= TOOLTIPS))


    map.toolbar.logo = None
    map.toolbar_location = None
    map.x_range = Range1d(start=(player.x)-2, end=(player.x)+3)
    map.y_range = Range1d(start=(player.y)-2, end=(player.y)+3)
    #map.x_range.start = (player.x)-2
    #map.image_url(url=['http://127.0.0.1:8000'+player.icon.url], x=0, y=0, h=1, w=1)



    for character in characters:
        character_x, character_y = character.x, character.y
        if host:
            icon_path, weapon_path = character.icon.url, character.weapon.image.url
        else:
            icon_path, weapon_path = os.path.join(settings.BASE_DIR, character.icon.url[1:]).replace('\\', '/'), os.path.join(settings.BASE_DIR, character.weapon.image.url[1:]).replace('\\', '/')
        map.image_url(url=[icon_path], x=character_x+0.1, y=character_y+0.9, h=0.8, w=0.8, name=character.name)
        map.image_url(url=[weapon_path], x=character_x+0.5, y=character_y+0.5, h=0.4, w=0.4, name=character.weapon.name)
        if character.is_playable:
            map.rect(x=character_x+0.5, y=character_y+0.5, width=0.8, height=0.8, line_color="blue", fill_alpha=0, line_width=2, name=character.name)
        else:
            map.rect(x=character_x+0.5, y=character_y+0.5, width=0.8, height=0.8, line_color="yellow", fill_alpha=0, line_width=2, name=character.name)

    for monster in monsters:
        monster_x, monster_y = monster.x, monster.y
        if host:
            icon_path, weapon_path = monster.icon.url, monster.weapon.image.url
        else:
            icon_path, weapon_path = os.path.join(settings.BASE_DIR, monster.icon.url[1:]).replace('\\', '/'), os.path.join(settings.BASE_DIR, monster.weapon.image.url[1:]).replace('\\', '/')
        map.image_url(url=[icon_path], x=monster_x+0.1, y=monster_y+0.9, h=0.8, w=0.8, name=monster.name)
        map.image_url(url=[weapon_path], x=monster_x+0.5, y=monster_y+0.5, h=0.4, w=0.4, name=monster.weapon.name)
        map.rect(x=monster_x+0.5, y=monster_y+0.5, width=0.8, height=0.8, line_color="red", fill_alpha=0, line_width=2, name=monster.name)

    # Player
    player_x, player_y = player.x, player.y
    if host:
        icon_path, weapon_path = player.icon.url, player.weapon.image.url
    else:
        icon_path, weapon_path = os.path.join(settings.BASE_DIR, player.icon.url[1:]).replace('\\', '/'), os.path.join(settings.BASE_DIR, player.weapon.image.url[1:]).replace('\\', '/')
    map.image_url(url=[icon_path], x=player_x+0.1, y=player_y+0.9, h=0.8, w=0.8)
    map.image_url(url=[weapon_path], x=player_x+0.5, y=player_y+0.5, h=0.4, w=0.4)
    map.rect(x=player_x+0.5, y=player_y+0.5, width=0.8, height=0.8, line_color="green", fill_alpha=0, line_width=2)
 
    map.outline_line_alpha = 0
    '''
    map.aspect_scale = 1
    map.sizing_mode = 'stretch_both'
    map.aspect_scale = 1
    '''
    if show_map:
        map.sizing_mode = 'scale_height'
        show(map)
        map.sizing_mode = 'scale_width'
    return map

def player_selection(player_name):
    if player_name:
        try:
            player = Character.objects.get(name__iexact=player_name)
        except:
            try:
                # If the name of the character is not found, it tries to find a character whose name contains the string entered
                player = Character.objects.filter(name__icontains=player_name).first()
                if player == None:
                    # If there is no character containing the name entered, it selects the first playable character in the database
                    player = Character.objects.filter(is_playable=True).first()
            except:
                player = Character.objects.filter(is_playable=True).first()
    else:
        # If the player label is not sent, it selects the first playable character in the database
        # We can change this to let the player select the character by himself, but we'll see.
        try:
            player = Character.objects.filter(is_playable=True).first()
        except:
            player = Character.objects.create()
            player.save()
    return player

def monster_selection(monster_name):
    if monster_name:
        try:
            monster = Monster.objects.get(name__iexact=monster_name)
        except:
            try:
                # If the name of the monster is not found, it tries to find a monster whose name contains the string entered
                monster = Monster.objects.filter(name__icontains=monster_name).first()
                if monster == None:
                    # If there is no monster containing the name entered, it selects the first monster in the database
                    monster = Monster.objects.first()
            except:
                monster = Monster.objects.first()
    else:
        # If the monster label is not sent, it selects the first monster in the database
        # We can change this to let the player select the monster by himself, but we'll see.
        try:
            monster = Monster.objects.first()
        except:
            monster = Monster.objects.create()
            monster.save()
    return monster

def monster_selection_by_id(monster_id):
    if monster_id:
        try:
            monster = Monster.objects.get(id=monster_id)
        except:
            try:
                # If the id of the monster is not found, it selects the first monster in the database
                monster = Monster.objects.first()
            except:
                monster = Monster.objects.create()
                monster.save()
    else:
        # If the monster_id label is not sent, it selects the first monster in the database
        # We can change this to let the player select the monster by himself, but we'll see.
        try:
            monster = Monster.objects.first()
        except:
            monster = Monster.objects.create()
            monster.save()
    return monster
