from django.db import models

# Create your models here.

# for default, the characters and monsters use their bare hands 
class Weapon(models.Model):
    id = models.AutoField(primary_key=True) # added here to be seen in the __str__ 
    name = models.CharField(max_length=30, default="His bare hands")
    is_ranged = models.BooleanField(default=False)
    weapon_type = models.CharField(max_length=15, default="Body part") # type was reserved
    damage_type = models.CharField(max_length=15, default="Physical")

    physical_description = models.CharField(max_length=100, default="It's using his hands")
    image = models.ImageField(upload_to='weapon/images/', default='weapon/images/default.png')

    # Statistics
    damage      = models.IntegerField(default=10)
    range       = models.IntegerField(default=1)
    durability  = models.IntegerField(default=100)

    # Only uses already existent weapons, if it doesn't exist then it creates it.
    # The problem is that it brings all the default weapons that exists, I only need the first one it finds.
    # Right now we are creating a new default every time a new character is created without a weapon.
    # With a modification, it says "django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet."
    # The migration does not let me delete this method, so I leave it here.
    @classmethod
    def get_default_weapon(cls):
        #default_weapon, created = cls.objects.get_or_create(name='DEFAULT')
        default_weapon = cls.objects.create()
        return default_weapon

    def __str__(self):
        if self.is_ranged:
            return f'({self.id}) WEAPON, ranged, {self.name}, {self.weapon_type}, {self.damage_type}'
        else:
            return f'({self.id}) WEAPON, melee, {self.name}, {self.weapon_type}, {self.damage_type}'


# for default, the character is a simple playable human
class Character(models.Model):
    id = models.AutoField(primary_key=True) # added here to be seen in the __str__ 
    is_playable = models.BooleanField(default=True) # playable or NPC
    name        = models.CharField(max_length=30, default="DEFAULT_CHARACTER")
    story = models.CharField(max_length=1000, default="DEFAULT_STORY")

    physical_description = models.CharField(max_length=200, default="Man, tall, white skin, black clothes")
    image = models.ImageField(upload_to='entity/images/', default='entity/images/default.png')

    # Character description 
    # We will see if the class and race can add a bonus to some statistics
    # class was a reserved word.
    character_race  = models.CharField(max_length=30, default="Human")
    character_class = models.CharField(max_length=30, default="Warrior") 

    # Weapon
    # A character or monster always has a weapon, including his bare hands.
    # weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE, default=Weapon.get_default_weapon())
    # weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE, default=Weapon.objects.create())
    weapon = models.ForeignKey(Weapon, on_delete=models.SET_NULL, null=True, blank=True)
    

    # Statistics
    max_health      = models.IntegerField(default=100)
    health          = models.IntegerField(default=100)
    #   For damage
    strength        = models.IntegerField(default=10)
    intelligence    = models.IntegerField(default=10)
    #   To act first
    dexterity       = models.IntegerField(default=10)
    #   For defense
    physical_resistance = models.IntegerField(default=10)
    magical_resistance  = models.IntegerField(default=10)
    constitution    = models.IntegerField(default=10)

    # Progress
    level   = models.IntegerField(default=0)
    exp     = models.IntegerField(default=0)

    # Coordinates
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    icon = models.ImageField(upload_to="entity/icons/", default='entity/icons/default.png')

    # If weapon doesn't exist, it creates a new one and assigns it to the character's weapon
    def save(self, *args, **kwargs):
        if not self.weapon:
            self.weapon = Weapon.objects.create()
        super().save(*args, **kwargs)

        
    # return 'PLAYABLE, '+self.name+', '+self.character_race+', '+self.character_class
    def __str__(self):
        if self.is_playable:
            return f'({self.id}) PLAYABLE, {self.name}, {self.character_race}, {self.character_class}, [{self.weapon}]'
        else:
            return f'({self.id}) NPC, {self.name}, {self.character_race}, {self.character_class}, [{self.weapon}]'


# for default, a monster is a simple goblin
class Monster(models.Model):
    id = models.AutoField(primary_key=True) # added here to be seen in the __str__ 
    name = models.CharField(max_length=30, default="DEFAULT_MONSTER")

    # Monster description 
    # We will see if the class and race can add a bonus to some statistics
    # class was a reserved word. 
    monster_race  = models.CharField(max_length=30, default="Goblin")
    monster_class = models.CharField(max_length=30, default="Warrior") # maybe blank=True would be better

    physical_description = models.CharField(max_length=100, default="Green goblin, small, with no weapon")

    # Weapon
    # A character or monster always has a weapon, including his bare hands.
    # weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    weapon = models.ForeignKey(Weapon, on_delete=models.SET_NULL, null=True, blank=True)

    # Statistics
    max_health      = models.IntegerField(default=100)
    health          = models.IntegerField(default=100)
    #   For damage
    strength        = models.IntegerField(default=10)
    intelligence    = models.IntegerField(default=10)
    #   To act first
    dexterity       = models.IntegerField(default=10)
    #   For defense
    physical_resistance = models.IntegerField(default=10)
    magical_resistance  = models.IntegerField(default=10)
    constitution    = models.IntegerField(default=10)

    # For character progress
    exp_drop = models.IntegerField(default=10)

    # Coordinates
    x = models.IntegerField(default=2)
    y = models.IntegerField(default=2)
    icon = models.ImageField(upload_to="entity/icons/", default='entity/icons/default.png')
    
    # If weapon doesn't exist, it creates a new one and assigns it to the monsters weapon
    def save(self, *args, **kwargs):
        if not self.weapon:
            self.weapon = Weapon.objects.create()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'({self.id}) MONSTER, {self.name}, {self.monster_race}, {self.monster_class}'


# -----------------------------------------------------

''' DESCRIPTIONS:

    BASICS
is_playable: Is the character playable for the user, or it's an NPC like a merchant?
name: the entity's name
story: the character itself can own a proper story.
physical_description: useful for prompts.
image: the entity's image, to be seen on the character's interface, above the statistics.
race: In rpg games, there's plenty of anthropomorphycal species to choose, not only humans.
class: Every entity (Character or Monster) has a "role" among their group, as warriors, magicians, archers...

    STATS DESCRIPTIONS
max_health: the entity begins his health in this state, and can't surpass it.
health: Can be reduced by attacks, and restored by skills and items used from the inventory. The entity dies if his health reaches 0 (or below). If the player reaches a new level, his health recovers to the max_health state.
strength: damage points added to physical attacks
intelligence: damage points added to magical attacks
dexterity: defines who attacks/acts first in a battle
physical_resistance: damage points reduced when the entity receives a physical attack.
magical_resistance: damage points reduced when the entity receives a magical attack.
constitution: damage points reduced when an entity receives an effect or a damaging state, like venom or poison. Effects/States resistance.

    PROGRESS DESCRIPTIONS
level: the entity's level. The entity can level up by gaining experience points (exp). The exp needed to reach a new level is calculated by a formula, and it's increased with every new level.
exp: the entity's experience points. The entity gains exp by defeating monsters, (or completing quests and by using items, in posible future features). When the entity reaches a new level, his exp is reset to 0.

    COORDINATES DESCRIPTIONS
x: the entity's position in the x axis of the map
y: the entity's position in the y axis of the map
icon: in a map, this small squared image can be seen to represent that entity

    WEAPON DESCRIPTIONS
is_ranged: a weapon can be melee or ranged, so it's a bool.
weapon_type: there's plenty of weapon types, as swords, axes, bows, knifes... (In future releases features, certain races could have a better handle of certain weapon types)
damage_type: That weapon can affect the enemies in different ways, as physical or magical ones.
'''

# -----------------------------------------------------

'''  AVALIABLE VALUES (AUTOGENERATED, BETA):

weapon_type: [Sword, Axe, Mace, Hammer, Spear, Bow, Crossbow, Dagger, Knife, Staff, Wand, Rod, Club, Whip, Flail, Sling, Shield, Gauntlet, Brass Knuckles, Claws, Teeth, Tail, Tentacle, Horn, Hoof, Wing, Tail, Beak, Pincers, Stinger, Spikes, Spines, Quills, Spores]

damage_type: [physical, magical]

(not exising yet) possible_weapon_effects: Acid, Poison, Venom, Fire, Ice, Lightning, Earth, Wind, Water, Light, Dark, Holy, Unholy, Arcane, Eldritch, Psychic, Sound, Force, Gravity, Time, Space, Reality, Void, Chaos, Order, Life, Death, Nature, Technology, Alchemy, Enchantment, Necromancy, Illusion, Divination, Conjuration, Evocation, Abjuration, Transmutation, Restoration, Destruction, Creation, Summoning, Binding, Banishing, Sealing, Warding, Hexing, Cursing, Blessing, Healing, Buffing, Debuffing, Disabling, Enfeebling, Empowering, Strengthening, Weakening, Fortifying, Weakening, Draining, Siphoning, Absorbing, Reflecting, Redirecting, Amplifying, Diminishing, Nullifying, Negating, Dispelling, Countering]

character_race: [Human, Elf, Dwarf, Halfling, Gnome, Orc, Goblin, Troll, Ogre, Minotaur, Centaur, Satyr, Siren, Mermaid, Dryad, Nymph, Faun, Gorgon, Cyclops, Sphinx, Chimera, Hydra, Golem, Wraith, Zombie, Skeleton, Ghost, Ghoul, Mummy, Lich, Vampire, Werewolf, Lycanthrope, Dragonborn]

character_class: [Warrior, Mage, Archer, Thief, Paladin, Cleric, Druid, Bard, Monk, Barbarian, Sorcerer, Warlock, Ranger, Rogue, Fighter, Wizard, Necromancer, Alchemist, Blacksmith, Merchant, Farmer, Fisherman, Hunter, Cook, Miner, Lumberjack, Carpenter, Tailor, Leatherworker, Jeweler, Enchanter, Herbalist, Apothecary, Scribe, Scholar, Historian, Librarian, Teacher, Student, Artist, Musician, Dancer, Actor, Entertainer, Jester, Acrobat, Tamer, Beastmaster, Summoner, Illusionist, Seer, Oracle, Diviner, Medium, Shaman, Witch, Warlord, General, Commander, Captain, Lieutenant, Sergeant, Corporal, Private, Recruit, Soldier, Guard, Knight, Squire, Page, Noble, Lord, Lady, King, Queen, Prince, Princess, Duke, Duchess, Count, Countess, Baron, Baroness, Viscount, Viscountess, Marquis, Marquise, Emperor, Empress, Highness, Majesty

monster_race: [Goblin, Orc, Troll, Ogre, Minotaur, Centaur, Satyr, Harpy, Siren, Naga, Mermaid, Dryad, Nymph, Faun, Gorgon, Cyclops, Sphinx, Chimera, Hydra, Basilisk, Manticore, Griffin, Hippogriff, Pegasus, Unicorn, Phoenix, Roc, Wyvern, Dragon, Demon, Angel, Devil, Elemental, Golem, Specter, Wraith, Zombie, Skeleton, Ghost, Ghoul, Mummy, Lich, Vampire, Werewolf, Lycanthrope, Dragonborn, Elf, Dwarf, Halfling, Gnome, Orc, Goblin, Troll, Ogre, Minotaur, Centaur, Satyr, Harpy, Siren, Naga, Mermaid, Dryad, Nymph, Faun, Gorgon, Cyclops, Sphinx, Chimera, Hydra, Basilisk, Manticore, Griffin, Hippogriff, Pegasus, Unicorn, Phoenix, Roc, Wyvern, Dragon, Demon, Angel, Devil, Elemental, Golem, Specter, Wraith, Zombie, Skeleton, Ghost, Ghoul, Mummy, Lich, Vampire, Werewolf, Lycanthrope, Dragonborn, Elf, Dwarf, Halfling, Gnome, Orc, Goblin, Troll, Ogre, Minotaur, Centaur, Satyr, Harpy, Siren, Naga, Mermaid, Dryad, Nymph, Faun, Gorgon, Cyclops, Sphinx, Chimera, Hydra, Basilisk, Manticore, Griffin, Hippogriff, Pegasus, Unicorn, Phoenix, Roc, Wyvern, Dragon, Demon, Angel, Devil, Elemental, Golem, Specter, Wraith, Zombie, Skeleton]

monster_class: (The same as character_class)


'''

# -----------------------------------------------------


''' FUTURE DEVELOPMENT:

Weapon.effects:      str    (list or dict, interpretation needed)

Character.inventory: str    (list or dict, interpretation needed)

Monster.item_drop:   str    (list or dict, interpretation needed)

Skill.name:          str
Skill.uses:          int
Skill.type:          str    (Area, point/s or line/s)
Skill.damage_type:   str    (Physical, Magic)
Skill.range:         int
Skill.coords:        str    (list, interpretation needed)

Maybe a Story or Campaign class will be needed.

'''