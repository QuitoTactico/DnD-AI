from django.db import models
from .default import *

# Create your models here.


# for default, the characters and monsters use their bare hands 
class Weapon(models.Model):
    id = models.AutoField(primary_key=True) # added here to be seen in the __str__ 
    # if the weapon is going to be modified, then we'll need to create a new one 
    # to not modify that weapon template. Set is_template to False
    is_template = models.BooleanField(default=False) 
    name        = models.CharField(max_length=30, default="Bare hands")
    is_ranged   = models.BooleanField(default=False)
    weapon_type = models.CharField(max_length=15, default="Body part") # type was reserved
    damage_type = models.CharField(max_length=15, default="Physical")

    physical_description = models.CharField(max_length=100, default="It's using his own hands")
    image       = models.ImageField(upload_to='weapon/images/', default='weapon/images/default/bare_hands.png')

    # Statistics
    damage      = models.IntegerField(default=6)
    range       = models.IntegerField(default=1)
    durability  = models.IntegerField(default=100)

    def __str__(self):
        str_is_ranged = 'Ranged' if self.is_ranged else 'Melee'
        str_is_template = 'TEMPLATE' if self.is_template else 'UNIQUE'
        return f'({self.id}) WEAPON, {str_is_template}, {self.name}, {str_is_ranged}, {self.weapon_type}, {self.damage_type}, {self.damage}'


# If the entity doesn't have a weapon, it gets the default weapon for its class
def get_default_weapon_by_class(entity_class: str = 'Warrior', entity: str = 'Character'):
    
    try:
        if entity == 'Character':
            weapon_name = DEFAULT_WEAPON_PER_CHARACTER_CLASS[entity_class]
        else:
            weapon_name = DEFAULT_WEAPON_PER_MONSTER_CLASS[entity_class]
    except:
        weapon_name = 'Sword'

    template_weapon, was_created = Weapon.objects.get_or_create(
            name=weapon_name, 
            is_template=True, 
            damage=DEFAULT_WEAPON_STATS[weapon_name]['damage'], 
            range=DEFAULT_WEAPON_STATS[weapon_name]['range'], 
            image=DEFAULT_WEAPON_STATS[weapon_name]['image'],
            is_ranged=DEFAULT_WEAPON_STATS[weapon_name]['is_ranged'],
            physical_description=DEFAULT_WEAPON_STATS[weapon_name]['physical_description'],
            damage_type=DEFAULT_WEAPON_STATS[weapon_name]['damage_type'],
            weapon_type=DEFAULT_WEAPON_STATS[weapon_name]['weapon_type']
    )
    return template_weapon
    '''
    return None'''
    # if something happens, comment all this function lines and return None


def get_default_weapon_by_name(weapon_name: str = 'Bare hands'):
    
    template_weapon, was_created = Weapon.objects.get_or_create(
            name=weapon_name, 
            is_template=True, 
            damage=DEFAULT_WEAPON_STATS[weapon_name]['damage'], 
            range=DEFAULT_WEAPON_STATS[weapon_name]['range'], 
            image=DEFAULT_WEAPON_STATS[weapon_name]['image'],
            is_ranged=DEFAULT_WEAPON_STATS[weapon_name]['is_ranged'],
            physical_description=DEFAULT_WEAPON_STATS[weapon_name]['physical_description'],
            damage_type=DEFAULT_WEAPON_STATS[weapon_name]['damage_type'],
            weapon_type=DEFAULT_WEAPON_STATS[weapon_name]['weapon_type']
    )
    return template_weapon
    '''
    return None'''
    # if something happens, comment all this function lines and return None


# for default, the character is a simple playable human
class Character(models.Model):
    id          = models.AutoField(primary_key=True) # added here to be seen in the __str__ 
    is_playable = models.BooleanField(default=True) # playable or NPC
    name        = models.CharField(max_length=30, default="DEFAULT_CHARACTER")
    story       = models.CharField(max_length=1000, default="DEFAULT_STORY")

    physical_description    = models.CharField(max_length=200, default="Masculine, tall, white skin, black clothes")
    image                   = models.ImageField(upload_to='entity/images/', default='entity/images/default.png')

    # Character description 
    # We will see if the class and race can add a bonus to some statistics
    # class was a reserved word.
    character_race  = models.CharField(max_length=30, default="Human")
    character_class = models.CharField(max_length=30, null=True, blank=True) 

    # Weapon
    # A character or monster always has a weapon, including his bare hands.
    # weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE, default=Weapon.get_default_weapon())
    # weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE, default=Weapon.objects.create())
    weapon = models.ForeignKey(Weapon, on_delete=models.SET(get_default_weapon_by_name), null=True, blank=True)
    got_initial_weapon = models.BooleanField(default=False)
    

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
    constitution        = models.IntegerField(default=10)

    # Progress
    level   = models.IntegerField(default=0)
    exp     = models.IntegerField(default=0)

    # Coordinates
    x       = models.IntegerField(default=0)
    y       = models.IntegerField(default=0)
    icon    = models.ImageField(upload_to="entity/icons/", default='entity/icons/default.png')

    # Default values for fields which depends on other fields values.
    def save(self, *args, **kwargs):
        # sometimes the race itself is the class. If the player doesn't choose a class, his class will be the race.
        # but class "human" is kinda odd, so warrior is the default class for humans.
        if not self.character_class:
            self.character_class = self.character_race if self.character_race != 'Human' else 'Warrior'

        # if the character doesn't have a weapon while it's created or saved...
        if not self.weapon:
            # the character gets his class' initial weapon
            if not self.got_initial_weapon:
                self.weapon = get_default_weapon_by_class(entity_class=self.character_class, entity='Character')
                self.got_initial_weapon = True
            else: # if he looses it, he gets his bare hands
                self.weapon = get_default_weapon_by_name()     # bare hands
        super().save(*args, **kwargs)


    # return 'PLAYABLE, '+self.name+', '+self.character_race+', '+self.character_class
    def __str__(self):
        str_is_playable = 'PLAYABLE' if self.is_playable else 'NPC'
        return f'({self.id}) {str_is_playable}, {self.name}, {self.character_race} {self.character_class}, HP: {self.health}, Level: {self.level}, Weapon: [{self.weapon}]'


# for default, a monster is a simple goblin
class Monster(models.Model):
    id      = models.AutoField(primary_key=True) # added here to be seen in the __str__ 
    name    = models.CharField(max_length=30, default="DEFAULT_MONSTER")
    is_key_for_campaign = models.BooleanField(default=False) # if it's a key monster for the campaign, it's a boss

    # Monster description 
    # We will see if the class and race can add a bonus to some statistics
    # class was a reserved word. 
    monster_race  = models.CharField(max_length=30, default="Goblin")
    monster_class = models.CharField(max_length=30, null=True, blank=True) # maybe blank=True would be better
                                                                           # edit: it was better XD

    physical_description = models.CharField(max_length=100, default="Green goblin, small, with no weapon")

    # Weapon
    # A character or monster always has a weapon, including his bare hands.
    # weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    weapon = models.ForeignKey(Weapon, on_delete=models.SET(get_default_weapon_by_name), null=True, blank=True)
    got_initial_weapon = models.BooleanField(default=False)

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
    constitution        = models.IntegerField(default=10)

    # For character progress
    exp_drop = models.IntegerField(default=10)

    # Coordinates
    x       = models.IntegerField(default=2)
    y       = models.IntegerField(default=2)
    icon    = models.ImageField(upload_to="entity/icons/", default='entity/icons/default.png')
    
    # Default values for fields which depends on other fields values.
    def save(self, *args, **kwargs):
        # sometimes the race itself is a race for the monsters, so the class will be the the race if it's not set.
        if not self.monster_class:
            self.monster_class = self.monster_race

        # if the monster doesn't have a weapon while it's created...
        if not self.weapon:
            # it gets the default weapon for its class
            if not self.got_initial_weapon:
                self.weapon = get_default_weapon_by_class(entity_class=self.monster_class, entity='Monster')
                self.got_initial_weapon = True
            else:  # if he looses it, he gets his bare hands
                self.weapon = get_default_weapon_by_name()     # bare hands
        super().save(*args, **kwargs)

    def __str__(self):
        return f'({self.id}) MONSTER, {self.name}, {self.monster_race}, {self.monster_class}, [{self.weapon}]'


# -----------------------------------------------------

''' DESCRIPTIONS:

    BASICS
is_playable:    Is the character playable for the user, or it's an NPC like a merchant?
name:           the entity's name
story:          the character itself can own a proper story.
physical_description: Useful for prompts.
image:          the entity's image, to be seen on the character's interface, above the statistics.
race:           In rpg games, there's plenty of anthropomorphycal species to choose, not only humans.
class:          Every entity (Character or Monster) has a "role" among their group, as warriors, magicians, archers...

    STATS DESCRIPTIONS
max_health:     the entity begins his health in this state, and can't surpass it.
health:         Can be reduced by attacks, and restored by skills and items used from the inventory. 
                The entity dies if his health reaches 0 (or below). 
                If the player reaches a new level, his health recovers to the max_health state.
strength:       Damage points added to physical attacks
intelligence:   damage points added to magical attacks
dexterity:      defines who attacks/acts first in a battle
physical_resistance:    damage points reduced when the entity receives a physical attack.
magical_resistance:     damage points reduced when the entity receives a magical attack.
constitution:   damage points reduced when an entity receives an effect or a damaging state, like venom or poison. Effects/States resistance.

    PROGRESS DESCRIPTIONS
level:      the entity's level. The entity can level up by gaining experience points (exp). 
            The exp needed to reach a new level is calculated by a formula, 
            and it's increased with every new level.
exp:        the entity's experience points. The entity gains exp by defeating monsters, 
            (or completing quests and by using items, in posible future features). 
            When the entity reaches a new level, his exp is reset to 0.

    COORDINATES DESCRIPTIONS
x:      the entity's position in the x axis of the map
y:      the entity's position in the y axis of the map
icon:   in a map, this small squared image can be seen to represent that entity

    WEAPON DESCRIPTIONS
is_ranged:      a weapon can be melee or ranged, so it's a bool.
weapon_type:    there's plenty of weapon types, as swords, axes, bows, knifes... 
                (In future releases features, certain races could have a better 
                handle of certain weapon types)
damage_type:    That weapon can affect the enemies in different ways, as physical or magical ones.
'''