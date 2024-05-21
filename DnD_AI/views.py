from django.shortcuts import render
#from django.http import HttpResponse

from .models import *
from .functions import *
from .functions_AI import action_interpreter, create_initial_stories_gemini #, get_response


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def guide(request):
    return render(request, 'guide.html')


def campaignSelection(request):
    '''POST LABELS:
    - create_campaign (optional) (default = None)

    If the create_campaign label is sent, it creates a new campaign with this info sent in the POST request.
    - name
    - initial_story
    '''

    if request.method == "POST":
        if 'create_campaign' in request.POST:
            from .map_creator import generate_dungeon_map
            name = request.POST.get('name')
            initial_story = request.POST.get('initial_story')
            size_x = int(request.POST.get('size_x'))
            size_y = int(request.POST.get('size_y'))
            
            campaign = Campaign.objects.create(name=name, 
                                    initial_story=initial_story,
                                    size_x=size_x,
                                    size_y=size_y)
            campaign.save()

            History.objects.create(campaign_id=campaign.id, author='NARRATOR', color='purple', text=initial_story).save()

            generate_dungeon_map(campaign)
            


    campaigns = Campaign.objects.all().order_by('is_completed', '-turns')

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

        # Check if create_player is in the POST data
        if 'create_player' in request.POST:
            #try:
                name = request.POST.get('name')
                physical_description = request.POST.get('physical_description')

                character_race = request.POST.get('race')
                character_class = request.POST.get('class') or character_race  # we use the race twice, if no class is selected

                weapon_id = int(request.POST.get('weapon_id'))
                weapon = Weapon.objects.get(id=weapon_id)

                # stats
                max_health = int(request.POST.get('max_health', int(request.POST.get('vitality')) * 10))
                strength = int(request.POST.get('str'))
                intelligence = int(request.POST.get('int'))
                dexterity = int(request.POST.get('dex'))
                physical_resistance = int(request.POST.get('phyres'))
                magical_resistance = int(request.POST.get('magres'))

                story = request.POST.get('story') or "Default story."

                '''
                # we need to validate that numerical values do not exceed SQLite limits
                if max_health > 9223372036854775807 or strength > 9223372036854775807 or intelligence > 9223372036854775807 or dexterity > 9223372036854775807 or physical_resistance > 9223372036854775807 or magical_resistance > 9223372036854775807:
                    return HttpResponse("STATISTIC TOO BIG", status=400)
                '''

                # create new player
                new_player = Character.objects.create(
                    is_playable=True,
                    name=name,
                    physical_description=physical_description,
                    weapon=weapon,
                    max_health=max_health,
                    strength=strength,
                    intelligence=intelligence,
                    dexterity=dexterity,
                    physical_resistance=physical_resistance,
                    magical_resistance=magical_resistance,
                    inventory=str({'gold': 20, 'health potion': 5, 'go back bone': 3, 'key': 3}),
                    story=story,
                    character_race=character_race,
                    character_class=character_class,
                    campaign_id=campaign_id,
                    x=0,
                    y=0,
                )

                try:
                    place_player_on_spawn(new_player)
                except:
                    new_player.save()

                gift = request.POST.get('gift')
                loot = {'gold': 50} if gift == 'gold' or gift is None else {gift: 5}
                new_player.add_all_to_inventory(loot)

                image_description = f"{new_player.name}, a {new_player.character_race} {new_player.character_class}, {new_player.physical_description}"
                try:
                    image_dir_DallE = image_generator_DallE(image_description).replace('media/', '')
                    new_player.icon = image_dir_DallE
                    new_player.image = image_dir_DallE
                except:
                    try:
                        image_dir_StabDiff = image_generator_StabDiff(image_description).replace('media/', '')
                        new_player.icon = image_dir_StabDiff
                        new_player.image = image_dir_StabDiff
                    except:
                        pass

                new_player.save()

                History.objects.create(campaign_id=campaign_id, author='SYSTEM', text=f"{new_player.name} has joined the party!").save()
                '''
                return HttpResponse("Player created successfully.")
                
            except OverflowError as e:
                return HttpResponse(f"Overflow error: {e}", status=500)
            except ValueError as e:
                return HttpResponse(f"Value error: {e}", status=400)
            '''

    else:
        campaign_id = Campaign.objects.filter(is_completed=False).first().id

    players = Character.objects.filter(campaign_id=campaign_id, is_playable=True).order_by('-level')

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
    #weapons = Weapon.objects.filter(is_template=True)

    races = DEFAULT_RACES
    classes = [player_class for player_class in DEFAULT_CLASSES if player_class not in DEFAULT_RACES]
    weapon_names = DEFAULT_WEAPON_NAMES
    #weapons_with_stats = DEFAULT_WEAPON_STATS

    weapons = []
    for weapon_name in weapon_names:
        default_weapon = Weapon.objects.filter(is_template=True, name=weapon_name).first()
        if default_weapon:
            weapons.append(default_weapon)


    
    return render(request, 'playercreation.html',
                  {
                        'campaign_id':campaign_id,
                        'races':races,
                        'classes':classes,
                        'weapons':weapons,
                        #'weapons_name':weapon_names,
                        #'weapons_with_stats':weapons_with_stats,
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
                    History.objects.create(campaign_id=campaign_id, author='ACTION', color='gray', text=prompt).save()


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
        exp_bar = min((player.exp / player.exp_top) * 100, 100)


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
                            'exp_bar'           : exp_bar,
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
    
