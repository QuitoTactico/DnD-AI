from django.contrib import admin
from .models import Weapon
from .models import Character
from .models import Monster

# Register your models here.

admin.site.register(Weapon)
admin.site.register(Character)
admin.site.register(Monster)