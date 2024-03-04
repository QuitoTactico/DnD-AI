from django.shortcuts import render
from random import randint
#from django.http import HttpRestponse

from .models import *

# Create your views here.

def home(request):
    # WEB LABELS
    # player_name=str   
    # roll_dice=bool    (optional)


    # GETTING DATA FROM THE DATABASE
    player_name = request.GET.get('player')
    monsters = Monster.objects.all()
    characters = Character.objects.all()
    weapons = Weapon.objects.all()


    # PLAYER SELECTION
    # If through the player label they send the name of a playable character, it selects it as the player's character 
    if player_name:
        try:
            player = Character.objects.get(name__iexact=player_name)
        except:
            try:
                # If the name of the character is not found, it tries to find a character whose name contains the string entered
                player = Character.objects.filter(name__icontains=player_name).first() 
            except:
                # If there is no character containing the name entered, it selects the first playable character in the database
                player = Character.objects.filter(is_playable=True).first()
    else:
        # If the player label is not sent, it selects the first playable character in the database
        # We can change this to let the player select the character by himself, but we'll see.
        player = Character.objects.filter(is_playable=True).first()


    # DICE_ROLL
    dice_needed = request.GET.get('roll_dice')
    if dice_needed:     # If the roll_dice label is sent, it rolls the dice
        dice_value = roll_dice()
    else:               # If the roll_dice label is not sent, it sets the dice value to None, this way isn't rendered
        dice_value = None 


    return render(request, 'home.html', {'player':player, 'monsters':monsters, 'characters':characters, 'weapons':weapons, 'dice_value': dice_value, 'dice_needed': dice_needed} )


# I put it here if it's needed to be used in another view or code section
def roll_dice(): 
    return randint(1, 20)