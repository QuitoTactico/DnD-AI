DEFAULT_WEAPON_PER_CHARACTER_CLASS = {
    'Warrior': 'Sword',
    'Elf': 'Bow',
    'Archer': 'Long Bow',
    'Assassin': 'Crossbow',
    'Tribe': 'Blowpipe',
    'Mage': 'Staff',
    'Rogue': 'Dagger',
    'Cleric': 'Mace',
    'Paladin': 'Sword',
    'Druid': 'Staff',
    'Bard': 'Dagger',
    'Monk': 'Bare hands',
    'Barbarian': 'Axe',
    'Ranger': 'Bow',
    'Fighter': 'Bare hands',
    'Wizard': 'Staff',
    'Artificer': 'Dagger',
    'Hunter': 'Bow',
    'Alchemist': 'Dagger',
    'Knight': 'Sword',
    'Samurai': 'Katana',
    'Ninja': 'Shurikens',
    'Spearr': 'Spear',
    'Dwarf': 'Warhammer',
    'Viking': 'Battleaxe',
    'Cowboy': 'Revolver',
}

DEFAULT_WEAPON_PER_MONSTER_CLASS = {
    'Dragon': 'Beast Claws',
    'Goblin': 'Dagger',
    'Orc': 'Axe',
    'Troll': 'Warhammer',
    'Skeleton': 'Sword',
    'Zombie': 'Bare hands',
    'Vampire': 'Fangs',
    'Werewolf': 'Beast Claws',
    'Ghost': 'Scythe',
    'Witch': 'Enchanted Book',
    'Demon': 'Trident',
    'Giant': 'Great Warhammer',
    'Spider': 'Fangs',
    'Scorpion': 'Tail',
    'Centaur': 'Bow',
    'Minotaur': 'Battleaxe',
    'Cyclops': 'Great Warhammer',
    'Medusa': 'Sword',
    'Siren': 'Trident',
    'Golem': 'Great Warhammer',
    'Fairy': 'Magic Wand',
    'Mermaid': 'Trident',
    'Chimera': 'Fangs',
    'Hydra': 'Fangs',
    'Unicorn': 'Horns',
    'Basilisk': 'Beast Claws',
    'Manticore': 'Tail',
    'Rat': 'Fangs',
}
DEFAULT_WEAPON_PER_MONSTER_CLASS.update(DEFAULT_WEAPON_PER_CHARACTER_CLASS)


POSSIBLE_BOSSES = ['Sphinx', 'Cthulhu', 'Leviathan', 'Behemoth', 'Kraken', 'Hades', 'Cerberus', 'God', 'Zeus', 'Ares', 'Thanatos', 'Megatron', 'Mr Beast']

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
