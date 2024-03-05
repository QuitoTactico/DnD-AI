from .models import *
from random import randint
from .default import *

def roll_dice(): 
    return randint(1, 20)
            