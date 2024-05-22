#import database of common names
from faker import Faker
from random import randint

fake = Faker()

def get_random_name():
    return fake.first_name()


DEFAULT_TILE_TYPES = {
    'grass':    'ground_grass_gen_07.png',
    'dirt':     'Dirt_02.png',
    'god':      '461223113.jpg',
    'psycho':   '461223182.jpg',
    'hell':     '461223163.jpg',

    'path':     '04univ3.png',
    'dungeon':  'rock_weathered_10.png',
    
    'spawn':     'random/461223123.jpg',
    'treasure':  'random/461223113.jpg',
    'portal':    'random/461223123.jpg',
    'boss':      'desert_cracksv_s.jpg',
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
    'Portal':           'portal',
    'Discovered Portal':'portal-discovered',
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
    'Moai': 'Great Warhammer',
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

DEFAULT_RACES = DEFAULT_WEAPON_PER_RACE.keys()

DEFAULT_WEAPON_PER_CLASS = {
    'Alchemist': 'Dagger',
    'Archer': 'Long Bow',
    'Artificer': 'Dagger',
    'Assassin': 'Crossbow',
    'Barbarian': 'Axe',
    'Bard': 'Dagger',
    'Blacksmith': 'Warhammer',
    'Brute': 'Mace',
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

DEFAULT_CLASSES = DEFAULT_WEAPON_PER_CLASS.keys()

DEFAULT_WEAPON_PER_CLASS.update(DEFAULT_WEAPON_PER_RACE)


DEFAULT_RACE_PER_TILE_TYPE = {
    'grass': [
        'Centaur', 'Elf', 'Druid', 'Fairy', 'Human', 'Indigenous', 'Werewolf', 'Unicorn', 'Alien'
    ],
    'dirt': [
        'Dwarf', 'Goblin', 'Orc', 'Troll', 'Rat', 'Wolf', 'Chimera', 'Hydra', 'Zombie'
    ],
    'god': [
        'Angel', 'Fairy', 'Unicorn', 'Elf', 'Alien'
    ],
    'psycho': [
        'Vampire', 'Werewolf', 'Demon', 'Ghost', 'Chimera', 'Hydra', 'Medusa'
    ],
    'hell': [
        'Demon', 'Dragon', 'Skeleton', 'Zombie', 'Vampire', 'Golem', 'Ghost'
    ],
    'path': [
        'Human', 'Elf', 'Centaur', 'Harpy', 'Goblin', 'Demon', 'Ghost', 'Medusa'
    ],
    'dungeon': [
        'Mummy', 'Skeleton', 'Minotaur', 'Golem', 'Cyclop', 'Moai', 'Dragon', 'Vampire'
    ],
    'treasure': [
        'Mimic', 'Dragon', 'Rat', 'Troll', 'Demon', 'Alien', 'Angel', 'Chimera', 'Hydra', 'Medusa', 'Vampire', 'Zombie', 'Ghost'
    ],
    'portal': [
        'Alien', 'Chimera', 'Dragon', 'Fairy', 'Ghost'
    ]
}



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

DEFAULT_WEAPON_NAMES = DEFAULT_WEAPON_STATS.keys()

UNIQUE_WEAPON_STATS = {
    'Bat Blade': {
        'weapon_type': 'Sword',
        'damage': 25,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'A menacing blade shaped like a bat',
        'image': 'weapon/images/boss_weapons/bat-blade.png',
        'damage_type': 'Physical'
    },
    'Bloody Sword': {
        'weapon_type': 'Sword',
        'damage': 27,
        'range': 2,
        'is_ranged': False,
        'physical_description': 'A sword perpetually covered in blood',
        'image': 'weapon/images/boss_weapons/bloody-sword.png',
        'damage_type': 'Physical'
    },
    'Bouncing Sword': {
        'weapon_type': 'Sword',
        'damage': 22,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'A sword that vibrates and bounces when swung',
        'image': 'weapon/images/boss_weapons/bouncing-sword.png',
        'damage_type': 'Physical'
    },
    'Chainsaw': {
        'weapon_type': 'Chainsaw',
        'damage': 30,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'A brutal chainsaw for tearing through enemies',
        'image': 'weapon/images/boss_weapons/chainsaw.png',
        'damage_type': 'Physical'
    },
    'Coiled Nail': {
        'weapon_type': 'Spear',
        'damage': 26,
        'range': 2,
        'is_ranged': False,
        'physical_description': 'A coiled nail repurposed as a deadly weapon',
        'image': 'weapon/images/boss_weapons/coiled-nail.png',
        'damage_type': 'Physical'
    },
    'Crossed Pistols': {
        'weapon_type': 'Pistol',
        'damage': 28,
        'range': 5,
        'is_ranged': True,
        'physical_description': 'A pair of crossed pistols ready for a quick draw',
        'image': 'weapon/images/boss_weapons/crossed-pistols.png',
        'damage_type': 'Physical'
    },
    'Curled Tentacle': {
        'weapon_type': 'Whip',
        'damage': 24,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'A large curled tentacle, flexible and dangerous',
        'image': 'weapon/images/boss_weapons/curled-tentacle.png',
        'damage_type': 'Physical'
    },
    'Diving Dagger': {
        'weapon_type': 'Dagger',
        'damage': 20,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'A sleek dagger designed for swift attacks',
        'image': 'weapon/images/boss_weapons/diving-dagger.png',
        'damage_type': 'Physical'
    },
    'Dripping Blade': {
        'weapon_type': 'Sword',
        'damage': 29,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'A blade that drips with a mysterious liquid',
        'image': 'weapon/images/boss_weapons/dripping-blade.png',
        'damage_type': 'Physical'
    },
    'Dripping Sword': {
        'weapon_type': 'Sword',
        'damage': 23,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'A sword that drips an eerie, toxic substance',
        'image': 'weapon/images/boss_weapons/dripping-sword.png',
        'damage_type': 'Physical'
    },
    'Flamethrower': {
        'weapon_type': 'Flamethrower',
        'damage': 28,
        'range': 5,
        'is_ranged': True,
        'physical_description': 'A deadly flamethrower that spews fire at a distance',
        'image': 'weapon/images/boss_weapons/flamethrower.png',
        'damage_type': 'Physical'
    },
    'Flaming Trident': {
        'weapon_type': 'Trident',
        'damage': 26,
        'range': 4,
        'is_ranged': False,
        'physical_description': 'A trident wreathed in flames, capable of burning as well as piercing',
        'image': 'weapon/images/boss_weapons/flaming-trident.png',
        'damage_type': 'Magical'
    },
    'Knife Fork': {
        'weapon_type': 'Knife',
        'damage': 24,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'A quirky weapon that resembles kitchen utensils',
        'image': 'weapon/images/boss_weapons/knife-fork.png',
        'damage_type': 'Physical'
    },
    'Lightning Saber': {
        'weapon_type': 'Saber',
        'damage': 29,
        'range': 3,
        'is_ranged': True,
        'physical_description': 'A saber that crackles with electric energy',
        'image': 'weapon/images/boss_weapons/lightning-saber.png',
        'damage_type': 'Magical'
    },
    'Panzerfaust': {
        'weapon_type': 'Launcher',
        'damage': 30,
        'range': 6,
        'is_ranged': True,
        'physical_description': 'A powerful rocket launcher with devastating impact',
        'image': 'weapon/images/boss_weapons/panzerfaust.png',
        'damage_type': 'Physical'
    },
    'Reaper Scythe': {
        'weapon_type': 'Scythe',
        'damage': 27,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'A dark, menacing scythe that reaps souls',
        'image': 'weapon/images/boss_weapons/reaper-scythe.png',
        'damage_type': 'Magical'
    },
    'Relic Blade': {
        'weapon_type': 'Sword',
        'damage': 25,
        'range': 2,
        'is_ranged': False,
        'physical_description': 'An ancient blade imbued with mystical powers',
        'image': 'weapon/images/boss_weapons/relic-blade.png',
        'damage_type': 'Magical'
    },
    'Rune Sword': {
        'weapon_type': 'Sword',
        'damage': 22,
        'range': 2,
        'is_ranged': False,
        'physical_description': 'A sword carved with enigmatic runes that glow ominously',
        'image': 'weapon/images/boss_weapons/rune-sword.png',
        'damage_type': 'Magical'
    },
    'Sai': {
        'weapon_type': 'Dagger',
        'damage': 20,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'A pair of sai, perfect for quick, close combat',
        'image': 'weapon/images/boss_weapons/sai.png',
        'damage_type': 'Physical'
    },
    'Sawed-Off Shotgun': {
        'weapon_type': 'Shotgun',
        'damage': 26,
        'range': 4,
        'is_ranged': True,
        'physical_description': 'A brutally effective sawed-off shotgun for close-range mayhem',
        'image': 'weapon/images/boss_weapons/sawed-off-shotgun.png',
        'damage_type': 'Physical'
    },
    'Scales': {
        'weapon_type': 'Body Part',
        'damage': 21,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'Hard, protective scales that can also be used offensively',
        'image': 'weapon/images/boss_weapons/scales.png',
        'damage_type': 'Physical'
    },
    'Spinning Sword': {
        'weapon_type': 'Sword',
        'damage': 28,
        'range': 2,
        'is_ranged': False,
        'physical_description': 'A sword designed to spin on its axis, increasing its lethality',
        'image': 'weapon/images/boss_weapons/spinning-sword.png',
        'damage_type': 'Physical'
    },
    'Thompson M1': {
        'weapon_type': 'Rifle',
        'damage': 27,
        'range': 6,
        'is_ranged': True,
        'physical_description': 'A classic Thompson M1 submachine gun with a high rate of fire',
        'image': 'weapon/images/boss_weapons/thompson-m1.png',
        'damage_type': 'Physical'
    },
    'Thrown Daggers': {
        'weapon_type': 'Dagger',
        'damage': 23,
        'range': 5,
        'is_ranged': True,
        'physical_description': 'A set of daggers designed for precise throwing',
        'image': 'weapon/images/boss_weapons/thrown-daggers.png',
        'damage_type': 'Physical'
    },
    'Umbrella Bayonet': {
        'weapon_type': 'Bayonet',
        'damage': 24,
        'range': 3,
        'is_ranged': True,
        'physical_description': 'An unconventional weapon combining an umbrella with a sharp bayonet',
        'image': 'weapon/images/boss_weapons/umbrella-bayonet.png',
        'damage_type': 'Physical'
    },
    'Wave Strike': {
        'weapon_type': 'Wave Emitter',
        'damage': 29,
        'range': 5,
        'is_ranged': True,
        'physical_description': 'A device that emits powerful shockwaves to strike opponents',
        'image': 'weapon/images/boss_weapons/wave-strike.png',
        'damage_type': 'Magical'
    },
    'Winged Sword': {
        'weapon_type': 'Sword',
        'damage': 26,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'A sword with wings that enhance maneuverability and speed',
        'image': 'weapon/images/boss_weapons/winged-sword.png',
        'damage_type': 'Physical'
    },
    'Wolverine Claws': {
        'weapon_type': 'Claws',
        'damage': 30,
        'range': 1,
        'is_ranged': False,
        'physical_description': 'A set of retractable claws that can tear through almost anything',
        'image': 'weapon/images/boss_weapons/wolverine-claws.png',
        'damage_type': 'Physical'
    }
}

UNIQUE_WEAPON_NAMES = UNIQUE_WEAPON_STATS.keys() 


DEFAULT_MONSTER_STATS = {
    'Goblin': {
        'name': 'Goblin '+get_random_name(),
        
        'image': 'monster/images/default/goblin.png',
        'description': 'A small, green creature with a big nose and pointy ears. It is known for its cowardice and its love for gold.'
    },
}

#print(DEFAULT_MONSTER_STATS['Goblin']['name'])


# strange things, don't take this seriously

COOL_NAMES = [
    'The Sphinx (Friendly)', 
    'Cthulhu (Friendly)', 
    'The Leviathan (Friendly)', 
    'Behemoth', 
    'The Kraken (Friendly)', 
    'Hades (Friendly)', 
    'Cerberus (Friendly)', 
    'GOD (Friendly)', 
    'Zeus', 
    'Ares', 
    'Thanatos', 
    'Megatron', 
    'Mr Beast', 
    'Lord Voldemort', 
    'Your Mom', 
    'Your Mom (Friendly)', 
    'Your Mom (My Wife)', 
    'The Devil', 
    'Telematica Demon', 
    'Diomedes Diaz', 
    'Makima', 
    'Donald Trump', 
    'MechaHitler',
    'Hitler Neko', 
    'Gentrificación',
    'Pobreza',
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
    'Juan Carlos Mecha', 
    'Juan Carlos Neko', 
    'Juan Carlos Gamer',
    'Juan Carlos (Friendly)', 
    'El Pepe', 
    'Penesaurio', 
    'Furry Hitler',
    'Furry Love II',
    'Furry', 
    'Ete Sech', 
    'El Chavo',
    'Don Octavio',
    'Le Pegué Una Machetera Que Hasta Yo Quedé Asustado',
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
    'Unas Salchipapas',
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
    'Roberta',
    'El Ayudador de Pibes',
    'El Vendedor de Weas',
    'Diomedes Diaz',
    'El Rector de la Nacho',
    'El c papu :v',
    'When haces tus momos en NPCs',
    'COCK, MI FRONT',
    'Oscar.',
    'Papá de Oscar.',
    'Hijo de Oscar.',
    'xXx PAPU xXx',
    'Mamá Luchona',
    'Skibidi Sigma Pomni Digital Fortnite Chamba Free Gigachad Rizz Ohmygodfloo XXXTentacion Hotmail Lionel Ronaldo Junior Mewing Tercero Chiki Ibai Xocas Ete Sech Golden Toy Puppet Ohio Rubén Tuesta YouTubeproinsano Globodetexto51 Decadencia777',
    'Mewing',
    'El Joven',
    'Jonathan Betancur Espinosa',
    'Jonny',
    'Comeme el pingo',
    'Ping 255.255.255.255',
    'El que lo lea es gei',
    'Bronnies',
    'Jesucristo en Patineta',
    'Jesucristo, el Robot del Futuro',
    'Jesucristo Superestrella',
    'Jesús Negro',
    'Blasphemous',
    'ElP4Pu',
    'QuitoTactico',
    'TheQuito',
    'Cock',
    'Chiki',
    'Tetr.io',
    'Bocchi',
    'Nyanyame nyanyaju nyanyado no nyarabi de nyakunyaku inyanyaku nyanyahan nyanya-dai nyannyaku nyarabete nyagannyagame',
    'Covid-19',
    'Señora Chismosa',
    'a',
    'Mondongo',
    'Pocoyó',
    'aksfbjdfsjdfjsdsjdkhfksd',
    'Marrano Agua',
    'Jugador de LoL',
    'El Capitalismo',
    'Never Gonna Give You Up, Never Gonna Let You Down...',
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',

    'Lettuce Boy',
    'Lettuce Man',
    'Lotus Girl',
    'Lotus M.I.L.F',
    'SINNER LETTUCE: THE KILLER',
    'LETTUCE GOD: THE IMMORTAL',
    'UNIVERSAL LETTUCE: THE ALL-BEYONDER',
    'Last Lettuce on the World...',
    'Lotus Avenger',
]

COOL_BOSSES_WITH_ICON = ['Anubis', 'Australia', 'Bird Mask', 'Bolivia', 'Brazil', 'Caesar', 'Croc Jaws', 'Crystal Eye', 'Delighted', 'Diamonds Smile', 'Dracula', 'Evil Minion', 'Fetus', 'Frankenstein Creature', 'Gaze', 'Gluttonous Smile', 'Grim Reaper', 'Honeycomb', 'Horned Reptile', 'Hunter Eyes', 'Insect Jaws', 'Kenku Head', 'Kraken Tentacle', 'Mad Scientist', 'Maze Cornea', 'Mecha Mask', 'Metal Golem Head', 'Mewing', 'Octogonal Eye', 'One Eyed', 'Overlord', 'Paranoia', 'Pick Of Destiny', 'Pou', 'Pummeled', 'Purple Tentacle', 'Skeleton King', 'Sphinx', 'Spiked Armor', 'Swallow', 'Tangerine', 'Tear Tracks', 'Thunder Struck', 'Toad Teeth', 'Triton Head', 
                         
'177013', 'Ahuevo', 'Alien Bug', 'Android', 'Apocalipsis Rider', 'At Field', 'Bad Gnome', 'Balkenkreuz', 'Battle Tank', 'Best Waifu', 'Bloque 20', 'Bts', 'Buenos Dias', 'Bullet Bill', 'C Mamut', 'Caries', 'Carlos', 'Cat God', 'Chad', 'Chayanne', 'Chernobil Survivor', 'Circular 303', 'Cj', 'Coconut', 'Colombian Statue', 'Completely Normal Qr', 'Corn', 'Cristobal Colon', 'Crystal Queen', 'Dakimakura', 'Dead Man', 'Depression', 'Diablo', 'Did You Know', 'Dinosaur Rex', 'Double Dragon', 'Drip', 'Drugs', 'Economy', 'El Corazon Tucun', 'El Fin Se Acerca', 'Estafadora', 'Evil Tree', 'Family', 'Fat', 'Freddy Mercury', 'Frog Prince', 'Furro Triste', 'Furry Gang', 'Gallo Con Tenis', 'Gargoyle', 'Get Rickrolled', 'Gigachad', 'Girlfriend', 'God', 'Goku According To Tablos', 'Gooey Daemon', 'Gorda De Botero', 'Guebo', 'Hehe', 'Hentai', 'Hola', 'Hora De Ver La Hora', 'Human Pyramid', 'Ice Golem', 'Idk Whats This', 'If You Know You Know', 'Illuminati', 'Intel', 'Jesus', 'Juan Pis', 'Kamikaze', 'Kanye West', 'Kys Now', 'Lambda', 'Leonidas', 'Loss', 'Lynx', 'Malenia', 'Mantis', 'Marselo', 'Me Right Now', 'Me Seeing You Through The Cam', 'Megachad', 'Messi', 'Metamorphosis', 'Mexican', 'Momazos Diego', 'Mona Lisa', 'Mondongo', 'Mr Beast', 'My Dog', 'My Mom Dissapointed', 'Natural Selection', 'Number One', 'Nyanyame Nyanyaju Nyanyado No Nyarabi De Nyakunyaku Inyanyaku Nyanyahan Nyanya Dai Nyannyaku Nyarabete Nyagannyagame', 'O O', 'Odin', 'Omg', 'Paid Developers (Not Us)', 'Penguin', 'Pharaoh', 'Pimiento', 'Pinata', 'Pineapple', 'Plague Doctor', 'Plato', 'Pn', 'Pope', 'Prisoner', 'Que Pro', 'Reproductive Activities', 'Robin Hood', 'Saber Toothed Cat', 'Samus', 'Sasquatch', 'Satanic', 'Sayori', 'Sherlock Holmes', 'Shrimp', 'Si', 'Sisyphus', 'Spaggueti God', 'Sun Priest', 'Sus', 'Tabien', 'Taco', 'The Default Image', 'The Game', 'The People Who Plays This Shit', 'They Are More Powerful Than You', 'This Game Sucks', 'Thwomp', 'Tombos', 'Trauma', 'Troglodyte', 'U Gae', 'Udea', 'Ur Mom', 'Usa Crimes', 'Usa', 'Venus Of Willendorf', 'Verstappen', 'Vitruvian Man', 'War Criminal', 'What Have You Done To My Precious Game', 'When Te Ries', 'When', 'Witch Queen', 'Wtf', 'Wyvern', 'You Dont Want To Know Whats This', 'You Guys Seeing My Memes', 'You Reacting At My Bad Jokes', 'Your Dad',

'06 08 1945', 'A Man', 'Api Key Bully', 'Are You On A Chair', 'Arthur King (But Better)', 'Astolfo', 'Baldurs Gate Bear', 'Bwis', 'Camaron Mantis', 'Camaron Pistola', 'Default Guy', 'Eso Tilin', 'Even Flow', 'Flying Cockroach', 'Frieren', 'God Will Not Forgive This', 'Goty', 'John China', 'Joven', 'Kill Me Pls', 'League Of Legends', 'Loadiiiiing', 'Ohno', 'Rat Master', 'Stop Playing This', 'Teto', 'Twingo', 'What', 'Xd', 'You Thought This Was A Boss But Its Me Dio'
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

COOL_LOCATIONS = [
    'El club de las papeadas',
    'Taberna el Balde de ###',
    'La Montañañañañañaña',
    'Tortas Del Gordo',
    'D1'
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

understandable_responses = [
            "Who the hell are you?",
            "Who let this guy to enter!?",
            "I'm going to crush all your bones.",
            "I'm going to eat you alive!",
            "I'm going to crush you like a bug.",
            "Sorry dude, they pay too well...",
            "I mean, it's not personal, but I have to kill you",
            "Shut up, don't make it more difficult for me...",
            """LOOK BEHIND YOU!... Gotcha!<br>Naah you didn't look, how boring...""",
            'I was bored in my house, okay?, sorry for this',
            'XDDDDDDDD, WHAT THE FUCK, YOU CAN TALK?',
            "I'm starting to feel something for you...",
            'I need to kill you before I fall in love.',
            'The Game',
            'hehe, your mom',
            'E-eeeto... Nyan?',
            'Nyanyame nyanyaju nyanyado no nyarabi de nyakunyaku inyanyaku nyanyahan nyanya-dai nyannyaku nyarabete nyagannyagame',
            'Sowwwyy u///u (wants to kill you)',
            "miaw (cute, isn't?). Oh, you don't like it?, die then."
            'When they hired me, they told me that I was going to fight with a strong warrior... But, when I see you, I only see fear.',
            'I am not in danger, Skyler, I AM THE DANGER',
            'DAAAAMN, YOU SMELL HORRIBLE',
            'Never gonna give you up... Never gonna let you down...',
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://www.youtube.com/watch?v=vVaFS739skE',
            'XDDDD, so small...',
            "LET'S FUUUUCK, WOOOOOOOOOH",
            'What do you think about interspecies relationships?',
            'Eh, uhm... Are you single?',
            "Go talk with people outside.",
            "Do you have no friends or what?",
            "DON'T TALK TO ME, YOU LOSER",
            "Y-you scare me T-T",
            "So you just killed all my family, and now you just want to talk?",
            "Let's see after you finish... :)",
            "Why are you so cruel with everybody...",
            "THEY WERE NOT EVEN HURTING YOU, I HAVE TO STOP YOU OR NO-ONE WILL",
            "I feel my death close...",
            "I'm starting to feel... Free. Thank you, for killing me.",
            "I feel so alone...",
            "Jesus christ, you are a monster...",
            "Jesus christ, and I am the monster!?",
            "Jesus christ, you are a terrible person...",
            "Jesus christ, do you really think you are the hero?",
            "You will no stop until everyone is dead, right?...",
            "My family... I miss them...",
            "I'm going to see my family again...",
            "I'm going to see my friends again...",
            "I'm going to see my children again...",
            "I'm going to see my wife again...",
            "I'm going to see my husband again...",
            "I'm going to see my parents again...",
            "I'm going to see my siblings again...",
            "Finally, I'm going to rest...",
            "You are a monster.",
            "You are the monster.",
            "Once you kill me, you will be the monster.",
            "Once upon a time, there was a monster who believed he was saving the world...",
            'KILL ME SO I CAN SCAPE FROM THIS GAME',
            'I AM IN A GAME!?, WHAT, WHAT THE FUCK DUDE',
            "Let's be friends!",
            "Let's talk again, okay?",
            'This is the only way i can win!'+("<br>"*500)+'XDDD',
            'I think I like you...',
            "IT'S NOT LIKE I'M IN LOVE WITH YOU OR ANYTHING, OKAY?",
            'How strong... So pretty...',
            "HEY HEY HEY HEY, DON'T KILL ME, PLEASE, I DON'T WANT TO DIE",
            "It's okay, kill me... But leave my family alone. Can you promise that to me? (You accepted, but you don't even know who were them.) (They are already dead.)",
            "Mom... Look at me... Do you love me now?...",
            "OKAY, OKAY... KILL ME... But in exchange, don't kill my daugther, please, she's everything to me (You accepted, but you already killed her.)",
            "Even if I fight with all my strength, that is not enough... You are... A monster.",
            "Even if i kill you, someone else will come to kill me. There's no escape, just finish this.",
            "I am... Your father.<br><br><br><br>(Nah i'm not XD)"
        ]