from django.shortcuts import render

from .models import *
from .functions import *
from .functions_AI import *

    
def home(request):
    
    if request.method == "POST":
        '''
        POST LABELS:
        - test
        - player_name
        - target_id
        - dice_needed
        - prompt
        '''

        # ------------------------- GETTING POST LABELS -----------------------------

        # Optional test page selection
        page = 'home.html' if 'test' not in request.POST else 'test.html'

        # If the roll_dice label is sent, it rolls the dice
        # If the roll_dice label is not sent, it sets the dice value to None, this way isn't rendered
        dice_needed = 'dice_needed' in request.POST
        dice_value = roll_dice() if dice_needed else None

        # Adding the action prompt and response to the History model, so it's rendered on the game console
        if 'prompt' in request.POST:
            prompt = request.POST.get('prompt')
            response = get_response(prompt)
            History.objects.create(author=request.POST['player_name'], text=request.POST['prompt'], color='blue').save()
            History.objects.create(author='SYSTEM', text=response).save()
            
        
        # --------------------- GETTING DATA FROM THE DATABASE -----------------------
            
        
        # Getting all the models
        characters  = Character.objects.all()
        players     = Character.objects.filter(is_playable=True)
        monsters    = Monster.objects.all()
        weapons     = Weapon.objects.all()
        treasures   = Treasure.objects.all()
        history     = History.objects.all()
            
        # If the name of a character is sent, that character will be the actual player
        player_name = None if 'player_name' not in request.POST else request.POST['player_name']
        player = player_selection(player_name)

        # If the id or name of a monster is sent, that monster will be the actual target
        target_id = None if 'target_id' not in request.POST else request.POST['target_id']
        if target_id is not None and target_id.isdigit():
            target_id = int(target_id)
            target = target_selection_by_id(target_id)
        else:
            target = target_selection_by_name(target_id)


        # -------------------------------------- MAP -----------------------------------------
        host = request.get_host()
        map_script, map_div = create_map(player, characters, monsters, treasures, target, host)


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
                            'weapons'       : weapons, 
                            'text_history'  : history,

                                # Combat
                            'dice_value'    : dice_value, 
                            'player'        : player, 
                            'monster'       : target,

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
                        })
    else:

        # If there's no POST, then it selects the first character and monster in the database as player and target
        player = player_selection(None)
        target = target_selection_by_id(None)
        history = History.objects.all()
        return render(request, 
                      'home.html', 
                      {
                            'player'         : player, 
                            'monster'        : target,
                            'text_history'   : history,
                       })
    
