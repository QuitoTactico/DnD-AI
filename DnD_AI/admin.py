from django.contrib import admin
from .models import Weapon
from .models import Character
from .models import Monster
from .models import Treasure
from .models import History
from .models import Tile

# Register your models here.

admin.site.register(Weapon)
admin.site.register(Character)
admin.site.register(Monster)
admin.site.register(Treasure)
admin.site.register(History)
admin.site.register(Tile)