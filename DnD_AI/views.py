from django.shortcuts import render
#from django.http import HttpRestponse

from .models import *

# Create your views here.

def home(request):
    player_name = request.GET.get('player')
    monsters = Monster.objects.all()
    characters = Character.objects.all()
    weapons = Weapon.objects.all()

    # If through the player label they send the name of a playable character, it selects it as the player's character 
        # If the name of the character is not found, it tries to find a character whose name contains the string entered
        # If there is no character containing the name entered, it selects the first playable character in the database
    # If the player label is not sent, it selects the first playable character in the database
    if player_name:
        try:
            player = Character.objects.get(name__iexact=player_name)
        except:
            try:
                player = Character.objects.filter(name__icontains=player_name).first() 
            except:
                player = Character.objects.filter(is_playable=True).first()
    else:
        player = Character.objects.filter(is_playable=True).first()


    return render(request, 'home.html', {'player':player, 'monsters':monsters, 'characters':characters, 'weapons':weapons})
