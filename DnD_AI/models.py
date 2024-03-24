from django.db import models
from .default import *
import copy  # to level_up the weapon

# Create your models here.


# for default, the characters and monsters use their bare hands 
class Weapon(models.Model):
    """
    Represents a weapon in the game.

    Attributes:
    - id (AutoField): The unique identifier of the weapon.
    - is_template (BooleanField): Indicates if the weapon is a template or a unique instance.
    - name (CharField): The name of the weapon.
    - is_ranged (BooleanField): Indicates if the weapon is ranged or melee.
    - weapon_type (CharField): The type of the weapon.
    - damage_type (CharField): The type of damage the weapon deals.
    - physical_description (CharField): A description of the physical appearance of the weapon.
    - image (ImageField): An image of the weapon.
    - damage (IntegerField): The amount of damage the weapon deals.
    - range (IntegerField): The range of the weapon.
    - range_level_points (IntegerField): The number of level points that increase the range of the weapon.
    - durability (IntegerField): The durability of the weapon.
    - level (IntegerField): The level of the weapon.
    """

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
    damage          = models.IntegerField(default=6)
    range           = models.IntegerField(default=1)
    range_level_points = models.IntegerField(default=0)   # only for ranged weapons. 3 range level ups -> range +1
    durability      = models.IntegerField(default=100)
    level           = models.IntegerField(default=0)


    def __str__(self):
        str_is_ranged = 'Ranged' if self.is_ranged else 'Melee'
        str_is_template = 'TEMPLATE' if self.is_template else 'UNIQUE'
        str_level = f'+{self.level}' if self.level != 0 else ''
        return f'[{self.id}] WEAPON, {str_is_template}, {self.name}{str_level}, {str_is_ranged}, {self.weapon_type}, {self.damage_type}, {self.damage}'


def get_default_weapon(weapon_name:str = None, entity_class:str = 'Warrior', entity:str = 'Character'):
    """
    Returns the default weapon for a given entity.

    Parameters:
    - weapon_name (str): The name of the weapon. If None, the default weapon for the entity class will be returned.
    - entity_class (str): The class of the entity.
    - entity (str): The type of the entity (Character or Monster).

    Returns:
    - template_weapon (Weapon): The default weapon for the entity.
    """
    if weapon_name == None or weapon_name not in DEFAULT_WEAPON_STATS:
        try:
            weapon_name = DEFAULT_WEAPON_PER_CLASS[entity_class]
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
    # if the migrations are not running, comment all this function lines and return None, 
    # then delete the database and all migrations (except __init__) and 
    # run createmigrations, then migrate.


def get_bare_hands():
    """
    Returns the default weapon for bare hands.

    Returns:
    - template_weapon (Weapon): The default weapon for bare hands.
    """
    return get_default_weapon(weapon_name='Bare hands')
    '''
    return None'''
    # if the migrations are not running, comment all this function lines and return None, 
    # then delete the database and all migrations (except __init__) and 
    # run createmigrations, then migrate.


def get_default_icon(entity_race:str) -> str:
    if entity_race in DEFAULT_WEAPON_PER_CLASS.keys():
        return f'entity/icons/default/{entity_race.lower().replace(' ', '')}.png'
    else:
        return 'entity/images/default.png'


class Character(models.Model):
    """
    Represents a character in the game.

    Attributes:
    - id (AutoField): The unique identifier of the character.
    - is_playable (BooleanField): Indicates if the character is playable or an NPC.
    - name (CharField): The name of the character.
    - story (CharField): The story of the character.
    - physical_description (CharField): A description of the physical appearance of the character.
    - image (ImageField): An image of the character.
    - character_race (CharField): The race of the character.
    - character_class (CharField): The class of the character.
    - weapon (ForeignKey): The weapon of the character.
    - got_initial_weapon (BooleanField): Indicates if the character has obtained their initial weapon.
    - max_health (IntegerField): The maximum health of the character.
    - health (IntegerField): The current health of the character.
    - strength (IntegerField): The strength of the character.
    - intelligence (IntegerField): The intelligence of the character.
    - recursiveness (IntegerField): The recursiveness of the character.
    - dexterity (IntegerField): The dexterity of the character.
    - physical_resistance (IntegerField): The physical resistance of the character.
    - magical_resistance (IntegerField): The magical resistance of the character.
    - constitution (IntegerField): The constitution of the character.
    - level (IntegerField): The level of the character.
    - exp (IntegerField): The experience points of the character.
    - exp_top (IntegerField): The experience points required to level up.
    - x (IntegerField): The x-coordinate of the character.
    - y (IntegerField): The y-coordinate of the character.
    - icon (ImageField): An icon representing the character.
    """

    id          = models.AutoField(primary_key=True) # added here to be seen in the __str__ 
    is_playable = models.BooleanField(default=True) # playable or NPC
    name        = models.CharField(max_length=30, null=True, blank=True)
    story       = models.CharField(max_length=1000, default="DEFAULT_STORY")

    physical_description    = models.CharField(max_length=200, default="Masculine, tall, white skin, black clothes")
    image                   = models.ImageField(upload_to='entity/images/', null=True, blank=True)

    # Character description 
    # We will see if the class and race can add a bonus to some statistics
    # class was a reserved word.
    character_race  = models.CharField(max_length=30, default="Human")
    character_class = models.CharField(max_length=30, null=True, blank=True) 

    weapon = models.ForeignKey(Weapon, on_delete=models.SET(get_bare_hands), null=True, blank=True)
    got_initial_weapon = models.BooleanField(default=False)
    
    # Stats
    max_health      = models.IntegerField(default=100)  # health limit
    health          = models.IntegerField(null=True, blank=True)  # if reaches 0, the character dies
    strength        = models.IntegerField(default=10)   # plus to physical attacks
    intelligence    = models.IntegerField(default=10)   # plus to magical attacks
    recursiveness   = models.IntegerField(default=10)   # plus to item attacks
    dexterity       = models.IntegerField(default=10)   # decides who attacks first
    physical_resistance = models.IntegerField(default=10)   # reduces physical damage
    magical_resistance  = models.IntegerField(default=10)   # reduces magical damage
    constitution        = models.IntegerField(default=10)   # reduces item damage

    level   = models.IntegerField(default=0)
    exp     = models.IntegerField(default=0)
    exp_top = models.IntegerField(default=30)  # exp until level_up

    x       = models.IntegerField(default=0)
    y       = models.IntegerField(default=0)
    icon    = models.ImageField(upload_to="entity/icons/", null=True, blank=True)

    inventory = models.TextField(default=str({'gold': 10, 'health potion': 2}))  # the inventory is a dictionary, but it's saved as a string

    def get_inventory(self) -> dict:
        ''' returns the inventory as a dictionary '''
        inventory_dict = {}
        try:
            inventory_dict = eval(self.inventory)
        except:
            pass
        return inventory_dict
    
    def add_to_inventory(self, item:str, amount:int = 1) -> bool:
        ''' adds an item to the inventory, returns if was succesful '''
        inventory_dict = self.get_inventory()
        if item in inventory_dict:
            inventory_dict[item] += amount
        else:
            inventory_dict[item] = amount
        self.inventory = str(inventory_dict)
        self.save()
        return True
    
    def use_from_inventory(self, item:str, amount:int = 1) -> bool:
        ''' removes an item from the inventory, returns if was succesful '''
        inventory_dict = self.get_inventory()
        if item in inventory_dict:
            inventory_dict[item] -= amount
            if inventory_dict[item] <= 0:
                del inventory_dict[item]
            self.inventory = str(inventory_dict)
            self.save()
            return True
        return False

    def level_up_stat(self, stat:str = 'max_health'):
        ''' levels up the character, you can choose the stat to increace \n
        returns if was succesful '''
        stat = stat.lower().replace('_', ' ')
        if stat in ['max health', 'maxhealth', 'health', 'hp']:
            self.max_health += 10
        elif stat in ['str', 'strength']:
            self.strength += 1
        elif stat in ['int', 'intelligence']:
            self.intelligence += 1
        elif stat in ['dex', 'dexterity']:
            self.dexterity += 1
        elif stat in ['phys res', 'physical resistance']:
            self.physical_resistance += 1
        elif stat in ['mag res', 'magical resistance']:
            self.magical_resistance += 1
        elif stat in ['con', 'constitution']:
            self.constitution += 1

        self.level      += 1                        # the level increaces one point
        self.exp        -= self.exp_top             # the experience reduces the top passed
        self.exp_top    += int(self.exp_top*0.2)    # the top increaces by a function
        self.health     = self.max_health           # the health recovers to the max
        self.save()
        return True   # successful
        

    def level_up_weapon(self, new_name:str = None, stat:str = 'damage'):
        ''' levels up the weapon of the character, the damage will be increaced if you choose it. \n
        if is a ranged weapon, you can also level up the range, but with a five points accumulation system. \n
        returns the leveled up weapon, but now the character has it equipped  .
        '''
        leveled_weapon = copy.deepcopy(self.weapon)  # I create a copy of that weapon

        leveled_weapon.is_template = False  # Change is_template to false, now it's a unique weapon
        leveled_weapon.level += 1
        
        if stat == 'damage':
            leveled_weapon.damage += 1

        # for ranged weapons, you can also level up the range, but it's a point accumulation system.
        # if you reach five points (range_level_points), then the range is leveled up.
        # else, you only get one more point
        elif stat == 'range':
            if leveled_weapon.is_ranged:
                if leveled_weapon.range_level_points <= 5:
                    leveled_weapon.range_level_points = 0
                    leveled_weapon.range += 1
                else:
                    leveled_weapon.range_level_points += 1
            else:
                leveled_weapon.damage += 1  # dude, that's just only for ranged weapons

        
        # if a new name is sent, that will be the new name of the weapon. 
        if new_name:
            leveled_weapon.name = new_name
        
        leveled_weapon.save()
        self.weapon = leveled_weapon                # now the character has the leveled up weapon equipped
        self.level      += 1                        # the level increaces one point
        self.exp        -= self.exp_top             # the experience reduces the top passed
        self.exp_top    += int(self.exp_top*0.2)    # the top increaces by a function
        self.health     = self.max_health           # the health recovers to the max
        self.save()

        return leveled_weapon  # if you want to easily show the weapon or something like that
    
    def disarm(self) -> bool:
        ''' disarms the character, his weapon will be "Bare hands" \n
        returns if was succesful '''
        self.weapon = get_bare_hands()
        self.save()
        return True  # if was succesful
    
    def kill(self) -> bool:
        ''' deletes the character '''
        self.delete()
        return True  # if was succesful

    def save(self, *args, **kwargs):
        if not self.character_class:
            self.character_class = self.character_race if self.character_race != 'Human' else 'Warrior'

        if not self.icon and not self.image:
            self.icon = get_default_icon(self.character_race)

        if self.icon and not self.image:
            self.image = self.icon

        if self.image and not self.icon:
            self.icon = self.image

        if not self.weapon:
            if not self.got_initial_weapon:
                self.weapon = get_default_weapon(entity_class=self.character_class, entity='Character')
                self.got_initial_weapon = True
            else:
                self.weapon = get_bare_hands()

        if not self.name:
            if self.character_race == 'Human':
                self.name = self.character_class+' '+get_random_name()
            else:
                self.name = self.character_race+' '+get_random_name()
        
        if self.health == None:
            self.health = self.max_health

        super().save(*args, **kwargs)

    def __str__(self):
        str_is_playable = 'PLAYER' if self.is_playable else 'NPC'
        raceclass = f'{self.character_race} {self.character_class}' if self.character_race != self.character_class else self.character_class
        return f'[{self.id}] ({self.x},{self.y}) {str_is_playable}, {self.name}, {raceclass}, HP: {self.health}, Level: {self.level}, Weapon: [{self.weapon}]'


class Monster(models.Model):
    """
    Represents a monster in the game.

    Attributes:
    - id (AutoField): The unique identifier of the monster.
    - name (CharField): The name of the monster.
    - is_key_for_campaign (BooleanField): Indicates if the monster is a key monster for the campaign.
    - monster_race (CharField): The race of the monster.
    - monster_class (CharField): The class of the monster.
    - physical_description (CharField): A description of the physical appearance of the monster.
    - weapon (ForeignKey): The weapon of the monster.
    - got_initial_weapon (BooleanField): Indicates if the monster has obtained their initial weapon.
    - max_health (IntegerField): The maximum health of the monster.
    - health (IntegerField): The current health of the monster.
    - strength (IntegerField): The strength of the monster.
    - intelligence (IntegerField): The intelligence of the monster.
    - recursiveness (IntegerField): The recursiveness of the monster.
    - dexterity (IntegerField): The dexterity of the monster.
    - physical_resistance (IntegerField): The physical resistance of the monster.
    - magical_resistance (IntegerField): The magical resistance of the monster.
    - constitution (IntegerField): The constitution of the monster.
    - exp_drop (IntegerField): The amount of experience points the monster drops.
    - x (IntegerField): The x-coordinate of the monster.
    - y (IntegerField): The y-coordinate of the monster.
    - icon (ImageField): An icon representing the monster.
    """

    id      = models.AutoField(primary_key=True) # added here to be seen in the __str__ 
    name    = models.CharField(max_length=30, null=True, blank=True)
    is_key  = models.BooleanField(default=False)
    is_boss = models.BooleanField(default=False)

    monster_race  = models.CharField(max_length=30, default="Goblin")
    monster_class = models.CharField(max_length=30, null=True, blank=True)

    physical_description = models.CharField(max_length=100, default="Green goblin, small, with no weapon")

    weapon = models.ForeignKey(Weapon, on_delete=models.SET(get_bare_hands), null=True, blank=True)
    got_initial_weapon = models.BooleanField(default=False)

    # Stats
    max_health      = models.IntegerField(default=100)  # health limit
    health          = models.IntegerField(null=True, blank=True)  # if reaches 0, the monster dies
    strength        = models.IntegerField(default=10)   # plus to physical attacks
    intelligence    = models.IntegerField(default=10)   # plus to magical attacks
    recursiveness   = models.IntegerField(default=10)   # plus to item attacks
    dexterity       = models.IntegerField(default=10)   # decides who attacks first
    physical_resistance = models.IntegerField(default=10)   # reduces physical damage
    magical_resistance  = models.IntegerField(default=10)   # reduces magical damage
    constitution        = models.IntegerField(default=10)   # reduces item damage

    exp_drop = models.IntegerField(default=10)

    x       = models.IntegerField(default=2)
    y       = models.IntegerField(default=2)
    icon    = models.ImageField(upload_to="entity/icons/", null=True, blank=True)

    inventory = models.TextField(default=str({'gold': 10}))  # the inventory is a dictionary, but it's saved as a string

    def get_inventory(self) -> dict:
        ''' returns the inventory as a dictionary '''
        inventory_dict = {}
        try:
            inventory_dict = eval(self.inventory)
        except:
            pass
        return inventory_dict
    
    def add_to_inventory(self, item:str, amount:int = 1) -> bool:
        ''' adds an item to the inventory, returns if was succesful '''
        inventory_dict = self.get_inventory()
        if item in inventory_dict:
            inventory_dict[item] += amount
        else:
            inventory_dict[item] = amount
        self.inventory = str(inventory_dict)
        self.save()
        return True

    def disarm(self) -> bool:
        ''' disarms the monster, his weapon will be "Bare hands"\n
        returns if was succesful '''
        self.weapon = get_bare_hands()
        self.save()
        return True  # if was succesful
    
    def kill(self) -> tuple[bool, bool]:
        ''' deletes the monster \n
        returns a tuple. (if was succesful , if was a key monster)'''
        was_key = True if self.is_key else False
        self.delete()
        return True, was_key  
    
    def save(self, *args, **kwargs):
        if not self.monster_class:
            self.monster_class = self.monster_race

        if not self.icon:
            self.icon = get_default_icon(self.monster_race)

        if not self.name:
            self.name = self.monster_race+' '+get_random_name()

        if self.health == None:
            self.health = self.max_health

        if not self.weapon:
            if not self.got_initial_weapon:
                self.weapon = get_default_weapon(entity_class=self.monster_class, entity='Monster')
                self.got_initial_weapon = True
            else:
                self.weapon = get_bare_hands()
        super().save(*args, **kwargs)

    def __str__(self):
        raceclass = f'{self.monster_race} {self.monster_class}' if self.monster_race != self.monster_class else self.monster_class
        key_str = 'KEY ' if self.is_key else ''
        boss_str = 'BOSS' if self.is_boss else 'MONSTER'
        return f'[{self.id}] ({self.x},{self.y}) {key_str}{boss_str}, {self.name}, {raceclass}, [{self.weapon}]'
    

class Chest(models.Model):
    """
    Represents a chest in the game.

    Attributes:
    - id (AutoField): The unique identifier of the chest.
    - x (IntegerField): The x-coordinate of the chest.
    - y (IntegerField): The y-coordinate of the chest.
    - is_open (BooleanField): Indicates if the chest is open.
    - inventory (TextField): The inventory of the chest.
    """

    id = models.AutoField(primary_key=True)
    is_key = models.BooleanField(default=False)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    inventory = models.TextField(default=str({'gold': 10}))

    def get_inventory(self) -> dict:
        ''' returns the inventory as a dictionary '''
        inventory_dict = {}
        try:
            inventory_dict = eval(self.inventory)
        except:
            pass
        return inventory_dict

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'[{self.id}] ({self.x},{self.y}) CHEST, {self.x}, {self.y}, {self.inventory}'

    

class History(models.Model):
    """
    Represents the history of the game.

    Attributes:
    - id (AutoField): The unique identifier of the history.
    - author (CharField): The author of the history.
    - text (CharField): The text of the history.
    - color (CharField): The color of the history.
    - date (DateTimeField): The date of the history.
    """

    id = models.AutoField(primary_key=True)
    is_key = models.BooleanField(default=False)
    is_image = models.BooleanField(default=False)
    author = models.CharField(max_length=50, default="SYSTEM")
    text = models.CharField(max_length=2000, default="Hi (Default message)")
    color = models.CharField(max_length=10, default="black")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.id}] ({self.date}) {self.author} ({self.color}): {self.text}'


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
            (or completing quests and by using items, in possible future features). 
            When the entity reaches a new level, his exp is reset to 0.

    COORDINATES DESCRIPTIONS
x:      the entity's position in the x-axis of the map
y:      the entity's position in the y-axis of the map
icon:   in a map, this small squared image can be seen to represent that entity

    WEAPON DESCRIPTIONS
is_ranged:      a weapon can be melee or ranged, so it's a bool.
weapon_type:    there's plenty of weapon types, as swords, axes, bows, knives... 
                (In future releases features, certain races could have a better 
                handle of certain weapon types)
damage_type:    That weapon can affect the enemies in different ways, as physical or magical ones.

    CHARACTER DESCRIPTIONS
got_initial_weapon:     Indicates if the character has obtained their initial weapon.

    MONSTER DESCRIPTIONS
is_key_for_campaign:    Indicates if the monster is a key monster for the campaign.
exp_drop:               The amount of experience points the monster drops.
'''