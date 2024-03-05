from DnD_AI.models import *
from DnD_AI.default import *
from django.core.management.base import BaseCommand

def delete_every_template_weapon():
    for weapon_name in DEFAULT_WEAPON_STATS:
        if weapon_name != 'Bare hands':
            if Weapon.objects.filter(name=weapon_name, is_template=True).exists():
                Weapon.objects.filter(name=weapon_name, is_template=True).delete()

class Command(BaseCommand):
    help = 'Deletes the default weapons in the database'

    def handle(self, *args, **kwargs):
        delete_every_template_weapon()
        self.stdout.write(self.style.SUCCESS('Successfully deleted every template weapon'))