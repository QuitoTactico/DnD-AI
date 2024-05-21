import requests
from PIL import Image
from io import BytesIO
import os
from random import randint, choice


try:
    from DnD_AI.models import *
except:
    try:
        from models import *
    except: 
        from .models import *


try:  # AI modules changes frequently, so it's nice to import them in a try-except
    from openai import OpenAI as OpenAI

    from langchain.chains.llm import LLMChain
    from langchain.prompts import PromptTemplate
    from langchain_openai import OpenAI as llmOpenAI

    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
except:
    pass



# ================ OBTAINING THE KEYS ================


# its required to have either the openai or the huggingface api key
# its required to have the google gemini api key

# YES I KNOW...
# aaaaaall the possible ways to import the api keys (the users are... unpredictable) are:
#   1. having API.py in the same file than this file
#   2. having api_keys.env in root
#   3. having api_keys.env in the same folder than this file
#   4. having API.py in the root, two ways to import it
#   5. having any .env file in any folder in the root or above (damn... jesus christ)
try:    # 1
    from .API import openai_api_key, hf_api_key, gemini_api_key   
except:
    try:    # 2
        from dotenv import load_dotenv
        load_dotenv('api_keys.env')

        openai_api_key = os.getenv('openai_api_key') # its required to have either the openai 
        hf_api_key = os.getenv('hf_api_key')         # or the huggingface api key
        gemini_api_key = os.getenv('gemini_api_key') # its required to have the google gemini api key
    except:
        try:   # 3
            load_dotenv('DnD_AI/api_keys.env')

            openai_api_key = os.getenv('openai_api_key')
            hf_api_key = os.getenv('hf_api_key')        
            gemini_api_key = os.getenv('gemini_api_key')
        except:
            import sys
            sys.path.append("..")  # Añade la carpeta superior al PATH de Python

            try:   # 4
                from .API import openai_api_key, hf_api_key, gemini_api_key 
            except:
                try: 
                    from API import openai_api_key, hf_api_key, gemini_api_key   
                except:
                    try:   # 5
                        load_dotenv()
                        openai_api_key = os.getenv('openai_api_key')
                        hf_api_key = os.getenv('hf_api_key')        
                        gemini_api_key = os.getenv('gemini_api_key')
                    except:
                        pass # you just don't have api keys... so you can't use the AI functions
                
NO_API_KEYS_STR = "Sorry dude, you didn't set the api keys or you ran out of balance. Please set the api keys or try again later. Jaja salu2"

def NO_API_KEYS_IMG(): return f"media/entity/icons/no_api_keys{randint(1,3)}.png"


# ================ IMAGE GENERATION ================

#illustrations_dir = "media\\illustrations\\"
illustrations_dir = "media/illustrations/"


# --------------- OPENAI (DALL-E) ---------------

try:
    client_openai = OpenAI(api_key=openai_api_key)
except:
    pass


def image_generator_DallE(prompt):
    '''Through OpenAI API, uses dall-e-3'''

    try:
        response_dall_e = client_openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024", # the image generation is being too slow
            #size="512x512",
            #style="vivid",    # i've found this is possible
            #style="natural", 
            quality="standard",
            n=1,
        )

        #os.makedirs(image_dir, exist_ok=True)

        for _, image_data in enumerate(response_dall_e.data):
            i = randint(0, 9999999)

            image_url = image_data.url

            image_response = requests.get(image_url)

            #with open(os.path.join(image_dir, f"image_{i}.png"), "wb") as f:
                #f.write(image_response.content)
                #return image_data.url

            #image_route = f"{illustrations_dir}image_{i}.png"
            image_dir = f"{illustrations_dir}image_DE_{i}.png"
            image_bytes = image_response.content
            image = Image.open(BytesIO(image_bytes))
            try:
                image.save(image_dir)
            except:
                image.save(image_dir.replace('/', '\\'))
            #image.show()
            return image_dir.replace('\\', '/')
    except:
        try:
            return image_generator_StabDiff(prompt)
        except:
            return NO_API_KEYS_IMG()


# --------------- HUGGINGFACE (STABLE DIFFUSION) ---------------

StabDiff_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

headers = {"Authorization": f"Bearer {hf_api_key}"}

def StabDiff_query(payload):
	response = requests.post(StabDiff_API_URL, headers=headers, json=payload)
	return response.content

def image_generator_StabDiff(prompt_input):
    '''Through HuggingFace API, uses stable diffusion x1 1.0'''

    try:
        prompt = f"Epic scene of {prompt_input}"

        image_bytes = StabDiff_query({
            "inputs": prompt,
        })

        i = randint(0, 999999999999999999)

        # ruta absoluta del directorio de ilustraciones, no funcionó
        #abs_illustrations_dir = os.path.abspath(illustrations_dir)

        # ruta absoluta al guardar la imagen
        #image_route = f"{abs_illustrations_dir}\image_{i}.png"
        #image_route = f"media\\image_{i}.png"
        image_dir = f"{illustrations_dir}image_SD_{i}.png"
        
        image = Image.open(BytesIO(image_bytes))
        try:
            image.save(image_dir)
        except:
            image.save(image_dir.replace('/', '\\'))
        #image.show()
        #return image
        return image_dir.replace('\\', '/')
    except:
        return NO_API_KEYS_IMG()



# ================ TEXT GENERATION ================

# --------------- OPENAI (GPT) + LANGCHAIN ---------------

template = """Question: {question}

Answer: Let's think step by step, supossing that i am in a fantastical role-playing game, and i am the player's character.
"""
#Answer: Let's think step by step, supossing that i am in a fantastical role-playing game, and i am a character. BTW im gay

prompt_template = PromptTemplate.from_template(template)

try:
    llm = llmOpenAI(openai_api_key=openai_api_key)

    llm_chain = LLMChain(prompt=prompt_template, llm=llm)
except:
    pass

def continue_history_gpt(prompt):
    try:
        response = llm_chain.invoke(prompt)
        return response['text'].replace('\n', '<br>')
    except:
        return NO_API_KEYS_STR


# ------------------ GOOGLE (GEMINI) ------------------

try:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gemini_api_key

    gemini_model = genai.GenerativeModel('gemini-pro')

    genai.configure(api_key=gemini_api_key)

    # later, initialice as None, and ask if it's none on the views. If it is None, initialize it with the campaign context. 
    # if it's not None, let's assume that it has already the history of the campaign. 
    gemini_chat = gemini_model.start_chat(history=[])
except:
    pass

safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

def create_initial_stories_gemini(prompt:str="", n:int=3) -> list:
    prompt = prompt or ""   # if prompt is None, then it will be an empty string
    stories = []
    world_type = ["fantasy", "sci-fi", "medieval", "cyberpunk", "post-apocalyptic", "steampunk", "futuristic", "dystopian", "utopian", "magical", "mystical", "mythical", "legendary", "historical", "modern"]
    #render_format = "Use the html tag for underline instead of **"
    render_format = ". Write it using the HTML formats when underlining or bolding. No other format is allowed."

    for _ in range(n):
        try:
            story = gemini_model.generate_content(f"Tell me a story about a {choice(world_type)} world where i have to defeat some strong enemies and bosses to win, this is a initial story of a game. Also tell me at least three names of key bosses and it's race and class to be defeated, and why i have to defeat them. Don't talk about a protagonist or a specific hero, just leave it like a mission to fulfill for 'anyone' or 'you (talking to the player)'. "+prompt+render_format,
                                              safety_settings=safety_settings)
            initial_story = story.text.replace("\n", "<br>")
        except:
            initial_story = NO_API_KEYS_STR
        
        
        stories.append(initial_story)
    return stories


def continue_history_gemini(prompt:str="", campaign_story:str="", campaign_achievements:str="") -> str:
    try:
        response = gemini_chat.send_message(f"i did this: {prompt}. Progress the story taking in count that i'm in this world: {campaign_story}. and now my party already achieved this: {campaign_achievements}"+"Use the html tag for underline instead of **",
                                            safety_settings=safety_settings)
        return response.text
    except:
        return NO_API_KEYS_STR


def ask_world_info_gemini(prompt:str="about what to do next", campaign_story:str="", campaign_achievements:str="") -> str:
    render_format = ". Write it using the HTML formats when underlining or bolding. No other format is allowed."
    try:
        response = gemini_chat.send_message(f"Tell me {prompt}. Answer taking in count that i've already achieved this: [{campaign_achievements}].\nIn this world: [{campaign_story}]\n."+render_format,
                                            safety_settings=safety_settings)
        return response.text
    except:
        return NO_API_KEYS_STR


# ================== TEXT INTERPRETER ==================

# ------------------ GOOGLE (GEMINI) ------------------

TUTORIAL = """<ul>
                <li>/levelup &lt;stat_or_weaponstat&gt;</li>
                <li>/use &lt;item_name&gt;</li>
                <li>/equip &lt;weapon_name(optional)&gt;</li>
                <li>/take &lt;treasure_name(optional)&gt;</li>
                <li>/attack &lt;target(optional)&gt;</li>
                <li>/move &lt;direction&gt;</li>
                <li>/info &lt;question&gt;</li>
                <li>/see &lt;interest&gt;</li>
                <li>/talk &lt;target(optional)&gt;</li>
                <li>/help</li>
            </ul>

            <p>Valid values for:</p>
            <ul>
                <li>stat_or_weaponstat:
                    <ul>
                        <li>"health"</li>
                        <li>"strength"</li>
                        <li>"intelligence"</li>
                        <li>"recursiveness"</li>
                        <li>"dexterity"</li>
                        <li>"phyres"</li>
                        <li>"magres"</li>
                        <li>"constitution"</li>
                        <li>"damage"</li>
                        <li>"range"</li>
                    </ul>
                </li>
                <li>direction:
                    <ul>
                        <li>"up"</li>
                        <li>"down"</li>
                        <li>"left"</li>
                        <li>"right"</li>
                        <li>"upright"</li>
                        <li>"upleft"</li>
                        <li>"downright"</li>
                        <li>"downleft"</li>
                    </ul>
                </li>
                <li>treasure_name:
                    <ul>
                        <li>"gold"</li>
                        <li>"bag"</li>
                        <li>"chest"</li>
                        <li>"key"</li>
                        <li>"weapon"</li>
                        <li>"tombstone"</li>
                    </ul>
                </li>
                <li>target:
                    <ul>
                        <li>literally any target on range, a monster name</li>
                    </ul>
                </li>
                <li>weapon_name:
                    <ul>
                        <li>literally any near weapon</li>
                    </ul>
                </li>
                <li>question:
                    <ul>
                        <li>literally any desired information</li>
                    </ul>
                </li>
                <li>item_name:
                    <ul>
                        <li>"health potion"</li>
                        <li>"go back bone"</li>
                    </ul>
                </li>
                <li>interest:
                    <ul>
                        <li>"inventory"</li>
                        <li>"story"</li>
                        <li>"achievements"</li>
                        <li>"objectives"</li>
                        <li>"turns"</li>
                        <li>"physical_description"</li>
                    </ul>
                </li>
            </ul>"""

def action_interpreter(prompt_input) -> str:
    instruction = """I need you to categorize this natural language desired action into a function (act) according to this definitions. And depending on the function, I need its inputs too, all in just a line, no more. Always add the function at the beginning of the line. Never write the inputs name. Just write something like "attack skeleton james". For move, use specifically its valid values. Here are the functions and their inputs:
    
    "levelup <stat_or_weaponstat> <weapon_name(optional)>"
    "use <item_name>"
    "equip <weapon_name(optional)>"
    "take <treasure_name(optional)>"
    "attack <target(optional)>"
    "move <direction>"
    "info <question>"
    "see <interest>"
    "talk <target(optional)>"
    "help"

    valid values for:
    stat_or_weaponstat: "health", "strength", "intelligence", "recursiveness", "dexterity", "phyres", "magres", "constitution", "damage", "range", "weapon"
    direction: "up", "down", "left", "right", "upright", "upleft", "downright", "downleft"
    treasure_name: "gold", "bag", "chest", "key", "weapon", "tombstone"
    target: literally anyone, the desired target that was said by the player
    weapon_name: literally anything, the desired weapon that was said by the player. If it's not said, don't put it.
    question: literally anything, the desired information interest that was said by the player
    item_name: "health potion", "go back bone"
    interest: "inventory", "story", "achievements", "objectives", "turns", "physical_description", "description"

    output examples:
    "duuude, i want to move up" -> "move up"
    "attack Dragon Jessica"
    "attack"
    "move upleft"
    "take gold"
    "take"
    "i want to know about where to go next" -> "info where to go next"
    "level up my Super Excalibur" -> "levelup damage Super Excalibur"
    "make my Revolver's range bigger" -> "levelup range Revolver"
    without saying the function
    """
    #about_what: "player", "enemies", "bosses", "world", "game", "story", "quests", "items", "weapons", "enemies", "bosses", "npcs",

    prompt = f"{instruction} So... now categorize this: {prompt_input}"

    try:
        response = gemini_model.generate_content(prompt,
                                        safety_settings=safety_settings)
        try:
            return response.text 
        except ValueError:
            # If the response doesn't contain text, check if the prompt was blocked.
            # Also check the finish reason to see if the response was blocked.
            # If the finish reason was SAFETY, the safety ratings have more details.
            return  f"""{response.prompt_feedback}
                        {response.candidates[0].finish_reason}
                        {response.candidates[0].safety_ratings}"""
    except:
        '''
        return f"""{NO_API_KEYS_STR}
        
        But if you want to play anyways, there's the list of commands. they all starts with /
        
        {('zzzul'+instruction[377:-33]+'zzzulf').replace("\n", "zzzlifzzzli")}
        
        all starting with /""".replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>").replace('zzzulf', '</ul>').replace('zzzul', '<ul>').replace('zzzlif', '</li>').replace('zzzli', '<li>')
        '''

        return f"""{NO_API_KEYS_STR}
        
        But if you want to play anyways, there's the list of commands. they start with /
        """.replace("\n", "<br>")+TUTORIAL
    
        # Dios obra de formas misteriosas


def campaign_interpreter(campaign_id, n = int):
    campaign = Campaign.objects.get(id=campaign_id)

    attributes_response = {}

    for attribute in ['name', 'race', 'class', 'physical_description']:
        
        
        intro = f"Give me the {attribute} of the bosses of this story:" if attribute != 'physical_description' else f"Create the {attribute} of the {n} bosses of this story, a detailed physical description, perfect for image generation, talking about its clothes, physical appareance, colors, and others, you can create one if it's not said, 100 characters aprox:"

        prompt = f"""{intro}
        {campaign.initial_story}

        Please give it in a raw format and separed by |, like just this:  {attribute}1|{attribute}2|{attribute}3
        No other formats are allowed.""" 

        try:
            response = gemini_model.generate_content(prompt,
                                            safety_settings=safety_settings)
            
            attributes_response[attribute] = response.text.split('|')
            
        except:
            return {} , False
        
    return attributes_response, True


# ==================================== TESTING ====================================

def test():
    initial_story = ""
    while True:
        option = input("""
                       1. Action Interpreter
                       2. Image Generation
                       3. Initial story generation
                       4. Story progression
                       Any other. Exit
                       -> """)
        
        if option == "1":
            action = action_interpreter(input("What do you want to do?"))
            print(action)

        elif option == "2":
            prompt = input("What image do you want to see?")
            try:
                print("Dall-E")
                image = image_generator_DallE(prompt)
                image = Image.open(image)
                image.show()
            except:
                pass

            try:
                print("Stable Diffusion")
                image = image_generator_StabDiff(prompt)
                image = Image.open(image)
                image.show()
            except:
                pass
            
        elif option == "3":
            initial_stories = create_initial_stories_gemini()
            for i, story in enumerate(initial_stories):
                print("\n",i,"-"*20)
                print(story)
            
            selected_story = int(input("Select a story: "))
            initial_story = initial_stories[selected_story]
    
        elif option == "4":
            prompt = input("What have you done?")
            story = continue_history_gemini(prompt, initial_story)
            print(story)

        else:
            break

#test()


# ==================================== PAST TRIES RESOURCES ====================================

'''
# config openai key
openai.api_key = openai_api_key

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Traduce 'Hola mundo' al inglés",
  max_tokens=60
)

print(response.choices[0].text.strip())
# create language chain
#chain = langchain.LanguageChain()
'''

'''
def get_response(prompt):

    
    query = session.chat.completions.create(
        response_format={"type":"json:object"},
        messages=[
            {
                "role":"user","content":prompt
            }
        ],
        model="gpt-3.5-turbo",  
    )
    
    
    #chain.add_link(openai.Completion.create, engine="davinci-codex", prompt=prompt, max_tokens=60)

    #response = chain.run()
    
    response = llm_chain.invoke(prompt)
    return response['text'].replace('\n', '<br>')
    #text_responses = response['text'].split('\n')

    #return text_responses
    #print(response.choices[0].text.strip())
    #print(query.choices[0].message.content)

'''

'''
            #text_history.append(request.POST['player_name']+': '+request.POST['prompt'])
            
            made_by = 'SYSTEM: '
            for i in response:
                text_history.append(made_by+str(i))
                made_by=''
'''