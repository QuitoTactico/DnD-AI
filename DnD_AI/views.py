from django.shortcuts import render
#from django.http import HttpRestponse

from .models import *
from .functions import *

from bokeh.plotting import figure, show
from bokeh.models import Range1d
from bokeh.embed import components

from django.conf import settings
import os

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

        host = request.get_host()
        #map = create_map(player, characters, monsters, show_map = True)  # for map testing
        map = create_map(player, characters, monsters, host)
        script, div = components(map)

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
                                      'dice_needed': dice_needed,
                                      'script': script, 'div': div,
                                      #'url_prueba' : os.path.join(settings.BASE_DIR, player.icon.url[1:]).replace('\\', '/')
                                      'host': host,
                                      'url_prueba' : host + player.icon.url
                                      } )
    else:
        # If there's no get/post, then it selects the first playable character in the database
        player = player_selection(None)
        return render(request, 'home.html', {'player':player} )
    
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
    map = figure(active_scroll='wheel_zoom', title="", aspect_scale=1, sizing_mode='scale_width', align='center')
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
        map.image_url(url=[icon_path], x=character_x+0.1, y=character_y+0.9, h=0.8, w=0.8)
        map.image_url(url=[weapon_path], x=character_x+0.5, y=character_y+0.5, h=0.4, w=0.4)
        if character.is_playable:
            map.rect(x=character_x+0.5, y=character_y+0.5, width=0.8, height=0.8, line_color="blue", fill_alpha=0, line_width=2)
        else:
            map.rect(x=character_x+0.5, y=character_y+0.5, width=0.8, height=0.8, line_color="yellow", fill_alpha=0, line_width=2)

    for monster in monsters:
        monster_x, monster_y = monster.x, monster.y
        if host:
            icon_path, weapon_path = monster.icon.url, monster.weapon.image.url
        else:
            icon_path, weapon_path = os.path.join(settings.BASE_DIR, monster.icon.url[1:]).replace('\\', '/'), os.path.join(settings.BASE_DIR, monster.weapon.image.url[1:]).replace('\\', '/')
        map.image_url(url=[icon_path], x=monster_x+0.1, y=monster_y+0.9, h=0.8, w=0.8)
        map.image_url(url=[weapon_path], x=monster_x+0.5, y=monster_y+0.5, h=0.4, w=0.4)
        map.rect(x=monster_x+0.5, y=monster_y+0.5, width=0.8, height=0.8, line_color="red", fill_alpha=0, line_width=2)

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
