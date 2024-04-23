from django.shortcuts import render

from .models import *
from .functions import *
from .functions_AI import action_interpreter, create_initial_stories_gemini #, get_response


def home(request):
    return render(request, 'home.html')



def campaignSelection(request):
    '''POST LABELS:
    - create_campaign (optional) (default = None)

    If the create_campaign label is sent, it creates a new campaign with this info sent in the POST request.
    - name
    - initial_story
    '''

    if request.method == "POST":
        if 'create_campaign' in request.POST:
            name = request.POST.get('name')
            initial_story = request.POST.get('initial_story')
            Campaign.objects.create(name=name, initial_story=initial_story).save()

    campaigns = Campaign.objects.all()

    return render(request, 'campaignselection.html', 
                  {
                      'campaigns': campaigns,
                      })



def campaignCreation(request):
    if request.method == "POST":
        initial_stories = create_initial_stories_gemini(request.POST.get('prompt'))
    else:
        initial_stories = create_initial_stories_gemini()

    return render(request, 'campaigncreation.html',
                  {
                      'initial_stories': initial_stories,
                      })



def playerSelection(request):
    '''POST LABELS:
    - campaign_id   (optional) (default = First not completed)
    - create_player (optional) (default = None)
    
    If the create_player label is sent, it creates a new player with this info sent in the POST request.
    - name
    - physical_description
    - weapon_id
    - max_health
    - str
    - int
    - rec
    - dex
    - phyres
    - magres
    - con
    - gift
    - story
    - race
    - class
    - icon
    - image         (optional) (default = icon)
    '''

    if request.method == "POST":

        #campaign_id = request.POST['campaign_id'] if 'campaign_id' in request.POST else Campaign.objects.filter(is_completed=False).first().id  # REDUNDANT!
        # Today I've learnt something better than ternary conditional.
        campaign_id = request.POST.get('campaign_id') or Campaign.objects.filter(is_completed=False).first().id

        # This goes here. After the player selects his character info, the button will redirect the player to this view.
        # So, the button will send the info to this view and not the other one, to create the character.
        if 'create_player' in request.POST:
            name = request.POST.get('name')
            physical_description = request.POST.get('physical_description')

            weapon_id = request.POST.get('weapon_id')
            weapon = Weapon.objects.get(id=weapon_id)

            max_health = request.POST.get('max_health')
            strength = request.POST.get('str')
            intelligence = request.POST.get('int')
            recursiveness = request.POST.get('rec')
            dexterity = request.POST.get('dex')
            physical_resistance = request.POST.get('phyres')
            magical_resistance = request.POST.get('magres')
            constitution = request.POST.get('con')

            gift = request.POST.get('gift')
            inventory = "{}" if gift is None else f"{{{gift}: 5}}"

            story = request.POST.get('story')
            
            character_race = request.POST.get('race')
            character_class = request.POST.get('class')
            
            icon = request.POST.get('icon')
            image = request.POST.get('image') or icon
            
            Character.objects.create(
                is_playable=True,
                name=name,
                physical_description=physical_description,
                weapon=weapon,
                max_health=max_health,
                strength=strength,
                intelligence=intelligence,
                recursiveness=recursiveness,
                dexterity=dexterity,
                physical_resistance=physical_resistance,
                magical_resistance=magical_resistance,
                constitution=constitution,
                inventory=inventory,
                story=story,
                character_race=character_race,
                character_class=character_class,
                icon=icon,
                image=image,
                campaign_id=campaign_id,
            ).save()
    else:
        campaign_id = Campaign.objects.filter(is_completed=False).first().id
    

    players = Character.objects.filter(campaign_id=campaign_id, is_playable=True)

    return render(request, 
                  'playerselection.html', 
                  {
                      'players': players, 
                      'campaign_id': campaign_id
                      })



def playerCreation(request):
    '''POST LABELS:
    - campaign_id   (optional) (default = First not completed)
    '''

    campaign_id = request.POST.get('campaign_id') or Campaign.objects.filter(is_completed=False).first().id

    races = DEFAULT_RACES
    classes = DEFAULT_CLASSES
    weapons = DEFAULT_WEAPONS
    weapons_with_stats = DEFAULT_WEAPON_STATS
    
    return render(request, 'playercreation.html',
                  {
                        'campaign_id':campaign_id,
                        'races':races,
                        'classes':classes,
                        'weapons':weapons,
                        'weapons_with_stats':weapons_with_stats,
                        })
    


def game(request):
    '''POST LABELS:
    - campaign_id   (optional) (default = First not completed)
    - test          (optional) (default = False)
    - player_name   (optional) (default = First character in that campaign)
    - target_id     (optional) (default = None)
    - dice_needed   (optional) (default = False) (DEPRECATED, DELETE LATER)
    - prompt        (optional) (default = None)
    '''
    
    if request.method == "POST":
        

        # ------------------------- GETTING POST LABELS -----------------------------

        # Optional test page selection
        page = 'game.html' if 'test' not in request.POST else 'test.html'

        if 'campaign_id' in request.POST:
            campaign_id = request.POST['campaign_id']
        else: 
            campaign_id = Campaign.objects.filter(is_completed=False).first().id

        # If the roll_dice label is sent, it rolls the dice
        # If the roll_dice label is not sent, it sets the dice value to None, this way isn't rendered
        dice_needed = 'dice_needed' in request.POST
        dice_value = roll_dice() if dice_needed else None

        # Adding the action prompt and response to the History model, so it's rendered on the game console
        command = False
        if 'prompt' in request.POST:
            prompt = request.POST['prompt']
            
            # If the prompt is empty, it's considered a command (a null command)
            if len(prompt) == 0 or prompt == '' or prompt is None or prompt == '\n':
                prompt = ''
                command = True

            # If the prompt is not empty, it's considered a message that needs to be sent to the AI to become a command
            else:
                History.objects.create(campaign_id=campaign_id, author=request.POST['player_name'], text=prompt, color='blue').save()

                # If the prompt starts with a slash, it's considered a command
                if prompt[0] == '/':
                    prompt = prompt[1:]
                    command = True
                else:
                    #response = get_response(prompt)
                    #History.objects.create(campaign_id=campaign_id, author='SYSTEM', text=response).save()

                    prompt = action_interpreter(prompt)
                    command = True
                    History.objects.create(campaign_id=campaign_id, author='ACTION', text=prompt).save()


        # ------------------------- GETTING PLAYER AND TARGET -----------------------------
                
        # ALL OF THIS IS BETA. IT WILL BE CHANGED IN THE FUTURE FOR [(p_id 1, t_id 1), (p_id 2, t_id 2), ...]

        # If the name of a character is sent, that character will be the actual player
        if 'player_name' in request.POST:
            player_name = request.POST.get('player_name')
            player = player_selection(player_name)
        elif 'player_id' in request.POST:
            player_id = request.POST.get('player_id')
            player = player_selection_by_id(player_id)
        else:
            player = player_selection(None)

        player_name = player.name
        player_id = player.id

        # If the id or name of a monster is sent, that monster will be the actual target
        target_id = None if 'target_id' not in request.POST else request.POST.get('target_id')
        if target_id is not None and target_id != '':
            if target_id.isdigit():
                target_id = int(target_id)
                target = target_selection_by_id(target_id)
            else:
                target = target_selection_by_name(target_id)
        else:
            possible_targets = player.get_monsters_in_range()
            target = None if len(possible_targets) == 0 else possible_targets[0]
        


        # --------------------------------- ACTING ----------------------------------


        if command:
            successful, command_details = command_executer(prompt, player, target)
            if command_details['player_died']:
                player = command_details['new_player']
            target = command_details['new_target']
            target_id = target.id if target is not None else None

        
        # --------------------- GETTING DATA FROM THE DATABASE -----------------------
            
        
        # Getting all the models
        '''
        characters  = Character.objects.all()
        players     = Character.objects.filter(is_playable=True)
        monsters    = Monster.objects.all()
        weapons     = Weapon.objects.all()
        treasures   = Treasure.objects.all()
        history     = History.objects.all()
        tiles       = Tile.objects.all()
        '''

        characters  = Character.objects.filter(campaign_id=campaign_id)
        players     = Character.objects.filter(campaign_id=campaign_id, is_playable=True)
        monsters    = Monster.objects.filter(campaign_id=campaign_id)
        #weapons     = Weapon.objects.filter(campaign_id=campaign_id)
        treasures   = Treasure.objects.filter(campaign_id=campaign_id)
        history     = History.objects.filter(campaign_id=campaign_id)
        tiles       = Tile.objects.filter(campaign_id=campaign_id)
        

        # -------------------------------------- MAP -----------------------------------------

        host = request.get_host()
        map_script, map_div = create_map(player, characters, monsters, treasures, tiles, target, host)

        # --------------------------------- RENDER DETAILS -----------------------------------


        # A detail for the weapon, this will be placed in another file later.
        weapon_lvl = player.weapon.level
        weapon_lvl_label = '+'+str(weapon_lvl) if weapon_lvl > 0 else ''


        # ------------------------------------ RENDERING -------------------------------------


        return render(request, 
                      page, 
                      {
                                # Database
                            #'characters'    : characters, 
                            'players'       : players, 
                            #'monsters'      : monsters, 
                            #'weapons'       : weapons, 
                            'text_history'  : history,

                                # Combat
                            'dice_value'    : dice_value, 
                            'player'        : player, 
                            'target'       : target,

                                # Map
                            'map_script'    : map_script, 
                            'map_div'       : map_div,

                                # Testing details
                            'player_name_sent'  : player_name,
                            'player_id_sent'    : player_id,
                            'target_id_sent'    : target_id,
                            'dice_needed'       : dice_needed,
                            'host'              : host,
                            'url_prueba'        : host + player.icon.url,
                            'weapon_lvl_label'  : weapon_lvl_label,
                            'campaign_id'       : campaign_id,
                            })
    else:

        # If there's no POST, then it selects the first character and monster in the database as player and target
        
        player = player_selection(None)
        target = target_selection_by_id(None)
        campaign_id = Campaign.objects.filter(is_completed=False).first().id

        characters  = Character.objects.filter(campaign_id=campaign_id)
        players     = Character.objects.filter(campaign_id=campaign_id, is_playable=True)
        monsters    = Monster.objects.filter(campaign_id=campaign_id)
        treasures   = Treasure.objects.filter(campaign_id=campaign_id)
        history     = History.objects.filter(campaign_id=campaign_id)
        tiles       = Tile.objects.filter(campaign_id=campaign_id)

        
        host = request.get_host()
        map_script, map_div = create_map(player, characters, monsters, treasures, tiles, target, host)

        return render(request, 
                      'game.html', 
                      {
                            'player'         : player, 
                            'monster'        : target,
                            'text_history'   : history,
                            'campaign_id'    : campaign_id,
                            'map_script'     : map_script,
                            'map_div'        : map_div,
                       })
    
