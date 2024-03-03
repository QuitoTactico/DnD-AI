from django.db import models

# Create your models here.

# for default, the characters and monsters use their bare hands 
class Weapon(models.Model):
    id = models.AutoField(primary_key=True) # added here to be seen in the __str__ 
    name = models.CharField(max_length=30, default="His bare hands")
    is_ranged = models.BooleanField(default=False)
    weapon_type = models.CharField(max_length=15, default="Body") # type was reserved
    damage_type = models.CharField(max_length=15, default="Physic")

    # Statistics
    damage      = models.IntegerField(default=10)
    range       = models.IntegerField(default=1)
    durability  = models.IntegerField(default=100)

    def __str__(self):
        if self.is_ranged:
            return f'({self.id}) WEAPON, RANGED, {self.name}, {self.weapon_type}, {self.damage_type}'
        else:
            return f'({self.id}) WEAPON, MELEE, {self.name}, {self.weapon_type}, {self.damage_type}'


# for default, the character is a simple playable human
class Character(models.Model):
    id = models.AutoField(primary_key=True) # added here to be seen in the __str__ 
    is_playable = models.BooleanField(default=True) # playable or NPC
    name        = models.CharField(max_length=30, default="DEFAULT_CHARACTER")
    story = models.CharField(max_length=1000, default="DEFAULT_STORY")
    image = models.ImageField(upload_to='entity/images/', default='default.png')

    # Character description 
    # We will see if the class and race can add a bonus to some statistics
    # class was a reserved word.
    character_race  = models.CharField(max_length=30, default="Human")
    character_class = models.CharField(max_length=30, default="Warrior") 

    # Weapon
    # A character or monster always has a weapon, including his bare hands.
    id_weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    #idk how to really use a foreing key in django

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
    icon = models.ImageField(upload_to="entity/icons/", default='default.png')

    # return 'PLAYABLE, '+self.name+', '+self.character_race+', '+self.character_class
    def __str__(self):
        if self.is_playable:
            return f'({self.id}) PLAYABLE, {self.name}, {self.character_race}, {self.character_class}'
        else:
            return f'({self.id}) NPC, {self.name}, {self.character_race}, {self.character_class}'


# for default, a monster is a simple goblin
class Monster(models.Model):
    id = models.AutoField(primary_key=True) # added here to be seen in the __str__ 
    name = models.CharField(max_length=30, default="DEFAULT_MONSTER")

    # Monster description 
    # We will see if the class and race can add a bonus to some statistics
    # class was a reserved word. 
    monster_race  = models.CharField(max_length=30, default="Goblin")
    monster_class = models.CharField(max_length=30, default="Warrior") # maybe blank=True would be better

    # Weapon
    # A character or monster always has a weapon, including his bare hands.
    id_weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    #idk how to really use a foreing key in django

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
    icon = models.ImageField(upload_to="entity/icons/", default='default.png')
    

    def __str__(self):
        return f'({self.id}) MONSTER, {self.name}, {self.monster_race}, {self.monster_class}'


''' DESCRIPTIONS:

    BASICS
is_playable: Is the character playable for the user, or it's an NPC like a merchant?
name: the entity's name
story: the character itself can own a proper story.
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


'''  AVALIABLE VALUES:


'''




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


'''