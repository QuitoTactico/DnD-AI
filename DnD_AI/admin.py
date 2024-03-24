from django.contrib import admin
from .models import Weapon
from .models import Character
from .models import Monster
from .models import Chest
from .models import History

# Register your models here.

admin.site.register(Weapon)
admin.site.register(Character)
admin.site.register(Monster)
admin.site.register(Chest)
admin.site.register(History)