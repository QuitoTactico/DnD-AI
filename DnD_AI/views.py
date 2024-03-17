from django.shortcuts import render
#from django.http import HttpRestponse

from .models import *
from .functions import *

# Create your views here.

def home(request):
    # WEB LABELS
    # player_name=str   
    # roll_dice=bool    (optional)
    
    if request.method == "POST":
    #if True:     # i'm testing, sending all the things to the front.

        
        # DICE_ROLL
        #dice_needed = request.GET.get('dice_needed')
        #dice_needed = request.POST['dice_needed']
        dice_needed = 'dice_needed' in request.POST
        
        if dice_needed:   # If the roll_dice label is sent, it rolls the dice
            dice_value = roll_dice()
        else:               # If the roll_dice label is not sent, it sets the dice value to None, this way isn't rendered
            dice_value = None 
            dice_needed = False


        # GETTING DATA FROM THE DATABASE
        # player_name = request.GET.get('player')
        player_name = request.POST['player_name']

        if 'monster_id' in request.POST:
            try:
                monster_id = int(request.POST['monster_id'])
            except:
                monster_id = None
        else:
            monster_id = None

        # If there's any get/post, then gets the data from the database
       
        monsters = Monster.objects.all()
        characters = Character.objects.all()
        weapons = Weapon.objects.all()


        # PLAYER SELECTION
        # If through the player label they send the name of a playable character, it selects it as the player's character 
        player = player_selection(player_name)
        monster = monster_selection_by_id(monster_id)

        players = Character.objects.filter(is_playable=True)

        #test = request.GET.get('test')
        #test = request.POST['test']
        test = 'test' in request.POST
        page = 'test.html' if test else 'home.html'

        return render(request, page, {'player':player, 
                                      'players':players, 
                                      'player_name_sent':player_name, 
                                      'monster': monster, 
                                      'monsters':monsters, 
                                      'monster_id_sent': monster_id,
                                      'characters':characters, 
                                      'weapons':weapons, 
                                      'dice_value': dice_value, 
                                      'dice_needed': dice_needed} )
    else:
        # If there's no get/post, then it selects the first playable character in the database
        player = player_selection(None)
        return render(request, 'home.html', {'player':player} )

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