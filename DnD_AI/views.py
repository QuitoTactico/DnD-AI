from django.shortcuts import render
#from django.http import HttpRestponse

from .models import *
from .functions import *

from bokeh.embed import components

from django.shortcuts import render
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from .API import API_KEY

# Create your views here.

template = """Question: {question}

Answer: Let's think step by step."""

prompt_template = PromptTemplate.from_template(template)

llm = OpenAI(openai_api_key=API_KEY)

llm_chain = LLMChain(prompt=prompt_template, llm=llm)


'''
# config openai key
openai.api_key = API_KEY

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Traduce 'Hola mundo' al inglés",
  max_tokens=60
)

print(response.choices[0].text.strip())
# create language chain
#chain = langchain.LanguageChain()
'''

text_history = [f'{i}: Lorem ipsum dolor, sit amet consectetur adipisicing elit. Necessitatibus, sapiente? Beatae autem soluta modi alias, voluptatibus fugiat ab a mollitia qui laborum quae necessitatibus officia odit hic neque optio quibusdam.' for i in range(10)]


def get_response(prompt):

    '''
    query = session.chat.completions.create(
        response_format={"type":"json:object"},
        messages=[
            {
                "role":"user","content":prompt
            }
        ],
        model="gpt-3.5-turbo",  
    )
    '''
    
    #chain.add_link(openai.Completion.create, engine="davinci-codex", prompt=prompt, max_tokens=60)

    #response = chain.run()
    
    response = llm_chain.invoke(prompt)

    text_responses = response['text'].split('\n')

    return text_responses
    #print(response.choices[0].text.strip())
    #print(query.choices[0].message.content)

    
def home(request):
    # WEB LABELS
    # player_name=str   
    # roll_dice=bool    (optional)
    
    if request.method == "POST":
        #if True:     # i'm testing, sending all the things to the front.
        
        # DICE_ROLL
        #dice_needed = request.GET.get('dice_needed')
        #dice_needed = request.POST['dice_needed']
        dice_needed = 'dice_needed' in request.POST
        
        if dice_needed:   # If the roll_dice label is sent, it rolls the dice
            dice_value = roll_dice()
        else:               # If the roll_dice label is not sent, it sets the dice value to None, this way isn't rendered
            dice_value = None 
            dice_needed = False

        if 'action' in request.POST or "prompt" in request.POST:
            prompt = request.POST.get('prompt')
            response = get_response(prompt)
            text_history.append(request.POST['player_name']+': '+request.POST['prompt'])
            
            made_by = 'SYSTEM: '
            for i in response:
                text_history.append(made_by+str(i))
                made_by=''

        # GETTING DATA FROM THE DATABASE
        # player_name = request.GET.get('player')
        player_name = request.POST['player_name']


        if 'monster_id' in request.POST:
            try:
                monster_id = int(request.POST['monster_id'])
            except:
                monster_id = None
        else:
            monster_id = None

        # If there's any get/post, then gets the data from the database
       
        monsters = Monster.objects.all()
        characters = Character.objects.all()
        weapons = Weapon.objects.all()


        # PLAYER SELECTION
        # If through the player label they send the name of a playable character, it selects it as the player's character 
        player = player_selection(player_name)
        players = Character.objects.filter(is_playable=True)
        monster = monster_selection_by_id(monster_id)

        weapon_lvl = player.weapon.level
        weapon_lvl_label = '+'+str(weapon_lvl) if weapon_lvl > 0 else ''

        host = request.get_host()
        #map = create_map(player, characters, monsters, show_map = True)  # for map testing
        map = create_map(player, monster, characters, monsters, host)
        script, div = components(map)

        #test = request.GET.get('test')
        #test = request.POST['test']
        test = 'test' in request.POST
        page = 'test.html' if test else 'home.html'

        return render(request, page, {'player':player, 
                                      'players':players, 
                                      'player_name_sent':player_name, 
                                      'monster': monster, 
                                      'monsters':monsters, 
                                      'monster_id_sent': monster_id,
                                      'characters':characters, 
                                      'weapons':weapons, 
                                      'dice_value': dice_value, 
                                      'dice_needed': dice_needed,
                                      'script': script, 'div': div,
                                      #'url_prueba' : os.path.join(settings.BASE_DIR, player.icon.url[1:]).replace('\\', '/')
                                      'host': host,
                                      'url_prueba' : host + player.icon.url,
                                      'text_history': text_history,
                                      'weapon_lvl_label': weapon_lvl_label,
                                      } )
    else:
        # If there's no get/post, then it selects the first playable character in the database
        player = player_selection(None)
        monster = monster_selection_by_id(None)
        return render(request, 'home.html', {'player':player, 
                                            'monster': monster,
                                             'text_history':text_history,} )
    
