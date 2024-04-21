from django.shortcuts import render

from .models import *
from .functions import *
from .functions_AI import action_interpreter, get_response


def home(request):
    return render(request, 'home.html')

def campaignSelection(request):
    campaigns = Campaign.objects.all()
    return render(request, 'campaignselection.html', 
                  {'campaigns': campaigns})

def campaignCreation(request):
    return render(request, 'campaigncreation.html')

def playerSelection(request):
    if request.method == "POST":
        campaign_id = request.POST['campaign_id']
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
    return render(request, 'playercreation.html')
    
def game(request):
    
    if request.method == "POST":
        '''
        POST LABELS:
        - campaign_id
        - test
        - player_name
        - target_id
        - dice_needed
        - prompt
        '''

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
        player_name = None if 'player_name' not in request.POST else request.POST['player_name']
        player = player_selection(player_name)

        # If the id or name of a monster is sent, that monster will be the actual target
        target_id = None if 'target_id' not in request.POST else request.POST['target_id']
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
                            'characters'    : characters, 
                            'players'       : players, 
                            'monsters'      : monsters, 
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
        history = History.objects.all()
        campaign_id = Campaign.objects.filter(is_completed=False).first().id
        return render(request, 
                      'game.html', 
                      {
                            'player'         : player, 
                            'monster'        : target,
                            'text_history'   : history,
                            'campaign_id'    : campaign_id,
                       })
    
