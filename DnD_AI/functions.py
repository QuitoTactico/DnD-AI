from .models import *
from .default import *

from random import randint  # to roll the dice

#from django.conf import settings   # to image access
#import os          

from bokeh.plotting import figure, show                             # for plotting (map)
from bokeh.models import Range1d, Span, CrosshairTool, HoverTool    # for plot personalization (map components)
from bokeh.embed import components                                  # for plot html rendering (for the front-end)

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




# -------------------------------- COMBAT ---------------------------------------

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


# ---------------------------------------- ENTITY SELECTION ---------------------------------------------


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

def target_selection_by_name(monster_name):
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

def target_selection_by_id(monster_id):
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

def get_monsters_in_range(player:Character, monsters):
    monsters_in_range = []
    for monster in monsters:
        if abs(player.x - monster.x) <= player.weapon.range and abs(player.y - monster.y) <= player.weapon.range:
            monsters_in_range.append(monster)
    return monsters_in_range


# ------------------------------------------------ MAP --------------------------------------------------


def create_map(player:Character, characters, monsters, treasures, objective:Monster=None, host:str=None, show_map:bool=False) -> tuple:

    map = figure(active_scroll='wheel_zoom', 
                 title="", 
                 aspect_scale=1, 
                 sizing_mode='scale_height', 
                 align='center', 
                 min_height=410, 
                 min_width=410,
                 background_fill_alpha=0.05,
                 border_fill_alpha=0,
                 outline_line_color='white')

    # modifying the borders and background of the map
    map.outline_line_alpha = 0.1
    map.axis.axis_line_color = "white"
    map.axis.axis_line_alpha = 0.1
    map.axis.major_tick_line_alpha = 0
    map.axis.minor_tick_line_alpha = 0
    map.axis.major_label_text_color = "white"
    map.yaxis.major_label_orientation = "vertical"
    #map.outline_line_color = "white"

    # deleting the toolbar, they're not going to use it
    map.toolbar.logo = None
    map.toolbar_location = None
    

    # adding crosshair 
    width = Span(dimension="width", line_dash="dotted", line_alpha=0.5, line_width=1, line_color="white")
    height = Span(dimension="height", line_dash="dotted", line_alpha=0.5, line_width=1, line_color="white")
    map.add_tools(CrosshairTool(overlay=[width, height]))

    # adding crosshair hover functions, like showing the entities information
    ENTITY_TOOLTIPS = """
                <div>
                    <div style="color: @color">
                        <center>
                        <span style="font-size: 17px; font-weight: bold; text-align:center">@name</span>
                        </center>
                    </div>
                    <div>
                        <center>
                        <span style="font-size: 15px; color: @weapon_color; text-align:center; font-weight: bold">@weapon_name</span>
                        <img src=@weapon_icon height=20 style="background-color: #212529">
                        <hr/>
                        <div><span style="font-size: 10px; color: #696; text-align:center;">@raceclass</span></div>
                        <div><span style="font-size: 10px; color: #696; text-align:center;">@LVL</span></div>
                        <div><span style="font-size: 10px; color: #696; text-align:center;">HP: @HP/@HP_max</span></div>
                        <div><span style="font-size: 10px; color: #696; text-align:center;">Range: @RNG</span></div>
                        <div><span style="font-size: 10px; color: #696; text-align:center;">X:@real_x{0.}, Y:@real_y{0.}</span></div>
                        </center>
                    </div>
                </div>
            """
    
    TREASURE_TOOLTIPS = """
                <div>
                    <div style="color: @color">
                        <center>
                        <span style="font-size: 17px; font-weight: bold; text-align:center">@name</span>
                        </center>
                    </div>
                    <div>
                        <center>
                        <hr/>
                        <div><span style="font-size: 10px; color: #696; text-align:center;">@inv</span></div>
                        <div><span style="font-size: 10px; color: #696; text-align:center;">X:@real_x{0.}, Y:@real_y{0.}</span></div>
                        </center>
                    </div>
                </div>
            """
    #map.add_tools(HoverTool(tooltips= [("name", "$name"), ('location', '(${$x-(10)}{0.}, $y{0.})')]))
    #names_list = [character.name for character in characters] + [monster.name for monster in monsters]
    #hover = 

    # setting the initial map center and range. The player will be the center with a visual range of 2.5
    map.x_range = Range1d(start=(player.x)-2.5, end=(player.x)+3.5) # -2, +3
    map.y_range = Range1d(start=(player.y)-2.5, end=(player.y)+3.5) # -2, +3

    range_color,range_alpha = ('red',0.65) if len(get_monsters_in_range(player, monsters)) != 0 else ('gray',0.5)
    
    map.block(hatch_pattern='diagonal_cross', 
                hatch_scale=8, 
                hatch_weight=0.5,
                hatch_color=range_color, 
                hatch_alpha=range_alpha, #55, 65
                fill_alpha=0, 
                line_alpha=0, 
                line_color=range_color, 
                x=(player.x)-(player.weapon.range), 
                y=(player.y)-(player.weapon.range), 
                width=(player.weapon.range*2)+1, 
                height=(player.weapon.range*2)+1)
    
    # objective highlight
    if objective is not None:
        obj_color = 'deeppink' if objective.is_boss else 'red'
        obj_dash = 'dashed' if objective.is_key else 'solid'
        #map.circle(x=objective.x+0.5, y=objective.y+0.5, radius=1, fill_alpha=0, line_color=obj_color, line_dash=obj_dash, line_width=2)
        map.circle(x=objective.x+0.5, y=objective.y+0.5, radius=0.7, fill_alpha=0, line_color=obj_color, line_dash=obj_dash, line_width=2)

    # player highlight
    #map.circle(x=player.x+0.5, y=player.y+0.5, radius=1, fill_alpha=0, line_color='green', line_width=2)
    
    # adding the entities to the map
    entities = list(characters) + list(monsters)
    entity_data = {
        'x': [entity.x + 0.5 for entity in entities],
        'y': [entity.y + 0.5 for entity in entities],
        'raceclass' : [f'{character.character_race} {character.character_class}' if character.character_race != character.character_class else character.character_class for character in characters] + [f'{monster.monster_race} {monster.monster_class}' if monster.monster_race != monster.monster_class else monster.monster_class for monster in monsters],
        'LVL': [f'LVL: {character.level}' for character in characters]+['' for _ in monsters],
        'HP': [entity.health for entity in entities],
        'HP_max': [entity.max_health for entity in entities],
        'RNG' : [entity.weapon.range for entity in entities],
        'icon_x': [entity.x +0.1 for entity in entities],
        'icon_y': [entity.y + 0.9 for entity in entities],
        'real_x': [entity.x for entity in entities],
        'real_y': [entity.y for entity in entities],
        'name': [entity.name for entity in entities],
        'icon': [entity.icon.url for entity in entities],
        'weapon_icon': [entity.weapon.image.url for entity in entities],
        'weapon_name': [f'{entity.weapon.name}+{entity.weapon.level}' if entity.weapon.level != 0 else entity.weapon.name for entity in entities],
        'weapon_color': ['orange' if entity.weapon.damage_type == 'Physical' else 'cyan' if entity.weapon.damage_type == 'Magical' else 'black' for entity in entities],
        'color': [('green' if character.id == player.id else 'blue') if character.is_playable else 'gold' for character in characters] + ['deeppink' if monster.is_boss else 'red' for monster in monsters],
        'dash': ['solid' for _ in characters]+['dashed' if monster.is_key else 'solid' for monster in monsters],
        'type': ['character' if character.id != player.id else 'player' for character in characters] + ['boss' if monster.is_boss else 'monster' for monster in monsters]
    }

    map.rect(x='x', y='y', width=0.8, height=0.8, fill_color='color', fill_alpha=0.3, line_alpha=0, source=entity_data)  
    map.image_url(url='icon', x='icon_x', y='icon_y', h=0.8, w=0.8, name='name', source=entity_data)
    map.image_url(url='weapon_icon', x='x', y='y', h=0.4, w=0.4, name='weapon_name', source=entity_data)
    entities = map.rect(x='x', y='y', width=0.8, height=0.8, line_color='color', line_dash='dash', fill_alpha=0, line_width=2, name='name', source=entity_data)
    entities.tags = ['entity']


    treasure_data = {
        'x' : [treasure.x + 0.5 for treasure in treasures],
        'y' : [treasure.y + 0.5 for treasure in treasures],
        'icon_x' : [treasure.x +0.1 for treasure in treasures],
        'icon_y' : [treasure.y +0.9 for treasure in treasures],
        'real_x' : [treasure.x for treasure in treasures],
        'real_y' : [treasure.y for treasure in treasures],
        'color' : [('gold' if treasure.treasure_type == 'Gold' else 'dimgray' if treasure.discovered else '#212121') if treasure.treasure_type != 'Weapon' or not treasure.discovered else 'orange' if treasure.weapon.damage_type == 'Physical' else 'cyan' if treasure.weapon.damage_type == 'Magical' else 'black' for treasure in treasures],
        'inv': [(treasure.inventory[1:-1] if treasure.discovered  else '???') if treasure.treasure_type!='Weapon' else  (f'DMG: {treasure.weapon.damage}, RNG: {treasure.weapon.range}' if treasure.discovered else '') for treasure in treasures],
        'icon' : [treasure.icon.url for treasure in treasures],
        'name': [('Discovered '+treasure.treasure_type if treasure.discovered else treasure.treasure_type if treasure.treasure_type != 'Weapon' else 'Undiscovered Weapon') if treasure.treasure_type!='Weapon' or not treasure.discovered else treasure.weapon.name for treasure in treasures],
    }

    map.image_url(url='icon', x='icon_x', y='icon_y', h=0.8, w=0.8, name='name', source=treasure_data)
    treasure = map.rect(x='x', y='y', width=0.8, height=0.8, fill_alpha=0, line_alpha=0, name='name', source=treasure_data)
    treasure.tags = ['treasure']

    map.add_tools(HoverTool(renderers=map.select(tags=['entity']) , tooltips= ENTITY_TOOLTIPS))
    map.add_tools(HoverTool(renderers=map.select(tags=['treasure']) , tooltips= TREASURE_TOOLTIPS))


    if show_map:
        map.sizing_mode = 'scale_height'
        show(map)
        map.sizing_mode = 'scale_width'

    map_script, map_div = components(map)
    return map_script, map_div



# ---------------------------------------------- RESOURCES ------------------------------------------------


'''
MAP PAST TRIES  (DON'T DELETE, PLEASE)

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

    #logo_src = ColumnDataSource(data=dict(url=['/..'+player.icon.url]))
    #icon_path = PurePath(player.icon.url)
    #icon_path = icon_path.__str__()
    #('stretch_width', 'stretch_height', 'stretch_both', 'scale_width', 'scale_height', 'scale_both', 'fixed', 'inherit')

    #map.x_range.start = (player.x)-2
    #map.image_url(url=['http://127.0.0.1:8000'+player.icon.url], x=0, y=0, h=1, w=1)

    map.aspect_scale = 1
    map.sizing_mode = 'stretch_both'
    map.aspect_scale = 1

    
    for character in characters:
        if character.id != player.id:
            character_x, character_y = character.x, character.y

            character_color = 'blue' if character.is_playable else 'yellow'
            map.rect(x=character_x+0.5, y=character_y+0.5, width=0.8, height=0.8, fill_color=character_color, fill_alpha=0.3, line_alpha=0)

            if host:
                icon_path, weapon_path = character.icon.url, character.weapon.image.url
            else:
                icon_path, weapon_path = os.path.join(settings.BASE_DIR, character.icon.url[1:]).replace('\\', '/'), os.path.join(settings.BASE_DIR, character.weapon.image.url[1:]).replace('\\', '/')

            map.image_url(url=[icon_path], x=character_x+0.1, y=character_y+0.9, h=0.8, w=0.8, name=character.name)
            map.image_url(url=[weapon_path], x=character_x+0.5, y=character_y+0.5, h=0.4, w=0.4, name=character.weapon.name)
            borde_characters = map.rect(x=character_x+0.5, y=character_y+0.5, width=0.8, height=0.8, line_color=character_color, fill_alpha=0, line_width=2, name=character.name)
            borde_characters.tags = ['characters']


    for monster in monsters:
        monster_x, monster_y = monster.x, monster.y

        monster_line_dash = 'dashed' if monster.is_key else 'solid'
        monster_color = 'deeppink' if monster.is_boss else 'red'
        map.rect(x=monster_x+0.5, y=monster_y+0.5, width=0.8, height=0.8, line_color=monster_color, line_dash=monster_line_dash, fill_color=monster_color, fill_alpha=0.3, line_alpha=0, name=monster.name)

        if host:
            icon_path, weapon_path = monster.icon.url, monster.weapon.image.url
        else:
            icon_path, weapon_path = os.path.join(settings.BASE_DIR, monster.icon.url[1:]).replace('\\', '/'), os.path.join(settings.BASE_DIR, monster.weapon.image.url[1:]).replace('\\', '/')
        map.image_url(url=[icon_path], x=monster_x+0.1, y=monster_y+0.9, h=0.8, w=0.8, name=monster.name)
        map.image_url(url=[weapon_path], x=monster_x+0.5, y=monster_y+0.5, h=0.4, w=0.4, name=monster.weapon.name)
        borde_monsters = map.rect(x=monster_x+0.5, y=monster_y+0.5, width=0.8, height=0.8, line_color=monster_color, line_dash=monster_line_dash, fill_color=monster_color, fill_alpha=0, line_width=2, name=monster.name)
        borde_monsters.tags = ['monsters']

    # Player
    player_x, player_y = player.x, player.y
    #map.rect(name=player.name, x=player_x+0.5, y=player_y+0.5, width=0.8, height=0.8, line_color="green", fill_color='green', fill_alpha=0.3, line_width=2)
    map.rect(name=player.name, x=player_x+0.5, y=player_y+0.5, width=0.8, height=0.8, line_color="green", fill_color='green', fill_alpha=0.3, line_alpha=0)
    icon_path   = player.icon.url if host else os.path.join(settings.BASE_DIR, player.icon.url[1:]).replace('\\', '/') 
    weapon_path = player.weapon.image.url if host else os.path.join(settings.BASE_DIR, player.weapon.image.url[1:]).replace('\\', '/')
    map.image_url(url=[icon_path], x=player_x+0.1, y=player_y+0.9, h=0.8, w=0.8)
    map.image_url(url=[weapon_path], x=player_x+0.5, y=player_y+0.5, h=0.4, w=0.4)
    borde_player = map.rect(name=player.name, x=player_x+0.5, y=player_y+0.5, width=0.8, height=0.8, line_color="green", fill_color='green', fill_alpha=0, line_width=2)
    borde_player.tags = ['player']


MAP LABELS

unexpected attribute 'theme' to figure, possible attributes are above, active_drag, active_inspect, active_multi, active_scroll, active_tap, align, aspect_ratio, aspect_scale, attribution, background_fill_alpha, background_fill_color, below, border_fill_alpha, border_fill_color, center, context_menu, css_classes, css_variables, disabled, elements, extra_x_ranges, extra_x_scales, extra_y_ranges, extra_y_scales, flow_mode, frame_align, frame_height, frame_width, height, height_policy, hidpi, hold_render, inner_height, inner_width, js_event_callbacks, js_property_callbacks, left, lod_factor, lod_interval, lod_threshold, lod_timeout, margin, match_aspect, max_height, max_width, min_border, min_border_bottom, min_border_left, min_border_right, min_border_top, min_height, min_width, name, outer_height, outer_width, outline_line_alpha, outline_line_cap, outline_line_color, outline_line_dash, outline_line_dash_offset, outline_line_join, outline_line_width, output_backend, renderers, reset_policy, resizable, right, sizing_mode, styles, stylesheets, subscribed_events, syncable, tags, title, title_location, toolbar, toolbar_inner, toolbar_location, toolbar_sticky, tools, tooltips, visible, width, width_policy, x_axis_label, x_axis_location, x_axis_type, x_minor_ticks, x_range, x_scale, y_axis_label, y_axis_location, y_axis_type, y_minor_ticks, y_range or y_scale

'''