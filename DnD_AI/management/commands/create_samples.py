from DnD_AI.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates some examples of playable and non-playable characters in the database'

    def handle(self, *args, **kwargs):

        Character.objects.get_or_create(is_playable=True, name='Frieren the Slayer', 
                                        image='entity/images/Frieren.png',
                                        icon='entity/icons/Frieren_icon.png',
                                        character_race='Elf', character_class='Mage',
                                        story='Frieren is a powerful mage who has been traveling the world for centuries. She has seen the rise and fall of many civilizations, and has been a part of many of them. She is a wise and powerful ally, but also a dangerous enemy. She is a master of the arcane arts, and has a deep knowledge of the world and its secrets. Hates niggers.',
                                        physical_description='Female white-haired elf with twintails',
                                        level=50, exp=10, max_health=1000, intelligence=100)[0].save()
        
        Monster.objects.get_or_create(  name='Aura the Gilloutine', 
                                        icon='entity/icons/Aura_icon.png',
                                        monster_race='Demon', monster_class='Mage',
                                        physical_description='Female purple-haired demon with horns and buns',
                                        exp_drop=500, max_health=1000, intelligence=1)[0].save()

        self.stdout.write(self.style.SUCCESS('Successfully created some examples of playable and non-playable characters, monsters and weapons in the database'))