from django.db import models

# Create your models here.

# for default, the characters and monsters use their bare hands 
class Weapon(models.Model):
    id = models.AutoField(primary_key=True) # added here to be seen in the __str__ 
    # if the weapon is going to be modified, then we'll need to create a new one 
    # to not modify that weapon template. Set is_template to False
    is_template = models.BooleanField(default=False) 
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
    # Anyways... It could be useful in the future.
    @classmethod
    def create_non_template_weapon(cls):
        default_weapon = cls.objects.create()
        return default_weapon
    
    @classmethod
    def get_default_weapon(cls, entity_class: str = 'Warrior'):
        #default_weapon_name = DEFAULT_WEAPON_PER_CLASS[entity_class]
        default_weapon, was_created = cls.objects.get_or_create(name='DEFAULT', is_template=True)
        return default_weapon

    def __str__(self):
        str_is_ranged = 'Ranged' if self.is_ranged else 'Melee'
        str_is_template = 'UNIQUE' if self.is_template else 'TEMPLATE'
        return f'({self.id}) WEAPON, {str_is_template}, {self.name}, {str_is_ranged}, {self.weapon_type}, {self.damage_type}, {self.damage}'


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

    '''
    # If weapon doesn't exist, it creates a new one and assigns it to the character's weapon
    def save(self, *args, **kwargs):
        if not self.weapon:
            self.weapon = Weapon.objects.create()
        super().save(*args, **kwargs)
    '''

    # If weapon doesnt exist, it selects a default weapon and assigns it to the character's weapon
    def save(self, *args, **kwargs):
        if not self.weapon:
            self.weapon = Weapon.get_default_weapon()
        super().save(*args, **kwargs)


    # return 'PLAYABLE, '+self.name+', '+self.character_race+', '+self.character_class
    def __str__(self):
        str_is_playable = 'PLAYABLE' if self.is_playable else 'NPC'
        return f'({self.id}) {str_is_playable}, {self.name}, {self.character_race} {self.character_class}, HP: {self.health}, Level: {self.level}, Weapon: [{self.weapon}]'


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
    
    '''
    # If weapon doesn't exist, it creates a new one and assigns it to the monster's weapon
    def save(self, *args, **kwargs):
        if not self.weapon:
            self.weapon = Weapon.objects.create()
        super().save(*args, **kwargs)
    '''

    # If weapon doesnt exist, it selects a default weapon and assigns it to the monsters's weapon
    def save(self, *args, **kwargs):
        if not self.weapon:
            self.weapon = Weapon.get_default_weapon()
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