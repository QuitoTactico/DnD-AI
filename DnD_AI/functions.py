from .models import *
from .default import *

from random import randint, choice  # to roll the dice
import numpy as np

#from django.conf import settings   # to image access
#import os          

from bokeh.plotting import figure, show                             # for plotting (map)
                                                                    # for plot personalization (map components)
from bokeh.models import Range1d, Span, CrosshairTool, HoverTool, AdaptiveTicker, ColumnDataSource, MultiPolygons 
from bokeh.embed import components                                  # for plot html rendering (for the front-end)

from .functions_AI import image_generator_DallE, image_generator_StabDiff, ask_world_info_gemini, continue_history_gemini

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

def attack(attacker:Character|Monster, target:Character|Monster, attacker_dice:int = roll_dice(), attacker_is:str = 'player') -> dict:
    '''### The attack function will calculate the result of an attack from an attacker to an objective. Any of them can be a character or a monster\n
    The attack will be calculated based on the attacker's attack stats, weapon damage, weapon damage type and the objective's defense. The intensity varies depending on the dice result, the higher the result, the higher the damage.\n
    If the dice result is 20, the attack will be a CRITICAL HIT, doubling the damage. \n
    returns a dictionary with the attack, the damage dealt, a boolean indicating if the objective was killed and a boolean indicating if the hit was critic.'''


    # Each plus point in the stats will increase the damage by 10% of the base damage
    if attacker.weapon.damage_type == 'Physical':
        attack = attacker.weapon.damage + int((attacker.weapon.damage*0.1)*attacker.strength)
        defense = target.physical_resistance
    elif attacker.weapon.damage_type == 'Magical': 
        attack = attacker.weapon.damage + int((attacker.weapon.damage*0.1)*attacker.intelligence)
        defense = target.magical_resistance
    else: # the attacker damage will be calculated as item damage
        attack = attacker.weapon.damage + int((attacker.weapon.damage*0.1)*attacker.recursiveness)
        defense = target.constitution

    # The damage will be calculated as the difference between the attack and the defense, multiplied by the dice result
    # The dice result will be used to calculate the damage, the higher the result, the higher the damage
    # a dice result of 20 will double the damage, that's a CRITICAL HIT!
    damage_dealt = int((attack - (defense/50)*attack)*(attacker_dice/20)) if attacker_dice != 20 else int((attack - (defense/50)*attack)*2)
    target.health -= damage_dealt
  
    target_killed = True if target.health <= 0 else False

    was_critical_hit = True if attacker_dice == 20 else False
    was_critical_hit_str = ' CRITICAL HIT.' if was_critical_hit else ''

    History.objects.create(campaign=attacker.campaign, author='SYSTEM', text=f'D{attacker_dice}. {attacker.name} did {damage_dealt} points of DMG to {target.name}.{was_critical_hit_str}')

    if was_critical_hit:
        color = 'gold' if attacker_is == 'player' and not attacker.is_playable else 'blue' if attacker_is == 'player' else 'red'
        History.objects.create(campaign=attacker.campaign, author=attacker.name, text='Take that!', color=color)

    if damage_dealt == 0:
        color = 'gold' if attacker_is == 'player' and not attacker.is_playable else 'blue' if attacker_is == 'player' else 'red'
        History.objects.create(campaign=attacker.campaign, author=attacker.name, text='Oh no...', color=color)

    attacker.save()
    target.save()

    return {'attack': attack, 'damage_dealt': damage_dealt, 'target_killed': target_killed, 'was_critical_hit': was_critical_hit}


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
    
    Keys valid for 'player_results' and 'monster_results' dictionaries (if it's not None): 
    - 'attack'
    - 'damage_dealt'
    - 'target_killed'
    - 'was_critical_hit'\n
    '''

    first_by = "By dexterity" 
    if player.dexterity > monster.dexterity:
        first = 'player'
    elif player.dexterity < monster.dexterity:
        first = 'monster'
    else:  # they have the same dexterity
        first_by = "Same dexterity. By dice result" 
        if player_dice > monster_dice:
            first = 'player'
        elif player_dice < monster_dice:
            first = 'monster'
        else: # damn, they have the same dexterity and the same dice result XD, let's make it random
            first_by = 'Same dexterity and dice result (god damn...). By "just luck"'
            first = 'player' if randint(0, 1) == 1 else 'monster'

    History.objects.create(campaign=player.campaign, author='SYSTEM', text=f'{first_by}, {player.name if first=="player" else monster.name} attacks first.')

    player_died, monster_died, player_result, monster_result = False, False, None, None
    if first == 'player':
        if player.is_in_range(monster):
            player_result = attack(player, monster, player_dice, attacker_is='player')
            monster_died = player_result['target_killed']
        if monster_died:
            player_won_combat(player, monster)
        else:
            if monster.is_in_range(player):
                monster_result = attack(monster, player, monster_dice, attacker_is='monster')
                player_died = monster_result['target_killed']
            if player_died:
                player_died_in_combat(player, monster)
    else:
        if monster.is_in_range(player):
            monster_result = attack(monster, player, monster_dice, attacker_is='monster')
            player_died = monster_result['target_killed']
        if player_died:
            player_died_in_combat(player, monster)
        else:
            if player.is_in_range(monster):
                player_result = attack(player, monster, player_dice, attacker_is='player')
                monster_died = player_result['target_killed']
            if monster_died:
                player_won_combat(player, monster)

    return {'player_died': player_died, 'monster_died': monster_died, 'player_result': player_result, 'monster_result': monster_result}

def player_died_in_combat(player:Character, monster:Monster):
    action_image_generation('', 'attack', monster, player)
    Treasure.objects.create(campaign=player.campaign, treasure_type='Tombstone', inventory=player.inventory, x=player.x, y=player.y, discovered=False).save()
    History.objects.create(campaign=player.campaign ,author='SYSTEM', text=f'{player.name} died in combat.').save()
    History.objects.create(campaign=player.campaign ,author=monster.name, text='JA'*randint(2,15), color='red').save()
    player.kill()

def player_won_combat(player:Character, monster:Monster):
    action_image_generation('', 'attack', player, monster)
    loot = monster.get_inventory()
    player.add_all_to_inventory(loot)
    player.exp += monster.exp_drop
    History.objects.create(campaign=player.campaign, author='SYSTEM', text=f'{player.name} killed {monster.name}, got {monster.exp_drop} EXP and {loot}').save()

    if monster.is_key:
        achievement = f"KEY BOSS {monster.name} WAS SLAIN BY {player.name}."
        player.campaign.objective_completed(achievement)
        History.objects.create(campaign=player.campaign, author='SYSTEM', text=f'[ACHIEVEMENT - {achievement}]').save()

        history_progression = continue_history_gemini(achievement=achievement,
                                                      campaign_story=player.campaign.initial_story, 
                                                      campaign_achievements=player.campaign.achievements)
        
        history_progression_filtered = history_progression.replace("\n","<br>")
        History.objects.create(campaign=player.campaign, author='NARRATOR', color='purple', text=f'{history_progression_filtered}.<br><br>Remaining bosses: {player.campaign.objectives_remaining}').save()

    player.save()
    #monster.kill()
    monster.delete()


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
    if player_name is not None:
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
    #res = player.move('up') # for func testing
    #print(res)
    return player

def player_selection_by_id(player_id):
    if player_id:
        try:
            player = Character.objects.get(id=player_id)
        except:
            try:
                # If the id of the character is not found, it selects the first playable character in the database
                player = Character.objects.filter(is_playable=True).first()
            except:
                player = Character.objects.create()
                player.save()
    else:
        # If the player_id label is not sent, it selects the first playable character in the database
        # We can change this to let the player select the character by himself, but we'll see.
        try:
            player = Character.objects.filter(is_playable=True).first()
        except:
            player = Character.objects.create()
            player.save()
    return player

'''
def target_selection_by_name(monster_name, player:Character = None):
    if monster_name:
            try:
                monster = Monster.objects.get(name__iexact=monster_name) if not player else player.get_monsters_in_range(monster_name)[0]
            except:
                try:
                    # If the name of the monster is not found, it tries to find a monster whose name contains the string entered
                    monster = Monster.objects.filter(name__icontains=monster_name).first() if not player else player.get_monsters_in_range(monster_name)[0]
                    if monster == None:
                        # If there is no monster containing the name entered, it selects the first monster in the database
                        #monster = Monster.objects.first()
                        return None
                except:
                    #monster = Monster.objects.first()
                    return None
    else:
            # If the monster label is not sent, it selects the first monster in the database
            # We can change this to let the player select the monster by himself, but we'll see.
            try:
                monster = Monster.objects.first()
            except:
                monster = Monster.objects.create()
                monster.save()
    return monster
'''

def target_selection_by_name(monster_name, player:Character = None, campaign_id:int = None):
    if player:
        possible_targets = player.get_monsters_in_range(monster_name)
        if len(possible_targets) == 0:
            return None
        else:
            return possible_targets[0]
    elif campaign_id:
        possible_targets = Monster.objects.filter(campaign_id=campaign_id, name__icontains=monster_name)
        if possible_targets.count() == 0:
            return None
        else:
            return possible_targets.first()
    else:
        possible_targets = Monster.objects.filter(name__icontains=monster_name)
        if possible_targets.count() == 0:
            return None
        return possible_targets.first()

    

'''
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
'''

def target_selection_by_id(monster_id):
    monster = Monster.objects.filter(id=monster_id)
    if monster.count() == 0:
        return None
    return monster.first()


# ------------------------------------------------ ACT --------------------------------------------------


def action_image_generation(prompt:str, action:str, player:Character, target:Monster = None):

    # deprecated
    if action in ['move','go']:
        image_description = f"{player.name}, {player.character_race} {player.character_class} {player.physical_description} running to the {prompt[4:]}"

    elif action == 'attack':
        image_description = f"{player.name}, the {player.character_race} {player.character_class} {player.physical_description} using a {player.weapon.weapon_type} ({player.weapon.name}), fighting with a {target.monster_race} {target.monster_class} {target.physical_description} who's using a {target.weapon.weapon_type} ({target.weapon.name})"
        #image_description = f"{player.character_race} {player.character_class} {player.physical_description} fighting a {target.monster_race} {target.monster_class} {target.physical_description} with a {player.weapon.weapon_type}"

    elif action == 'equip':
        weapon_name = 'weapon' if prompt[6:] == "" else prompt[6:]
        image_description = f"{player.character_race} {player.character_class} {player.physical_description} taking a {weapon_name} from the ground"
        # holding up a {weapon_name}

    elif action == 'chest':
        image_description = f"{player.name}, the {player.character_race} {player.character_class} {player.physical_description} is opening a chest with amazement, surprised face"

    elif action == 'portal':
        image_description = f"{player.name}, the {player.character_race} {player.character_class} {player.physical_description} with a surprised face, is discovering a PORTAL with amazement"
    
    elif action == 'see':
        image_description = f"{player.name}, the {player.character_race} {player.character_class} {player.physical_description} is seeing his {prompt[4:]}"

    # take, use, levelup, info
    else:
        if action == 'info':
            #prompt = 'asking himself about'+prompt[5:]
            prompt = 'thinking, reflecting, pondering...'

        if action == 'levelup':
            prompt = 'shining, glowing, leveling up...'

        #image_description = f"{player.character_race} {player.character_class} {player.physical_description} is {prompt}"
        image_description = f"{player.name}, {player.character_race} {player.character_class} holding a {player.weapon.weapon_type}, {player.physical_description} is {prompt}"

    # try to generate an image with DallE, if it fails, it will use StabDiff
    # REASONS TO FAIL:
    #   - it can fail if the prompt is too long or if the model doesn't understand the prompt
    #   - maybe the prompt was too violent or sexual
    #   - maybe the tokens got empty
    # So, if it fails, it will use StabDiff, which is free
    try:
        image_dir_DallE = image_generator_DallE(image_description)
        History.objects.create(campaign=player.campaign, author='SYSTEM', is_image = True, text = image_dir_DallE).save()
    except:
        image_dir_StabDiff = image_generator_StabDiff(image_description)
        History.objects.create(campaign=player.campaign, author='SYSTEM', is_image = True, text = image_dir_StabDiff).save()


def command_executer(prompt:str|list, player:Character, target:Monster) -> tuple[bool, dict]:
    '''
    Returns
    - successful : bool
    - details : dict

    details keys:
    - 'player_died' : bool
    - 'new_player'  : Character
    - 'target_died' : bool
    - 'new_target'  : Monster
    
    '''

    # print(prompt)

    # if the prompt is a string, it will be split into a list
    action = prompt.split(' ') if type(prompt) == str else prompt

    if action[0] not in ['move', 'go', 'attack', 'take', 'talk', 'help']:
        action_image_generation(prompt, action[0], player, target)

    # for each action, the turns on the campaign will be increased
    player.campaign.turn_counter()

    # change players
    successful, player_died, target_died, new_player, new_target = False, False, False, player, target

    if len(prompt) == 0 or prompt == '' or prompt == '\n':
        History.objects.create(campaign=player.campaign, author=player.name, color="blue", text="...").save()
        History.objects.create(campaign=player.campaign, author='SYSTEM', text="The player stood still").save()
        successful = False

    elif action[0] == 'move' or action[0] == 'go':
        successful, new_target = act_move(player, target, action)

    elif action[0] == 'attack':
        successful, player_died, target_died, new_player, new_target = act_attack(player, target, action)

    elif action[0] == 'take':
        successful = act_take(player, action)

    # specifically for weapons on the ground. Take also works but it's more general
    elif action[0] == 'equip':
        successful = act_equip(player, action)

    elif action[0] == 'use':
        successful = act_use(player, action)

    elif action[0] == 'levelup':
        successful = act_levelup(player, action)

    elif action[0] == 'info':
        successful = act_info(player, action)

    elif action[0] == 'see':
        successful = act_see(player, action)

    elif action[0] == 'talk':
        successful = act_talk(player, target, action)

    elif action[0] == 'help':
        from DnD_AI.functions_AI import TUTORIAL
        History.objects.create(campaign=player.campaign, author='SYSTEM', text=TUTORIAL).save()
        successful = True

        
    return successful, {
        'player_died': player_died,
        'new_player': new_player,
        'target_died': target_died,
        'new_target': new_target, 
    }


def act_talk(player:Character, target:Monster, action:list):
    if target is None:
        alone_responses = [
            "You can't talk alone.",
            "You like talking alone, don't you?",
            "You don't seem like someone with many friends..."
        ]
        response = choice(alone_responses)
        History.objects.create(campaign=player.campaign, author='SYSTEM', text=response).save()
        return False

    if len(action) > 1:
        try:
            target_id = action[1]
            if target_id.isdigit():
                target_id = int(target_id)
                target = target_selection_by_id(target_id)
            else:
                target = target_selection_by_name(target_id, player=player)
                if target is None:
                    possible_targets = player.get_monsters_in_range()
                    if len(possible_targets) == 0:
                        History.objects.create(campaign=player.campaign, author='SYSTEM', text=f"There's no monster called {target_id} in your range.").save()
                    else:
                        target = possible_targets[0]
                        History.objects.create(campaign=player.campaign, author='SYSTEM', text=f"There's no monster called {target_id} in your range, talking to {target.name} instead.").save()
        except:
            pass
     
    was_understansable = False
    if target.monster_race == player.character_race or target.monster_class == player.character_class or target.monster_race == "Human" or target.is_boss or "traductor" in player.get_inventory().keys():
        from DnD_AI.default import understandable_responses
        was_understansable = True
        response = choice(understandable_responses)
    else:    
        number = randint(2, 20)
        not_understandable_responses = [
            'ra '*number,
            'k'*number,
            'kak '*number,
            'la lla'*number,
            'ajskd'*number,
            'sdfd'*number,
            'a'*number,
            'A'*number,
            'A'*number+'GGHH',
            'AaAaaA'*number,
            'aAAA'*number,
            '?'*number,
            'ñ',
            'ñ'*number,
            '¿?',
            '¿?'*number,
            '55'*number,
            'mdr '*number,
            'ha3'*number,
            'UwU '*number,
            'OwO '*number,
            'Nyan-'*number,
            'Nyan '*number,
            'Nyanyame nyanyaju nyanyado no nyarabi de nyakunyaku inyanyaku nyanyahan nyanya-dai nyannyaku nyarabete nyagannyagame',
            'w'*number, 
            'weqeqwqewqew',
            '哈'*number,
            '呵'*number,
            'ہا'*number,
            '笑う'*number,
            '笑い'*number,
            '草'*number,
            'TmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXAuLi4=',
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://www.youtube.com/watch?v=vVaFS739skE',
            'gebe dich nie auf',
            'никогда тебя не брошу',
            '绝不会放弃你',
            '絕對不會放棄你',
            'あなたを決してあきらめない',
            'नेवर गोना गिव यू अप',
            'mai bao duoc',
            'nigdy się nie poddawaj',
            'tak akan menyerahkanmu',
            'ನಿಮ್ಮನ್ನು ಎಂದಿಗೂ ಬಿಟ್ಟುಕೊಡುವುದಿಲ್ಲ',
            'ඞ'*(number-1),
            'ඞ',
            'nikdy se tě nevzdám',
            'non te deseram',
            'nigdy cię nie opuszczę',
            'Tôi không đời nào bỏ cậu đâu',
            'чамд хэзээ ч бууж өгөхгүй',
            '절대 포기하지 않을 거야 yoy',
            'ніколі не здамся',
            'nunca vou desistir de você',
            'nigdy się nie poddam',
            'երբեք չեմ հանձնվի',
            'לעולם לא אוותר על יואי',
            'ποτέ δεν θα τα παρατήσεις',
            'vil aldri gi deg opp',
            'لن تتخلى أبدا عن يو',
            'mai te tuku iho i a koe',
            "mana hayk'aqpas yoy up",
            'heç vaxt təslim olmayacaq',
            "ʻaʻole loa e hāʻawi iā ʻoe",
            'هرگز تسلیم نخواهم شد',
            '-. . ...- . .-. / --. --- -. -. .- / --. .. ...- . / -.-- --- ..- / ..- .--. .-.-.',
            '-.-- --- ..- / .- .-. . / --. .- -.-- .-.-.',
            '01101110 01100101 01110110 01100101 01110010 00100000 01100111 01101111 01101110 01101110 01100001 00100000 01100111 01101001 01110110 01100101 00100000 01111001 01101111 01110101 00100000 01110101 01110000',
            '01111001 01101111 01110101 00100000 01100001 01110010 01100101 00100000 01100111 01100001 01111001'
            '01110100 01101000 01100101 00100000 01100111 01100001 01101101 01100101',
            'dGhlIGdhbWU=',
            'bmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXA=',
            'bm8gb25lIGNhbiBlc2NhcGUgdGhlIGhlbGwu'
        ]
        response = choice(not_understandable_responses)


    History.objects.create(campaign=player.campaign, author=target.name, color="red", text=response)


    if was_understansable:
        successful_responses = [
            f"{target.name} is not in the mood to talk.",
            f"{target.name} is ignoring you.",
            f"{target.name} is too busy to talk to you.",
            f"{target.name} is not interested in talking to you.",
            f"{target.name} is still a monster.",
            f"{target.name} loves you secretly.",
            f"{target.name} knows that you will kill him.",
            f"{target.name} feels sad.",
            f"{target.name} is busy thinking on ways to win and save his family from you.",
            "That was still not useful.",
            "That was a waste of time, again.",
            "You like wasting your time, don't you?",
            "Go talk with people outside."
        ]
        response = choice(successful_responses)
    else:
        not_successful_responses = [
            f"{target.name} is not a {player.character_race}",
            f"{target.name} can't understand {player.character_race} language.",
            f"{player.name} is not a {target.monster_race}",
            f"{player.name} can't understand {target.monster_race} language.",
            "You can't understand that language.",
            'You have no traductors in your inventory.',
            'Go find a traductor first.',
            'You are not capable to understand that language. (loser...)',
            'You were not capable to understand it. (loser...)',
            "That was a waste of time.",
            "That wasn't useful at all.",
            "You like wasting your time, don't you?",
        ]
        response = choice(not_successful_responses)
    
    History.objects.create(campaign=player.campaign, author='SYSTEM', text=response)
    
    return True


def act_see(player:Character, action:list):
    if len(action) == 1:
        response = player.inventory
    elif action[1] == 'inventory':
        response = player.inventory
    elif action[1] in ['initial', 'story', 'initial_story']:
        response = player.campaign.initial_story
    elif action[1] == 'achievements':
        response = player.campaign.achievements
    elif action[1] == 'objectives':
        response = player.campaign.objectives_remaining
    elif action[1] == 'turns':
        response = player.campaign.turns
    elif action[1] in ['physical', 'physical_description', 'description']:
        response = player.physical_description
    else:
        response = player.get_inventory(action[1])
    History.objects.create(campaign=player.campaign, author='SYSTEM', text=response).save()
    return True


def act_info(player:Character, action:list):
    if len(action) == 1:
        response = ask_world_info_gemini(campaign_story=player.campaign.initial_story, 
                                         campaign_achievements=player.campaign.achievements)
    else:
        response = ask_world_info_gemini(prompt=action[1],
                              campaign_story=player.campaign.initial_story, 
                              campaign_achievements=player.campaign.achievements)
    History.objects.create(campaign=player.campaign, author='NARRATOR', color='purple', text=response.replace("\n", "<br>")).save()

    try:
        image_dir_DallE = image_generator_DallE(response)
        History.objects.create(campaign=player.campaign, author='SYSTEM', is_image = True, text = image_dir_DallE).save()
    except:
        image_dir_StabDiff = image_generator_StabDiff(response)
        History.objects.create(campaign=player.campaign, author='SYSTEM', is_image = True, text = image_dir_StabDiff).save()

    return True


def act_levelup(player:Character, action:list):
    if player.exp >= player.exp_top:
        if action[1] in ['dmg','damage','rng', 'range', 'wpn', 'weapon']:
            wpn_stat = 'dmg' if action[1] in ['wpn', 'weapon'] else action[1]

            # it means that the player wants to rename his weapon
            if len(action) > 2:
                wpn_name = ' '.join(action[2:])
                successful = player.level_up_weapon(wpn_stat, wpn_name)
            else: # if not, the weapon name remains the same
                successful = player.level_up_weapon(wpn_stat)
            
        else:
            stat = action[1]
            successful = player.level_up_stat(stat)  

        return successful
    else:
        History.objects.create(campaign=player.campaign, author='SYSTEM', text=f"You don't have enough EXP to level up.").save()
        return False


def act_use(player:Character, action:list):
    player_inventory = player.get_inventory()

    if len(action) == 1:
        History.objects.create(campaign=player.campaign, author='SYSTEM', text=f'You need to specify the item you want to use.<br>If you have problems using items, then replace the spaces with "_" i.<br>For example: health_potion.').save()

            # I don't have a list of possible usable items xd, so
            #History.objects.create(campaign=player.campaign, author='SYSTEM', text=f"There's a list of your items: ").save()
        #if 'health potion' not in player_inventory.keys():
        if player_inventory.keys() == ["gold"] or len(player_inventory.keys()) == 0:
            History.objects.create(campaign=player.campaign, author='SYSTEM', text=f"By the way... You don't have usable items.").save()

        return False
    

    item_to_use = (' '.join(action[1:])).lower().replace('_',' ')
    successful = False
    if item_to_use in ['health potion', 'potion', 'hp potion', 'hp']:
        item_to_use = 'health potion'
        successful = player.use_from_inventory(item_to_use, amount = 1)
        player.save()
        if successful:
            player.health = min(player.health + 50, player.max_health)
            player.save()
            History.objects.create(campaign=player.campaign, author='SYSTEM', text=f'{player.name} used a health potion. 50 HP restored!').save()
            return True
        
    elif item_to_use in ['go back bone', 'go back', 'bone', 'back bone']:
        item_to_use = 'go back bone'
        successful = player.use_from_inventory(item_to_use, amount = 1)
        player.save()
        if successful:
            try:
                random_portal = choice(Treasure.objects.filter(campaign=player.campaign, treasure_type='Portal', discovered=True))
                player.x, player.y = random_portal.x, random_portal.y
                player.save()
                History.objects.create(campaign=player.campaign, author='SYSTEM', text=f'{player.name} used a go back bone.').save()
                return True
            except:
                History.objects.create(campaign=player.campaign, author='SYSTEM', text=f"There's no portals.").save()
                return False

    #elif item_to_use == 'mana potion':, or something like that for each item
        # probably is not the best way, it would be better to be implemented on Character.use_from_inventory()
        # please remember me to create a list of possible usable items an their effects on default.py

    else:
        History.objects.create(campaign=player.campaign, author='SYSTEM', text=f"You can't use that.").save()
        return False    
    

    if not successful:
        History.objects.create(campaign=player.campaign, author='SYSTEM', text=f"You have no {item_to_use}s.").save()
        return False
        

    
    
    

def act_equip(player:Character, action:list):
    treasure_to_take = action[1].lower() if len(action) > 1 else 'all'
    possible_treasures = player.get_treasures_in_range(treasure_to_take, is_weapon=True)
    if len(possible_treasures) == 0:
        treasure_to_take = 'weapons' if treasure_to_take == 'all' else treasure_to_take
        History.objects.create(campaign=player.campaign, author='SYSTEM', text=f"There's no {treasure_to_take} to take here.").save()
        successful = False
    else:
        loot = possible_treasures[0].weapon
        History.objects.create(campaign=player.campaign, author='SYSTEM', text=f'{player.name} equipped {loot.name}.').save()
        player.weapon = loot
        player.save()
        possible_treasures[0].delete()
        successful = True
    return successful

def act_take(player:Character, action:list):
    treasure_to_take = action[1].lower() if len(action) > 1 else 'all'
    possible_treasures = player.get_treasures_in_range(treasure_to_take)
    possible_treasures, treasure_to_take = player.get_treasures_in_range(treasure_to_take, is_weapon=True) if len(possible_treasures) == 0 else possible_treasures, 'weapon' if len(possible_treasures) == 0 else treasure_to_take

    if len(possible_treasures) == 0:
        treasure_to_take = 'treasures' if treasure_to_take == 'all' else treasure_to_take
        History.objects.create(campaign=player.campaign, author='SYSTEM', text=f"There's no {treasure_to_take} to take here.").save()
        successful = False

    elif treasure_to_take != 'weapon':
        for treasure in possible_treasures:
            if treasure.treasure_type != 'Weapon':
                loot = treasure.get_inventory()
                if treasure.treasure_type == 'Chest':
                    action_image_generation('', 'chest', player)
                History.objects.create(campaign=player.campaign, author='SYSTEM', text=f'{player.name} got {loot} from {treasure.treasure_type}.').save()
                player.add_all_to_inventory(loot)
                treasure.delete()
        successful = True
    else:
        for treasure in possible_treasures:
            loot = treasure.weapon
            History.objects.create(campaign=player.campaign, author='SYSTEM', text=f'{player.name} equipped {loot.name}.').save()
            player.weapon = loot
            player.save()
            treasure.delete()
        successful = True
    return successful

def act_attack(player:Character, target:Monster, action:list):
    player_died, target_died = False, False
    new_player, new_target = player, None
    try:
        if len(action) > 1:
            target_id = action[1]
            if target_id.isdigit():
                target_id = int(target_id)
                target = target_selection_by_id(target_id)
            else:
                target = target_selection_by_name(target_id, player=player)
                if target is None:
                    possible_targets = player.get_monsters_in_range()
                    if len(possible_targets) == 0:
                        History.objects.create(campaign=player.campaign, author='SYSTEM', text=f"There's no monster called {target_id} in your range.").save()
                    else:
                        target = possible_targets[0]
                        History.objects.create(campaign=player.campaign, author='SYSTEM', text=f"There's no monster called {target_id} in your range, attacking {target.name} instead.").save()
        elif not target:
            History.objects.create(campaign=player.campaign, author='SYSTEM', text=f"There's no monsters in your range.").save()

        result = combat_turn(player=player, monster=target, player_dice=roll_dice(), monster_dice=roll_dice())

        if result['player_died']:
            new_player = player_selection(None)  ###
            player_died = True
        if result['monster_died']:
            #target.delete()     # por si algo, me tiene mamao' que no se borre el monstruo
            target_died = True
            try:
                new_target = player.get_monsters_in_range()[0]
            except:
                new_target = None
        else:
            new_target = target
        successful = True
    except:
        successful = False
    return successful, player_died, target_died, new_player, new_target

def act_move(player:Character, target:Monster, action:list):
    new_target = target

    action[1] = action[1].replace('-','')
    if len(action) > 2:
        action[1] = action[2]+action[1] if action[2] in ['up','down'] else action[1]+action[2]
        
    successful = player.move(action[1])

    for treasure in player.get_treasures_in_range():
        if not treasure.discovered:
            treasure.discover()
            if treasure.treasure_type == 'Portal':
                action_image_generation('', 'portal', player)

    if not successful:
        History.objects.create(campaign=player.campaign, author='SYSTEM', text="You can't be there").save()

    if target is None or target not in player.get_monsters_in_range():
        try:
            new_target = player.get_monsters_in_range()[0]
        except:
            new_target = None

    return successful, new_target


# ------------------------------------------------ MAP --------------------------------------------------


def create_map(player:Character, characters, monsters, treasures, tiles, target:Monster=None, host:str=None, show_map:bool=False) -> tuple:

    zoom_border = max(player.campaign.size_x, player.campaign.size_y)
    player_vision_range = 30

    map = figure(active_scroll='wheel_zoom', 
                 title="", 
                 aspect_scale=1, 
                 sizing_mode='scale_height', 
                 align='center', 
                 min_height=410, 
                 min_width=410,
                 background_fill_alpha=0.05,
                 border_fill_alpha=0,
                 outline_line_color='white',
                 
                 # setting the initial map center and range. The player will be the center with a visual range of 2.5
                 x_range=Range1d(start=(player.x)-2.5, end=(player.x)+3.5, bounds=(-zoom_border, player.campaign.size_x+zoom_border)), 
                 #x_range=Range1d(start=(player.x)-2.5, end=(player.x)+3.5, bounds=(-5, player.campaign.size_x+5)), 
                 y_range=Range1d(start=(player.y)-2.5, end=(player.y)+3.5, bounds=(-zoom_border, player.campaign.size_y+zoom_border)),
                 #y_range=Range1d(start=(player.y)-2.5, end=(player.y)+3.5, bounds=(-5, player.campaign.size_y+5)),
                 )

    #map.rect(x=player.campaign.size_x/2, y=player.campaign.size_y/2, width=player.campaign.size_x, height=player.campaign.size_y, fill_alpha=0, line_width=2, line_color='gray')
        
    # Define las coordenadas x e y para el cuadrado exterior
    x_inner = [0, player.campaign.size_x, player.campaign.size_x, 0]
    y_inner = [0, 0, player.campaign.size_y, player.campaign.size_y]

    # Define las coordenadas x e y para el cuadrado interior
    x_outer = [-zoom_border, player.campaign.size_x+zoom_border, player.campaign.size_x+zoom_border, -zoom_border]
    y_outer = [-zoom_border, -zoom_border, player.campaign.size_y+zoom_border, player.campaign.size_y+zoom_border]
    
    
    xs_dict = [[{'exterior': x_outer, 'holes': [x_inner]}]]
    ys_dict = [[{'exterior': y_outer, 'holes': [y_inner]}]]

    xs = [[[p['exterior'], *p['holes']] for p in mp] for mp in xs_dict]
    ys = [[[p['exterior'], *p['holes']] for p in mp] for mp in ys_dict]

    border_source = ColumnDataSource(dict(xs=xs, ys=ys))

    glyph = MultiPolygons(xs="xs", ys="ys", 
                          hatch_pattern='spiral',
                          hatch_scale=8, 
                          hatch_weight=0.5,
                          hatch_color='black',
                          hatch_alpha=0.5,
                          fill_alpha=0.5,
                          line_alpha=0, 
                          line_color='white')
    map.add_glyph(border_source, glyph)



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
    #map.x_range = Range1d() # -2, +3
    #map.y_range = Range1d() # -2, +3


    filtered_tiles = [tile for tile in tiles if np.sqrt((tile.x - player.x)**2 + (tile.y - player.y)**2) <= player_vision_range]
    # rendering the map tiles
    '''for tile in Tile.objects.all():
        map.image_url(url=[f'media/map/tiles/{DEFAULT_TILE_TYPES[tile.tile_type]}'], x=tile.x, y=tile.y +1, w=1, h=1)'''
    urls = [f'media/map/tiles/{DEFAULT_TILE_TYPES[tile.tile_type]}' for tile in filtered_tiles]
    xs = [tile.x for tile in filtered_tiles]
    ys = [tile.y + 1 for tile in filtered_tiles ]
    map.image_url(url=urls, x=xs, y=ys, w=1, h=1)

    # player's vision range (50 tiles)
    map.circle(x=player.x + 0.5, y=player.y + 0.5, radius=player_vision_range, fill_alpha=0, line_width=1, line_color='gray')

    # the wepon range of the player will glow red if there are monsters in range, else it will be gray
    range_color,range_alpha = ('red',0.65) if len(player.get_monsters_in_range()) != 0 else ('gray',0.5)

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
    if target is not None:
        obj_color = 'deeppink' if target.is_boss else 'red'
        obj_dash = 'dashed' if target.is_key else 'solid'
        #map.circle(x=objective.x+0.5, y=objective.y+0.5, radius=1, fill_alpha=0, line_color=obj_color, line_dash=obj_dash, line_width=2)
        map.circle(x=target.x+0.5, y=target.y+0.5, radius=0.7, fill_alpha=0, line_color=obj_color, line_dash=obj_dash, line_width=2)

    # player highlight
    #map.circle(x=player.x+0.5, y=player.y+0.5, radius=1, fill_alpha=0, line_color='green', line_width=2)
    
    # adding the entities to the map
    filtered_monsters = [monster for monster in monsters if np.sqrt((monster.x - player.x)**2 + (monster.y - player.y)**2) <= player_vision_range or monster.is_boss]
    
    entities = list(characters) + list(filtered_monsters)
    
    entity_data = {
        'x': [], 'y': [], 'raceclass': [], 'LVL': [], 'HP': [], 'HP_max': [], 'RNG': [],
        'icon_x': [], 'icon_y': [], 'real_x': [], 'real_y': [], 'name': [], 'icon': [],
        'weapon_icon': [], 'weapon_name': [], 'weapon_color': [], 'color': [], 'dash': [], 'type': []
    }

    for entity in entities:
        entity_data['x'].append(entity.x + 0.5)
        entity_data['y'].append(entity.y + 0.5)
        entity_data['HP'].append(entity.health)
        entity_data['HP_max'].append(entity.max_health)
        entity_data['RNG'].append(entity.weapon.range)
        entity_data['icon_x'].append(entity.x + 0.1)
        entity_data['icon_y'].append(entity.y + 0.9)
        entity_data['real_x'].append(entity.x)
        entity_data['real_y'].append(entity.y)
        entity_data['name'].append(entity.name)
        entity_data['icon'].append(entity.icon.url)
        entity_data['weapon_icon'].append(entity.weapon.image.url)
        entity_data['weapon_name'].append(f'{entity.weapon.name}+{entity.weapon.level}' if entity.weapon.level != 0 else entity.weapon.name)
        entity_data['weapon_color'].append('orange' if entity.weapon.damage_type == 'Physical' else 'cyan' if entity.weapon.damage_type == 'Magical' else 'black')

        if isinstance(entity, Character):
            entity_data['raceclass'].append(f'{entity.character_race} {entity.character_class}' if entity.character_race != entity.character_class else entity.character_class)
            entity_data['LVL'].append(f'LVL: {entity.level}')
            entity_data['color'].append('green' if entity.id == player.id else 'blue' if entity.is_playable else 'gold')
            entity_data['dash'].append('solid')
            entity_data['type'].append('character' if entity.id != player.id else 'player')
        elif isinstance(entity, Monster):
            entity_data['raceclass'].append(f'{entity.monster_race} {entity.monster_class}' if entity.monster_race != entity.monster_class else entity.monster_class)
            entity_data['LVL'].append('')
            entity_data['color'].append('deeppink' if entity.is_boss else 'red')
            entity_data['dash'].append('dashed' if entity.is_key else 'solid')
            entity_data['type'].append('boss' if entity.is_boss else 'monster')

    # key bosses decorations
    try:
        bosses_data = [(monster.x + 0.5, monster.y + 0.5) for monster in monsters if monster.is_key and monster.is_boss]
        bosses_x, bosses_y = zip(*bosses_data)
        #map.circle(x=bosses_x, y=bosses_y, radius=0.6, fill_color='deeppink', fill_alpha=0.3, line_width=2, line_color='deeppink')
        map.circle(x=bosses_x, y=bosses_y, radius=0.8, fill_alpha=0, line_width=2, line_color='deeppink')
        map.rect(x=bosses_x, y=bosses_y, width=1.13, height=1.13, angle=7.07, fill_alpha=0, line_width=2, line_color='deeppink')
        map.rect(x=bosses_x, y=bosses_y, width=1.13, height=1.13, fill_alpha=0, line_width=2, line_color='deeppink')
    except:
        pass

    # everyone else's decorations
    map.rect(x='x', y='y', width=0.8, height=0.8, fill_color='color', fill_alpha=0.3, line_alpha=0, source=entity_data) 
    map.image_url(url='icon', x='icon_x', y='icon_y', h=0.8, w=0.8, name='name', source=entity_data)
    map.image_url(url='weapon_icon', x='x', y='y', h=0.4, w=0.4, name='weapon_name', source=entity_data)
    entities = map.rect(x='x', y='y', width=0.8, height=0.8, line_color='color', line_dash='dash', fill_alpha=0, line_width=2, name='name', source=entity_data)
    entities.tags = ['entity']

    filtered_treasures = [treasure for treasure in treasures if treasure.treasure_type == 'Chest' or treasure.treasure_type =='Weapon' or treasure.treasure_type == 'Portal' or np.sqrt((treasure.x - player.x)**2 + (treasure.y - player.y)**2) <= player_vision_range]

    treasure_data = {
        'x' : [treasure.x + 0.5 for treasure in filtered_treasures],
        'y' : [treasure.y + 0.5 for treasure in filtered_treasures],
        'icon_x' : [treasure.x +0.1 for treasure in filtered_treasures],
        'icon_y' : [treasure.y +0.9 for treasure in filtered_treasures],
        'real_x' : [treasure.x for treasure in filtered_treasures],
        'real_y' : [treasure.y for treasure in filtered_treasures],
        'color' : [('gold' if treasure.treasure_type == 'Gold' else 'dimgray' if treasure.discovered else '#212121') if treasure.treasure_type != 'Weapon' or not treasure.discovered else 'orange' if treasure.weapon.damage_type == 'Physical' else 'cyan' if treasure.weapon.damage_type == 'Magical' else 'black' for treasure in filtered_treasures],
        'inv': ['' if treasure.treasure_type == "Portal" else (treasure.inventory[1:-1] if treasure.discovered  else '???') if treasure.treasure_type!='Weapon' else  (f'DMG: {treasure.weapon.damage}, RNG: {treasure.weapon.range}' if treasure.discovered else '') for treasure in filtered_treasures],
        'icon' : [treasure.icon.url for treasure in filtered_treasures],
        'name': [('Discovered '+treasure.treasure_type if treasure.discovered else treasure.treasure_type if treasure.treasure_type != 'Weapon' else 'Undiscovered Weapon') if treasure.treasure_type!='Weapon' or not treasure.discovered else treasure.weapon.name for treasure in filtered_treasures],
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

    map.grid.grid_line_color = "grey"
    
    map.xaxis.ticker = AdaptiveTicker(min_interval=1,  mantissas=[1, 2, 5], base=10)
    map.yaxis.ticker = AdaptiveTicker(min_interval=1,  mantissas=[1, 2, 5], base=10)
    
    map_script, map_div = components(map)
    return map_script, map_div


def place_player_on_spawn(player:Character):
    tries = 50
    campaign_id = player.campaign.id
    spawn_tiles = Tile.objects.filter(campaign_id=campaign_id, tile_type='spawn')

    try:
        while tries > 0:
            chosen_tile = choice(spawn_tiles)

            x = chosen_tile.x
            y = chosen_tile.y

            existent_player = Character.objects.filter(campaign_id=campaign_id, x=x, y=y)
            existent_treasure = Treasure.objects.filter(campaign_id=campaign_id, x=x, y=y)
            existent_monster = Monster.objects.filter(campaign_id=campaign_id, x=x, y=y)
            
            if not existent_player and not existent_treasure and not existent_monster:
                player.x = x
                player.y = y
                player.save()
                return True
            else:
                tries -= 1
    except:
        History.objects.create(campaign=player.campaign, author='SYSTEM', text=f"Couldn't place {player.name} on the map. Maybe there's no map...").save()
        return False
        
    # if that didn't work...

    for tile in spawn_tiles:
        x = tile.x
        y = tile.y

        existent_player = Character.objects.filter(campaign_id=campaign_id, x=x, y=y)
        existent_treasure = Treasure.objects.filter(campaign_id=campaign_id, x=x, y=y)
        
        if not existent_player and not existent_treasure:
            player.x = x
            player.y = y
            player.save()
            return True

    return False


# ---------------------------------------------- RESOURCES ------------------------------------------------


'''
MAP PAST TRIES  (DON'T DELETE, PLEASE)

    #tile_color = 'green' if tile.tile_type == 'grass' else 'brown' if tile.tile_type == 'dirt' else 'gray' if tile.tile_type == 'path' else 'black' if tile.tile_type == 'dungeon' else 'red' if tile.tile_type == 'boss' else 'purple' if tile.tile_type == 'god' else 'orange' if tile.tile_type == 'psycho' else 'black'


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

'''

'''
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
'''

'''# Define las coordenadas x e y para el cuadrado exterior
    x_outer = [[0, player.campaign.size_x, player.campaign.size_x, 0]]
    y_outer = [[0, 0, player.campaign.size_y, player.campaign.size_y]]

    # Define las coordenadas x e y para el cuadrado interior
    x_inner = [[player.campaign.size_x/4, 3*player.campaign.size_x/4, 3*player.campaign.size_x/4, player.campaign.size_x/4]]
    y_inner = [[player.campaign.size_y/4, player.campaign.size_y/4, 3*player.campaign.size_y/4, 3*player.campaign.size_y/4]]

    # Dibuja el cuadrado exterior con un hueco en el medio
    map.multi_polygons(xs=[x_outer, x_inner], ys=[y_outer, y_inner],
                    fill_color=['blue', 'white'],
                    hatch_pattern=['diagonal_cross', None],
                    hatch_scale=8, 
                    hatch_weight=0.5,
                    hatch_color='gray',
                    hatch_alpha=0.5,
                    line_alpha=0, 
                    line_color='white')
'''

'''

    # Define una función para mover las marcas de graduación a la mitad de las celdas de la cuadrícula
    formatter = FuncTickFormatter(code="""
        return (tick + 0.5).toFixed(1);
    """)
    #return Math.round(tick + 0.5)
    
    minor_ticks = [i + 0.5 for i in range(0, 10)]  # Ajusta el rango según el tamaño de tu cuadrícula

    # Ajusta los major ticks en los ejes x e y
    map.xaxis.ticker = SingleIntervalTicker(interval=1, num_minor_ticks=0)
    map.yaxis.ticker = SingleIntervalTicker(interval=1, num_minor_ticks=0)

        # Ajusta los minor ticks en los ejes x e y
    map.xaxis.minor_ticks = FixedTicker(ticks=minor_ticks)
    map.yaxis.minor_ticks = FixedTicker(ticks=minor_ticks)

    # Oculta los major ticks
    map.xaxis.major_label_overrides = {i: '' for i in range(0, 10)}  # Ajusta el rango según el tamaño de tu cuadrícula
    map.yaxis.major_label_overrides = {i: '' for i in range(0, 10)}  # Ajusta el rango según el tamaño de tu cuadrícula

    map.xaxis.formatter = formatter
    map.yaxis.formatter = formatter
    
    # Define una función para mover las marcas de graduación a la mitad de las celdas de la cuadrícula
    formatter = FuncTickFormatter(code="""
        return (tick + 0.5).toFixed(0);
    """)

    # Ajusta los major ticks en los ejes x e y
    map.xaxis.ticker = SingleIntervalTicker(interval=1, num_minor_ticks=1)
    map.yaxis.ticker = SingleIntervalTicker(interval=1, num_minor_ticks=1)

    # Ajusta los minor ticks en los ejes x e y
    map.xaxis.formatter = formatter
    map.yaxis.formatter = formatter

    # Oculta los major ticks
    map.xaxis.major_label_overrides = {i: '' for i in range(0, 10)}  # Ajusta el rango según el tamaño de tu cuadrícula
    map.yaxis.major_label_overrides = {i: '' for i in range(0, 10)}  # Ajusta el rango según el tamaño de tu cuadrícula
    
'''


'''
MAP LABELS

unexpected attribute 'theme' to figure, possible attributes are above, active_drag, active_inspect, active_multi, active_scroll, active_tap, align, aspect_ratio, aspect_scale, attribution, background_fill_alpha, background_fill_color, below, border_fill_alpha, border_fill_color, center, context_menu, css_classes, css_variables, disabled, elements, extra_x_ranges, extra_x_scales, extra_y_ranges, extra_y_scales, flow_mode, frame_align, frame_height, frame_width, height, height_policy, hidpi, hold_render, inner_height, inner_width, js_event_callbacks, js_property_callbacks, left, lod_factor, lod_interval, lod_threshold, lod_timeout, margin, match_aspect, max_height, max_width, min_border, min_border_bottom, min_border_left, min_border_right, min_border_top, min_height, min_width, name, outer_height, outer_width, outline_line_alpha, outline_line_cap, outline_line_color, outline_line_dash, outline_line_dash_offset, outline_line_join, outline_line_width, output_backend, renderers, reset_policy, resizable, right, sizing_mode, styles, stylesheets, subscribed_events, syncable, tags, title, title_location, toolbar, toolbar_inner, toolbar_location, toolbar_sticky, tools, tooltips, visible, width, width_policy, x_axis_label, x_axis_location, x_axis_type, x_minor_ticks, x_range, x_scale, y_axis_label, y_axis_location, y_axis_type, y_minor_ticks, y_range or y_scale

'''