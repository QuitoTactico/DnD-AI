#import database of common names
from faker import Faker
from random import randint

fake = Faker()

def get_random_name():
    return fake.first_name()


DEFAULT_TILE_TYPES = {
    'grass':    'ground_grass_gen_07.png',
    'dirt':     'Dirt_02.png',
    'path':     '04univ3.png',
    'dungeon':  'rock_weathered_10.png',
    'boss':     'desert_cracksv_s.jpg',
    'god':      '461223113.jpg',
    'psycho':   '461223182.jpg',
    'hell':     '461223163.jpg',
}

DEFAULT_TREASURE_TYPES = {
    'Gold':             'gold',
    'Bag':              'bag',
    'Discovered Bag':   'bag-discovered',
    'Chest':            'chest',
    'Discovered Chest': 'chest-discovered',
    'Key':              'key',
    'Weapon' :          'weapon',
    'Tombstone':        'tombstone',
}

DEFAULT_WEAPON_PER_RACE = {
    'Alien': 'Magic Wand',
    'Angel': 'Sword',
    'Basilisk': 'Beast Claws',
    'Centaur': 'Bow',
    'Chicken': 'Beast Claws',
    'Chimera': 'Fangs',
    'Cyclop': 'Great Warhammer',
    'Demon': 'Trident',
    'Dragon': 'Beast Claws',
    'Druid': 'Staff',
    'Dwarf': 'Warhammer',
    'Elf': 'Bow',
    'Fairy': 'Magic Wand',
    'Fox': 'Fangs',
    'Ghost': 'Scythe',
    'Giant': 'Great Warhammer',
    'Goblin': 'Dagger',
    'Golem': 'Great Warhammer',
    'Harpy': 'Bow',
    'Human': 'Sword',
    'Hydra': 'Fangs',
    'Indigenous': 'Blowpipe',
    'Kiwi': 'Beast Claws',
    'Medusa': 'Sword',
    'Mermaid': 'Trident',
    'Mimic': 'Fangs',
    'Minotaur': 'Battleaxe',
    'Mummy': 'Scythe',
    'Orc': 'Axe',
    'Rat': 'Fangs',
    'Scorpion': 'Tail',
    'Skeleton': 'Sword',
    'Spider': 'Fangs',
    'Troll': 'Warhammer',
    'Unicorn': 'Horns',
    'Vampire': 'Fangs',
    'Werewolf': 'Beast Claws',
    'Wolf': 'Beast Claws',
    'Zombie': 'Bare hands',
}

DEFAULT_WEAPON_PER_CLASS = {
    'Alchemist': 'Dagger',
    'Archer': 'Long Bow',
    'Artificer': 'Dagger',
    'Assassin': 'Crossbow',
    'Barbarian': 'Axe',
    'Bard': 'Dagger',
    'Blacksmith': 'Warhammer',
    'Cleric': 'Mace',
    'Cowboy': 'Revolver',
    'Farmer': 'Trident',
    'Fighter': 'Bare hands',
    'Hunter': 'Bow',
    'Knight': 'Sword',
    'Lancer': 'Spear',
    'Mage': 'Staff',
    'Merchant': 'Katana',
    'Monk': 'Bare hands',
    'Ninja': 'Shurikens',
    'Overlord': 'Great Warhammer',
    'Paladin': 'Sword',
    'Pirate': 'Sabres',
    'Ranger': 'Bow',
    'Rogue': 'Dagger',
    'Samurai': 'Katana',
    'Soldier': 'Sword',
    'Spartan': 'Spear',
    'Tribal': 'Blowpipe',
    'Viking': 'Battleaxe',
    'Warrior': 'Sword',
    'Witch': 'Enchanted Book',
    'Wizard': 'Staff',
}
#DEFAULT_WEAPON_PER_RACE.update(DEFAULT_WEAPON_PER_CLASS)
DEFAULT_WEAPON_PER_CLASS.update(DEFAULT_WEAPON_PER_RACE)


DEFAULT_WEAPON_STATS = {
    'Sword': {
        'weapon_type': 'Sword',
        'damage': 10,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'a sword',
        'image': 'weapon/images/default/sword.png',
        'damage_type': 'Physical'
    },
    'Bow': {
        'weapon_type': 'Bow',
        'damage': 6,
        'range': 3,
        'is_ranged': True,
        'physical_description': 'a bow',
        'image': 'weapon/images/default/bow.png',
        'damage_type': 'Physical'
    },
    'Staff': {
        'weapon_type': 'Staff',
        'damage': 8,
        'range': 2,
        'is_ranged': True,
        'physical_description': 'a staff',
        'image': 'weapon/images/default/staff.png',
        'damage_type': 'Magical'
    },
    'Beast Claws': {
        'weapon_type': 'Body Part',
        'damage': 8,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'beast claws',
        'image': 'weapon/images/default/claws.png',
        'damage_type': 'Physical'
    },
    'Dagger': {
        'weapon_type': 'Dagger',
        'damage': 7,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'a dagger',
        'image': 'weapon/images/default/dagger.png',
        'damage_type': 'Physical'
    },
    'Mace': {
        'weapon_type': 'Mace',
        'damage': 9,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'a mace',
        'image': 'weapon/images/default/mace.png',
        'damage_type': 'Physical'
    },
    'Axe': {
        'weapon_type': 'Axe',
        'damage': 11,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'an axe',
        'image': 'weapon/images/default/axe.png',
        'damage_type': 'Physical'
    },
    'Bare hands': {
        'weapon_type': 'Body Part',
        'damage': 6,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'bare hands',
        'image': 'weapon/images/default/bare_hands.png',
        'damage_type': 'Physical'
    },
    'Crossbow': {
        'weapon_type': 'Crossbow',
        'damage': 7,
        'range': 4,
        'is_ranged': True,
        'physical_description': 'a crossbow',
        'image': 'weapon/images/default/crossbow.png',
        'damage_type': 'Physical'
    },
    'Long Bow': {
        'weapon_type': 'Bow',
        'damage': 7,
        'range': 4,
        'is_ranged': True,
        'physical_description': 'a long bow',
        'image': 'weapon/images/default/long_bow.png',
        'damage_type': 'Physical'
    },
    'Blowpipe': {
        'weapon_type': 'Blowpipe',
        'damage': 5,
        'range': 3,
        'is_ranged': True,
        'physical_description': 'a blowpipe',
        'image': 'weapon/images/default/blowpipe.png',
        'damage_type': 'Physical'
    },
    'Warhammer': {
        'weapon_type': 'Warhammer',
        'damage': 12,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'a warhammer',
        'image': 'weapon/images/default/warhammer.png',
        'damage_type': 'Physical'
    },
    'Battleaxe': {
        'weapon_type': 'Axe',
        'damage': 10,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'a battleaxe',
        'image': 'weapon/images/default/battleaxe.png',
        'damage_type': 'Physical'
    },
    'Revolver': {
        'weapon_type': 'Gun',
        'damage': 5,
        'range': 4,
        'is_ranged': True,
        'physical_description': 'a revolver',
        'image': 'weapon/images/default/revolver.png',
        'damage_type': 'Physical'
    },
    'Trident': {
        'weapon_type': 'Trident',
        'damage': 10,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'a trident',
        'image': 'weapon/images/default/trident.png',
        'damage_type': 'Physical'
    },
    'Shurikens': {
        'weapon_type': 'Throwable',
        'damage': 7,
        'range': 3,
        'is_ranged': True,
        'physical_description': 'shurikens',
        'image': 'weapon/images/default/shurikens.png',
        'damage_type': 'Physical'
    },
    'Spear': {
        'weapon_type': 'Spear',
        'damage': 9,
        'range': 2,
        'is_ranged': True,
        'physical_description': 'a spear',
        'image': 'weapon/images/default/spear.png',
        'damage_type': 'Physical'
    },
    'Katana': {
        'weapon_type': 'Sword',
        'damage': 11,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'a katana',
        'image': 'weapon/images/default/katana.png',
        'damage_type': 'Physical'
    },
    'Fangs': {
        'weapon_type': 'Body Part',
        'damage': 9,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'fangs',
        'image': 'weapon/images/default/fangs.png',
        'damage_type': 'Physical'
    },
    'Sabres': {
        'weapon_type': 'Sword',
        'damage': 9,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'two crossed sabres',
        'image': 'weapon/images/default/sabres.png',
        'damage_type': 'Physical'
    },
    'Scythe': {
        'weapon_type': 'Scythe',
        'damage': 10,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'a scythe',
        'image': 'weapon/images/default/scythe.png',
        'damage_type': 'Physical'
    },
    'Enchanted Book': {
        'weapon_type': 'Book',
        'damage': 8,
        'range': 2,
        'is_ranged': True,
        'physical_description': 'an enchanted book',
        'image': 'weapon/images/default/enchanted_book.png',
        'damage_type': 'Magical'
    },
    'Great Warhammer': {
        'weapon_type': 'Warhammer',
        'damage': 13,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'a great warhammer',
        'image': 'weapon/images/default/great_warhammer.png',
        'damage_type': 'Physical'
    },
    'Magic Wand': {
        'weapon_type': 'Wand',
        'damage': 7,
        'range': 2,
        'is_ranged': True,
        'physical_description': 'a Magic wand',
        'image': 'weapon/images/default/magic_wand.png',
        'damage_type': 'Magical'
    },
    'Horns': {
        'weapon_type': 'Body Part',
        'damage': 7,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'his horns',
        'image': 'weapon/images/default/horns.png',
        'damage_type': 'Physical'
    },
    'Tail': {
        'weapon_type': 'Body Part',
        'damage': 9,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'a tail',
        'image': 'weapon/images/default/tail.png',
        'damage_type': 'Physical'
    },
}

DEFAULT_MONSTER_STATS = {
    'Goblin': {
        'name': 'Goblin '+get_random_name(),
        
        'image': 'monster/images/default/goblin.png',
        'description': 'A small, green creature with a big nose and pointy ears. It is known for its cowardice and its love for gold.'
    },
}

#print(DEFAULT_MONSTER_STATS['Goblin']['name'])


# strange things, don't take this seriously

POSSIBLE_BOSSES = [
    'The Sphinx', 
    'Cthulhu', 
    'The Leviathan', 
    'Behemoth', 
    'The Kraken', 
    'Hades', 
    'Cerberus', 
    'GOD', 
    'Zeus', 
    'Ares', 
    'Thanatos', 
    'Megatron', 
    'Mr Beast', 
    'Lord Voldemort', 
    'Your Mom', 
    'The Devil', 
    'Telematica Demon', 
    'Diomedes Diaz', 
    'Makima', 
    'Donald Trump', 
    'MechaHitler', 
    'John Cena', 
    'The Rock', 
    'Undertaker', 
    'Jackie Chan', 
    'Megamind', 
    'Shrek', 
    'Darth Vader', 
    'Sauron', 
    'Mike Wazousky', 
    'The Joker', 
    'John Wick', 
    'Cristionel Messinaldo', 
    'Fernanfloo', 
    'Michael Jackson', 
    'PewDiePie', 
    'Elon Musk', 
    'Terminator', 
    'The Creators: a Malformed Three-Headed Beast Who Rules Everything and Fears Nothing', 
    'Yourself but Chinese', 
    'Hatsune Miku', 
    'Racism Demon', 
    'The Cancer', 
    'NekoKiller', 
    'Mbappe', 
    'Dross Rotzank', 
    'Doc Tops', 
    'El Putas de Aguadas', 
    'Waluigi', 
    'Slenderman', 
    'Flying Spagguetti God', 
    'Sonic.exe', 
    'Spongebob', 
    'Sans', 
    'The Game', 
    'Juan Carlos', 
    'El Pepe', 
    'Ete Sech', 
    'Tilín', 
    'Eminem', 
    'Yourself', 
    'Wolverine', 
    'Dracula', 
    'Link', 
    'The Hollow Knight', 
    'Moai', 
    'Skeleton King', 
    'Anubis', 
    'Fetus',
    'Conde Eyácula',
    'Jax: Minor Hunter',
    'Unas salchipapas',
    'Sr. Pelo',
    'Molinete',
    'Powerbazinga',
    'Vegetta: The Bear Hunter',
    'El payaso que se esconde de los gays',
    'Cirno',
    'Tyler The Creator',
    'Kratos',
    'Trece',
    '13',
    'Hello Kitty',
    'DoomSlayer',
    'El espectro del fortinaiti',
    'Skinwalker',
    'SirenHead',
    'Skibidi Toilet',
    'Titan Speakerman',
    'The End',
    'Bloodbath',
    'Tidal Wave',
    'RobTop',
    'GuitarHeroStyles',
    'Tienes 13 activa cam',
    'Akira Toriyama',
    'Kanye West',
    'Meru The Demon',
    'Ankha',
    'Auronplay',
    'Jim Carrey',
    'El Chavo',
    'Roblox God',
    'ERR 404',
    'Circular 303',
    'Circular 302',
    'Kick Buttowsky',
    'Acetato',
    'Dr. Doofenshmirtz',
    'Genio Peruano',
    'Kronk',
    'THE ZULU',
    'Lucio',
    'Roberta'
]

COOL_SORCERY_NAMES = [
    "Qui's Crotolamo",
    "Qui's Uxiono",
    'Testicular Torsion',
    'Anal Palpitations',
    'Rats... Take his balls',
    'The one who moves is gay',
    'Automatic breathing deactivation',
    'The Game'
]


COOL_NPCS = [
    'El Ayudador de Pibes',
    'El Vendedor de Vainas',
    'Diomedes Diaz',

]

COOL_LOCATIONS = [
    'El club de las papeadas',
    'Taberna el Balde de ###',
    'La Montañañañañañaña'
]


COOL_EVENTS = {
    # familia de lechugas, todos son opcionales. Si matas muchos de ellos tendrás que pagar por tus pecados
    'LETTUCE FAMILY': [  
        'Lettuce Boy',
        'Lettuce Man',
        'Lotus Girl',
        'Lotus M.I.L.F',
        'SINNER LETTUCE: THE KILLER',
        'LETTUCE GOD: THE IMMORTAL',
        'UNIVERSAL LETTUCE: THE ALL-BEYONDER',
        'Last Lettuce on the World...',
        'Lotus Avenger'
    ],
    # evento del club de comedores de niños, debes acabar con todos
    # esto fué autogenerado y me pareció demasiado gracioso como para borrarlo, dios mío
    'KID EATERS': [
        'El que se come a los niños',
        'El que se come a los niños pero con salsa',
        'El que se come a los niños pero con salsa de tomate',
        'El que se come a los niños pero con salsa de tomate y queso',
        'El que se come a los niños pero con salsa de tomate y queso rallado',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate y un plato de galletitas',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate y un plato de galletitas y un plato de frutas',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate y un plato de galletitas y un plato de frutas y un plato de verduras',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate y un plato de galletitas y un plato de frutas y un plato de verduras y un plato de carne',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate y un plato de galletitas y un plato de frutas y un plato de verduras y un plato de carne y un plato de pescado',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate y un plato de galletitas y un plato de frutas y un plato de verduras y un plato de carne y un plato de pescado y un plato de pastas',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate y un plato de galletitas y un plato de frutas y un plato de verduras y un plato de carne y un plato de pescado y un plato de pastas y un plato de arroz',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate y un plato de galletitas y un plato de frutas y un plato de verduras y un plato de carne y un plato de pescado y un plato de pastas y un plato de arroz y un plato de sopa',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate y un plato de galletitas y un plato de frutas y un plato de verduras y un plato de carne y un plato de pescado y un plato de pastas y un plato de arroz y un plato de sopa y un plato de postre',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate y un plato de galletitas y un plato de frutas y un plato de verduras y un plato de carne y un plato de pescado y un plato de pastas y un plato de arroz y un plato de sopa y un plato de postre y un plato de helado',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate y un plato de galletitas y un plato de frutas y un plato de verduras y un plato de carne y un plato de pescado y un plato de pastas y un plato de arroz y un plato de sopa y un plato de postre y un plato de helado y un plato de frutas secas',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate y un plato de galletitas y un plato de frutas y un plato de verduras y un plato de carne y un plato de pescado y un plato de pastas y un plato de arroz y un plato de sopa y un plato de postre y un plato de helado y un plato de frutas secas y un plato de frutas en almibar',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate y un plato de galletitas y un plato de frutas y un plato de verduras y un plato de carne y un plato de pescado y un plato de pastas y un plato de arroz y un plato de sopa y un plato de postre y un plato de helado y un plato de frutas secas y un plato de frutas en almibar y un plato de frutas en almibar con crema',
        'El que se come a los niños pero con salsa de tomate y queso rallado y pan tostado con manteca y un vaso de leche con chocolate y un plato de galletitas y un plato de frutas y un plato de verduras y un plato de carne y un plato de pescado y un plato de pastas y un plato de arroz y un plato de sopa y un plato de postre y un plato de helado y un plato de frutas secas y un plato de frutas en almibar y un plato de frutas en almibar con crema y un plato de frutas en almibar con crema y un vaso de jugo'
    ]
}

'''


'''