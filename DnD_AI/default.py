#import database of common names
from faker import Faker

fake = Faker()

def get_random_name():
    return fake.first_name()

DEFAULT_WEAPON_PER_CLASS = {
    'Alchemist': 'Dagger',
    'Archer': 'Long Bow',
    'Artificer': 'Dagger',
    'Assassin': 'Crossbow',
    'Barbarian': 'Axe',
    'Bard': 'Dagger',
    'Cleric': 'Mace',
    'Cowboy': 'Revolver',
    'Druid': 'Staff',
    'Dwarf': 'Warhammer',
    'Elf': 'Bow',
    'Fighter': 'Bare hands',
    'Hunter': 'Bow',
    'Knight': 'Sword',
    'Lancer': 'Spear',
    'Mage': 'Staff',
    'Monk': 'Bare hands',
    'Ninja': 'Shurikens',
    'Paladin': 'Sword',
    'Ranger': 'Bow',
    'Rogue': 'Dagger',
    'Samurai': 'Katana',
    'Tribe': 'Blowpipe',
    'Viking': 'Battleaxe',
    'Warrior': 'Sword',
    'Wizard': 'Staff',
    'Wizard': 'Staff',
}

DEFAULT_WEAPON_PER_RACE = {
    'Basilisk': 'Beast Claws',
    'Centaur': 'Bow',
    'Chimera': 'Fangs',
    'Cyclop': 'Great Warhammer',
    'Demon': 'Trident',
    'Dragon': 'Beast Claws',
    'Fairy': 'Magic Wand',
    'Ghost': 'Scythe',
    'Giant': 'Great Warhammer',
    'Goblin': 'Dagger',
    'Golem': 'Great Warhammer',
    'Harpy': 'Bow',
    'Hydra': 'Fangs',
    'Medusa': 'Sword',
    'Mermaid': 'Trident',
    'Minotaur': 'Battleaxe',
    'Orc': 'Axe',
    'Overlord': 'Great Warhammer',
    'Rat': 'Fangs',
    'Scorpion': 'Tail',
    'Skeleton': 'Sword',
    'Spider': 'Fangs',
    'Troll': 'Warhammer',
    'Unicorn': 'Horns',
    'Vampire': 'Fangs',
    'Werewolf': 'Beast Claws',
    'Wolf': 'Fangs',
    'Witch': 'Enchanted Book',
    'Zombie': 'Bare hands',
}
DEFAULT_WEAPON_PER_RACE.update(DEFAULT_WEAPON_PER_CLASS)


POSSIBLE_BOSSES = ['The Sphinx', 'Cthulhu', 'The Leviathan', 'Behemoth', 'The Kraken', 'Hades', 'Cerberus', 'GOD', 'Zeus', 'Ares', 'Thanatos', 'Megatron', 'Mr Beast', 'Lord Voldemort', 'Your Mom', 'The Devil', 'Telematica Demon', 'Diomedes Diaz', 'Makima', 'Donald Trump', 'MechaHitler', 'John Cena', 'The Rock', 'Undertaker', 'Jackie Chan', 'Megamind', 'Shrek', 'Darth Vader', 'Sauron', 'Mike Wazousky', 'The Joker', 'John Wick', 'Cristionel Messinaldo', 'Fernanfloo', 'Michael Jackson', 'PewDiePie', 'Elon Musk', 'Terminator', 'The Creators, a Malformed Three-Headed Beast Who Rules Everything and Fears Nothing', 'Yourself but Chinese', 'Hatsune Miku', 'Racism Demon', 'The Cancer', 'NekoKiller', 'Mbappe', 'Dross Rotzank', 'Doc Tops', 'El Putas de Aguadas', 'Waluigi', 'Slenderman', 'Flying Spagguetti God', 'Sonic.exe', 'Spongebob', 'Sans', 'The Game', 'Juan Carlos', 'El Pepe', 'Ete Sech', 'Tilín', 'Eminem', 'Yourself', 'Wolverine', 'Dracula', 'Link', 'The Hollow Knight', 'Moai', 'Skeleton King', 'Anubis', "Fetus"]


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