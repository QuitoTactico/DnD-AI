import numpy as np
#import matplotlib.pyplot as plt
import random
from .models import *

class Habitacion:
    def __init__(self, x, y, w, h, room_type):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.room_type = room_type
        self.treasure = False
        self.boss = False
        self.spawn = False
        self.portal = False

def crear_habitacion(mapa, min_size, max_size, room_type):
    h = random.randint(min_size, max_size)
    w = random.randint(min_size, max_size)
    x = random.randint(1, mapa.shape[1] - w - 1)
    y = random.randint(1, mapa.shape[0] - h - 1)

    # Asegurar que la habitación no se superponga con otras
    if np.any(mapa[y:y+h, x:x+w] != ''):
        return None

    return Habitacion(x, y, w, h, room_type)

def designar_habitaciones_especiales(rooms):
    # Seleccionar habitación para spawn de jugadores
    habitacion_spawn = random.choice(rooms)
    habitacion_spawn.spawn = True
    
    # Seleccionar tres rooms para jefes
    habitaciones_boss = 0
    while habitaciones_boss < 3:
        h = random.choice(rooms)
        if not h.spawn:
            h.boss = True
            habitaciones_boss += 1
    
    # Seleccionar rooms para tesoros
    for h in rooms:
        if random.random() < 0.20:  # 20% de probabilidad de tener tesoro (cofre)
            h.treasure = True

    # Seleccionar rooms para portales
    habitaciones_portal = 0
    while habitaciones_portal < int(len(rooms)*0.015): # el 2% de las rooms tienen portal
        h = random.choice(rooms)
        if not h.spawn and not h.boss:
            h.portal = True
            habitaciones_portal += 1



def distance(h1, h2):
    # Calcular la distancia entre el centro de dos rooms
    centro_h1 = (h1.x + h1.w // 2, h1.y + h1.h // 2)
    centro_h2 = (h2.x + h2.w // 2, h2.y + h2.h // 2)
    return np.sqrt((centro_h1[0] - centro_h2[0]) ** 2 + (centro_h1[1] - centro_h2[1]) ** 2)

def connect_rooms(mapa, habitacion1, habitacion2, hallway_type, campaign_id):
    puntos1 = (random.randint(habitacion1.x, habitacion1.x + habitacion1.w - 1),
               random.randint(habitacion1.y, habitacion1.y + habitacion1.h - 1))
    puntos2 = (random.randint(habitacion2.x, habitacion2.x + habitacion2.w - 1),
               random.randint(habitacion2.y, habitacion2.y + habitacion2.h - 1))

    # Crear un pasillo horizontal o vertical
    ancho_pasillo = random.randint(1, 2)
    if random.random() < 0.5:  # horizontal primero, luego vertical
        for x in range(min(puntos1[0], puntos2[0]), max(puntos1[0], puntos2[0]) + 1):
            for offset in range(ancho_pasillo):
                y = puntos1[1] + offset
                if 0 <= y < mapa.shape[0]:
                    #mapa[puntos1[1] + offset, x] = tipo_pasillo
                    Tile.objects.update_or_create(campaign_id=campaign_id, x=x, y=y, defaults={'tile_type': hallway_type})
                    if random.random() < 0.05:
                        generate_object_in_coords(campaign_id, x, y, hallway_type, habitacion1)

        for y in range(min(puntos1[1], puntos2[1]), max(puntos1[1], puntos2[1]) + 1):
            for offset in range(ancho_pasillo):
                x = puntos2[0] + offset
                if 0 <= x < mapa.shape[1]:
                    #mapa[y, puntos2[0] + offset] = tipo_pasillo
                    Tile.objects.update_or_create(campaign_id=campaign_id, x=x, y=y, defaults={'tile_type': hallway_type})
                    if random.random() < 0.05:
                        generate_object_in_coords(campaign_id, x, y, hallway_type, habitacion1)


    else:  # vertical primero, luego horizontal
        for y in range(min(puntos1[1], puntos2[1]), max(puntos1[1], puntos2[1]) + 1):
            for offset in range(ancho_pasillo):
                x = puntos1[0] + offset
                if 0 <= x < mapa.shape[1]:
                    #mapa[y, puntos1[0] + offset] = tipo_pasillo
                    Tile.objects.update_or_create(campaign_id=campaign_id, x=x, y=y, defaults={'tile_type': hallway_type})
                    if random.random() < 0.05:
                        generate_object_in_coords(campaign_id, x, y, hallway_type, habitacion1)

        for x in range(min(puntos1[0], puntos2[0]), max(puntos1[0], puntos2[0]) + 1):
            for offset in range(ancho_pasillo):
                y = puntos2[1] + offset
                if 0 <= y < mapa.shape[0]:
                    #mapa[puntos2[1] + offset, x] = tipo_pasillo
                    Tile.objects.update_or_create(campaign_id=campaign_id, x=x, y=y, defaults={'tile_type': hallway_type})
                    if random.random() < 0.05:
                        generate_object_in_coords(campaign_id, x, y, hallway_type, habitacion1)


def generate_monster(campaign_id, tile_type):
    from DnD_AI.default import COOL_NAMES, DEFAULT_RACES, DEFAULT_CLASSES, COOL_BOSSES_WITH_ICON, DEFAULT_RACE_PER_TILE_TYPE
    FILTERED_CLASSES = [entity_class for entity_class in DEFAULT_CLASSES if entity_class not in DEFAULT_RACES]

    #monster_race = random.choice(DEFAULT_RACES)
    monster_race = random.choice(DEFAULT_RACE_PER_TILE_TYPE[tile_type])
    monster_class = random.choice(FILTERED_CLASSES)

    magical_result = random.randint(7,13)
    physical_result = random.randint(7,13)
    survival_result = random.randint(7,13)


    optional_boss = random.random() < 0.05

    if optional_boss:
        weapon = generate_unique_weapon()
        multiplier = random.randint(3, 5)
        inventory=str({'gold':50, 'health potion': 3, 'go back bone': 1, 'key': 1})
    else:
        weapon = get_default_weapon(entity_class=monster_class) if random.random() < 0.5 else get_default_weapon(entity_class=monster_race)
        multiplier = 1
        inventory_random = random.random()
        inventory=str({'traductor': 1}) if inventory_random < 0.01 else str({'gold':random.randint(10,20)}) if inventory_random < 0.25 else str({'health potion': random.randint(1,3)}) if inventory_random < 0.5 else str({'go back bone': 1}) if inventory_random < 0.75 else str({'key': 1})


    monster = Monster.objects.create(
            is_boss=optional_boss,
            monster_race=monster_race,
            monster_class=monster_class,
            weapon=weapon,
            campaign_id=campaign_id,
            max_health=random.randint(20,30)*multiplier,
            strength=physical_result,
            intelligence=magical_result,
            recursiveness=survival_result,
            dexterity=random.randint(10,16),
            physical_resistance=physical_result, 
            magical_resistance=magical_result,
            constitution=survival_result,
            exp_drop=random.randint(20,40)*multiplier,
            inventory=inventory,
            x=0,
            y=0,
        )
    
    if random.random() < 0.05:
        monster.name = random.choice(COOL_NAMES)
    
    if optional_boss:
        monster_name = random.choice(COOL_BOSSES_WITH_ICON)
        monster_physical_description = monster_name

        icon_name = monster_name.replace(' ', '-').lower()
        icon_path = f"entity/icons/boss_icons/{icon_name}.png"

        monster.name = monster_name
        monster.physical_description = monster_physical_description
        monster.icon = icon_path
        monster.monster_race = ''
        monster.monster_class = ''

    monster.save()
    return monster
    

def generate_object_in_coords(campaign_id, x, y, tile_type, room=None):
    if random.random() < 0.3:
        generate_object(campaign_id, room, 'small_treasure', entity=None, x=x, y=y)
    else:
        monster = generate_monster(campaign_id, tile_type)
        generate_object(campaign_id, room, 'monster', monster, x=x, y=y)


def generate_object(campaign_id, room, object_type, entity=None, x=None, y=None):
    tries = 30
    while tries > 0:
        if x is None and y is None:
            x = random.randint(room.x, room.x + room.w - 1)
            y = random.randint(room.y, room.y + room.h - 1)

        if object_type == 'treasure':
            existent_treasure = Treasure.objects.filter(campaign_id=campaign_id, x=x, y=y)
            
            if not existent_treasure:
                if random.random() < 0.5:
                    Treasure.objects.create(campaign_id=campaign_id, treasure_type='Chest', x=x, y=y,
                                            inventory=str(
                                                {'gold': random.randint(30, 100), 'health potion': random.randint(3, 5), 'go back bone': random.randint(1, 3)}
                                                ))
                else:
                    Treasure.objects.create(campaign_id=campaign_id, treasure_type='Weapon', x=x, y=y,
                                            weapon=generate_unique_weapon(common_too=True),
                                            inventory=str(
                                                {'gold': random.randint(1, 50), 'health potion': random.randint(1, 3), 'go back bone': 1}
                                                ))
                break
            else:
                tries -= 1

        # bag = 33% gold = 33%, key = 33%

        # when bag: 
        # traductor = 1%, health potion = 32%, gold = 32%, go back bone = 32%
        elif object_type == 'small_treasure':
            existent_player = Character.objects.filter(campaign_id=campaign_id, x=x, y=y)
            existent_treasure = Treasure.objects.filter(campaign_id=campaign_id, x=x, y=y)
            existent_monster = Monster.objects.filter(campaign_id=campaign_id, x=x, y=y)
            
            if not existent_player and not existent_treasure and not existent_monster:
                spawn = random.random()
                if spawn < 0.33:
                    inventory = str({'traductor': 1}) if spawn < 0.01 else str({'health potion': random.randint(1, 2)}) if spawn < 0.11 else str({'gold': random.randint(3,10)}) if spawn < 0.22 else str({'go back bone': 1})
                    Treasure.objects.create(campaign_id=campaign_id, treasure_type='Bag', x=x, y=y,
                                            inventory=inventory)
                elif spawn < 0.66:
                    inventory = str({'gold': random.randint(10, 20)})
                    Treasure.objects.create(campaign_id=campaign_id, treasure_type='Gold', x=x, y=y,
                                            inventory=inventory)
                else:
                    inventory = str({'key': 1})
                    Treasure.objects.create(campaign_id=campaign_id, treasure_type='Key', x=x, y=y,
                                            inventory=inventory)
                break
            else:
                tries -= 1

        elif object_type == 'portal':
            existent_treasure = Treasure.objects.filter(campaign_id=campaign_id, x=x, y=y)
            if not existent_treasure:
                Treasure.objects.create(campaign_id=campaign_id, treasure_type='Portal', x=x, y=y)
                break
            else:
                tries -= 1

        elif object_type == 'discovered_portal':
            existent_treasure = Treasure.objects.filter(campaign_id=campaign_id, x=x, y=y)
            if not existent_treasure:
                Treasure.objects.create(campaign_id=campaign_id, treasure_type='Portal', x=x, y=y, discovered=True)
                break
            else:
                tries -= 1

        elif object_type == 'player':
            existent_player = Character.objects.filter(campaign_id=campaign_id, x=x, y=y)
            existent_treasure = Treasure.objects.filter(campaign_id=campaign_id, x=x, y=y)
            existent_monster = Monster.objects.filter(campaign_id=campaign_id, x=x, y=y)
            
            if not existent_player and not existent_treasure and not existent_monster:
                entity.x = x
                entity.y = y
                entity.save()
                break
            else:
                tries -= 1

        elif object_type == 'monster':
            existent_player = Character.objects.filter(campaign_id=campaign_id, x=x, y=y)
            existent_treasure = Treasure.objects.filter(campaign_id=campaign_id, x=x, y=y)
            existent_monster = Monster.objects.filter(campaign_id=campaign_id, x=x, y=y)
            
            if not existent_player and not existent_treasure and not existent_monster:
                entity.x = x
                entity.y = y
                entity.save()
                break
            else:
                tries -= 1

        elif object_type == 'boss':
            entity.x = x
            entity.y = y
            entity.save()
            break

        x, y = None, None

    if tries == 0:
        return False
    return True
    

def generate_dungeon_map(campaign: Campaign) -> bool:
    #campaign = Campaign.objects.get(id=campaign_id)
    #print(campaign)
    campaign_id = campaign.id
    dimx = int(campaign.size_x)
    dimy = int(campaign.size_y)

    if dimx * dimy > 500000:
        print('Mapa demasiado grande')
        return False
    
    mapa = np.full((dimy, dimx), '', dtype=object)

    total_tiles = dimx * dimy   # 200
    num_habitaciones = total_tiles // 200  # 1 habitación por cada 200 tiles

    room_types = ['path', 'dungeon', 'grass', 'dirt']
    boss_types = ['boss', 'psycho', 'hell', 'god']
    path_types = ['dirt', 'path', 'dungeon']
    portal_types = ['portal', 'psycho', 'hell', 'god']

    rooms = []
    while len(rooms) < num_habitaciones:
        room_type = random.choice(room_types)
        new_room = crear_habitacion(mapa, 4, 10, room_type)
        if new_room:
            if rooms:
                # Conectar con la habitación más cercana
                habitacion_cercana = min(rooms, key=lambda h: distance(h, new_room))

                # Quizás sería mejor ponerlo a lo último
                connect_rooms(mapa, habitacion_cercana, new_room, random.choice(path_types), campaign_id)
            rooms.append(new_room)
            mapa[new_room.y:new_room.y + new_room.h, new_room.x:new_room.x + new_room.w] = new_room.room_type

    # Designar habitaciones para spawn de jugadores, jefes y tesoros
    designar_habitaciones_especiales(rooms)

    boss_counter = 0
    key_bosses = Monster.objects.filter(campaign_id=campaign_id, is_boss=True, is_key=True)
    if key_bosses.count() < 3:          # 3 jefes clave
        key_bosses = generate_key_bosses(campaign_id, 3-key_bosses.count())

    #are_there_common_monsters = Monster.objects.filter(campaign_id=campaign_id, is_key=False).exists()

    for room in rooms:

        tile_type = room.room_type

        if room.spawn:
            tile_type = 'spawn'
            generate_object(campaign_id, room, 'discovered_portal')
            for player in Character.objects.filter(campaign_id=campaign_id):
                generate_object(campaign_id, room, 'player', player)

        elif room.boss:
            tile_type = random.choice(boss_types)
            try:
                generate_object(campaign_id, room, 'boss', key_bosses[boss_counter])
                boss_counter += 1
            except:
                pass

        elif room.portal:
            tile_type = random.choice(portal_types)
            generate_object(campaign_id, room, 'portal')

        elif room.treasure or room.boss:
            generate_object(campaign_id, room, 'treasure')
            # 20% de probabilidad de tener dos tesoros
            # 2% de probabilidad de tener tres tesoros
            how_much = random.random()
            if how_much < 0.02:
                generate_object(campaign_id, room, 'treasure')
                generate_object(campaign_id, room, 'treasure')
            elif how_much < 0.2:
                generate_object(campaign_id, room, 'treasure')

        fill_room(campaign_id, room, tile_type)

                


    
    non_boss_rooms = [room for room in rooms if not room.boss]
    #usable_rooms = [room for room in rooms if not room.spawn]

    for NPC in Character.objects.filter(campaign_id=campaign_id, is_playable=False):
        generate_object(campaign_id, random.choice(non_boss_rooms), 'player', NPC)
    
    '''
    for monster in Monster.objects.filter(campaign_id=campaign_id, is_key=False, is_boss=False):
        generate_object(campaign_id, random.choice(non_spawn_rooms), 'monster', monster)
    
    for monster in Monster.objects.filter(campaign_id=campaign_id, is_key=True, is_boss=False):
        generate_object(campaign_id, random.choice(non_spawn_rooms), 'monster', monster)

    for monster in Monster.objects.filter(campaign_id=campaign_id, is_key=False, is_boss=True):
        generate_object(campaign_id, random.choice(non_spawn_rooms), 'monster', monster)
    '''
    
    # we delete everythong in 0,0
    Monster.objects.filter(campaign_id=campaign_id, x=0, y=0, is_key = False).delete()
    Treasure.objects.filter(campaign_id=campaign_id, x=0, y=0).delete()

    return True

def fill_room(campaign_id, room, tile_type):
    for x in range(room.x, room.x + room.w):
        for y in range(room.y, room.y + room.h):
            Tile.objects.update_or_create(campaign_id=campaign_id, x=x, y=y, defaults={'tile_type': tile_type})

            if tile_type not in ['spawn', 'boss']:
                spawn = random.random()
                if spawn < 0.05:
                    generate_object_in_coords(campaign_id, x, y, tile_type, room)
                #elif spawn > 1-0.003:
                    #    generate_object_in_coords(campaign_id, x, y, tile_type) NPCCCC
                    #    la idea es generar un NPC

    # así se asegura que haya al menos una cosa interesante en cada habitación
    if tile_type not in ['spawn', 'boss']:
        x = random.randint(room.x, room.x + room.w - 1)
        y = random.randint(room.y, room.y + room.h - 1)
        generate_object_in_coords(campaign_id, x, y, tile_type, room)

# Ejemplo de uso
# no más de 500.000 tiles
# generate_mapa_dungeon(3)

# -----------------------------------------------------------------------------------------------------------

def generate_unique_weapon(common_too=False):
    from DnD_AI.default import UNIQUE_WEAPON_NAMES, UNIQUE_WEAPON_STATS, DEFAULT_WEAPON_NAMES, DEFAULT_WEAPON_STATS

    weapon_name = random.choice(list(UNIQUE_WEAPON_NAMES)) if not common_too else random.choice(list(UNIQUE_WEAPON_NAMES)+list(DEFAULT_WEAPON_NAMES))
    try:
        weapon_stats = UNIQUE_WEAPON_STATS[weapon_name]
    except:
        weapon_stats = DEFAULT_WEAPON_STATS[weapon_name]

    unique_weapon = Weapon.objects.get_or_create(
        is_template=True,
        name=weapon_name,
        is_ranged=weapon_stats['is_ranged'],
        weapon_type=weapon_stats['weapon_type'],  
        damage_type=weapon_stats['damage_type'],  
        physical_description=weapon_stats['physical_description'],
        image=weapon_stats['image'],
        damage=weapon_stats['damage'],
        range=weapon_stats['range'],
        range_level_points=0,
        durability=100,
    )
    unique_weapon[0].save()

    return unique_weapon[0]




def generate_key_bosses(campaign_id, n:int = 3):
    from DnD_AI.functions_AI import campaign_interpreter, image_generator_DallE, image_generator_StabDiff
    from DnD_AI.default import COOL_NAMES, DEFAULT_RACES, DEFAULT_CLASSES, COOL_BOSSES_WITH_ICON

    FILTERED_CLASSES = [player_class for player_class in DEFAULT_CLASSES if player_class not in DEFAULT_RACES]
    
    attributes_dict, API_KEY_GEMINI = campaign_interpreter(campaign_id, n)

    unique_weapons = [generate_unique_weapon() for _ in range(n)]

    key_bosses = []

    for i in range(n):

        no_api_name, no_api_boss_race, no_api_boss_class, no_api_physical_description = None, None, None, None
        if not API_KEY_GEMINI:
            no_api_name = random.choice(COOL_NAMES)
            no_api_boss_race = random.choice(DEFAULT_RACES)
            no_api_boss_class = random.choice(FILTERED_CLASSES)
            no_api_physical_description = no_api_boss_race+' '+no_api_boss_class

        key_boss = Monster.objects.create(
            name=no_api_name if not API_KEY_GEMINI else attributes_dict['name'][i],
            is_key=True,
            is_boss=True,
            monster_race=no_api_boss_race if not API_KEY_GEMINI else  attributes_dict['race'][i],
            monster_class=no_api_boss_class if not API_KEY_GEMINI else attributes_dict['class'][i],
            physical_description=no_api_physical_description if not API_KEY_GEMINI else  attributes_dict['physical_description'][i],
            weapon=unique_weapons[i],
            campaign_id=campaign_id,
            max_health=random.randint(4,6)*100,
            strength=random.randint(10,15),
            intelligence=random.randint(10,15),
            recursiveness=random.randint(10,15),
            dexterity=random.randint(10,15),
            physical_resistance=random.randint(10,15), 
            magical_resistance=random.randint(10,15),
            constitution=random.randint(10,15),
            inventory=str({'gold':500, 'health potion': 10, 'go back bone': 5, 'key': 5, 'traductor': 1}),
            exp_drop=1000,
            x=random.randint(0,10),
            y=random.randint(0,10),
        )

        boss_personality = random.choice(['making a smug face', 'laughing...', 'looking at you with a serious face', 'smiling', 'intimidating'])

        image_description = f"{key_boss.name}{key_boss.monster_race} {key_boss.monster_class} holding a {key_boss.weapon.weapon_type}, {key_boss.physical_description} is {boss_personality}"
        try:
            image_dir_DallE = image_generator_DallE(image_description).replace('media/', '')
            key_boss.icon = image_dir_DallE
        except:
            try:
                image_dir_StabDiff = image_generator_StabDiff(image_description).replace('media/', '')
                key_boss.icon = image_dir_StabDiff
            except:
                name = random.choice(COOL_BOSSES_WITH_ICON)
                icon_path = name.replace(' ', '-').lower()
                icon = f"entity/icons/boss_icons/{icon_path}.png"

                key_boss.name = name
                key_boss.icon = icon

        key_boss.save()

        key_bosses.append(key_boss)

    return key_bosses


# -----------------------------------------------------------------------------------------------------------

'''
# Visualización del mapa en matplotlib
    # Rellenar las rooms y los pasillos en el mapa
    for room in rooms:
        if room.spawn:
            mapa[room.y:room.y + room.h, room.x:room.x + room.w] = 'spawn'
        elif room.boss:
            mapa[room.y:room.y + room.h, room.x:room.x + room.w] = 'boss'
        elif room.treasure:
            mapa[room.y:room.y + room.h, room.x:room.x + room.w] = 'treasure'
        elif room.portal:
            mapa[room.y:room.y + room.h, room.x:room.x + room.w] = 'portal'
        else:
            mapa[room.y:room.y + room.h, room.x:room.x + room.w] = room.room_type

    # Convertir nombres a colores RGB
    
    color_map = {'': [0, 0, 0], 'path': [210, 180, 140], 'dungeon': [128, 128, 128], 'boss': [255, 0, 0], 'god': [255, 255, 0], 'psycho': [75, 0, 130], 'hell': [11, 111, 11], 'grass': [0, 128, 0], 'dirt': [139, 69, 19], 'Spawn': [255, 255, 224], 'Boss': [255, 0, 0], 'Treasure': [255, 223, 0]}
    
    color_map = {
        '':         [0, 0, 0], 
        'path':     [210, 180, 140], 
        'dungeon':  [128, 128, 128],
        'god':      [255, 255, 255], 
        'psycho':   [255, 255, 255],
        'hell':     [255, 255, 255],
        'grass':    [255, 255, 255],
        'dirt':     [255, 255, 255],
        
        'spawn':    [0, 0, 255],
        'boss':     [255, 0, 0],
        'treasure': [0, 255, 0],
        'portal':   [255, 100, 255],
        }
    
    mapa_colorido = np.array([[color_map[cell] for cell in row] for row in mapa])

    # Visualización
    plt.figure(figsize=(10, 10))
    plt.imshow(mapa_colorido, interpolation='nearest')
    plt.title("Mapa de Mazmorra Procedural con Juego Integrado")
    plt.xticks([])
    plt.yticks([])
    plt.show()
'''
