import requests
from PIL import Image
from io import BytesIO
import os
from random import randint, choice

try:
    try:
        from DnD_AI.models import *
    except: 
        from models import *
except:
    pass # Testing purposes


# we decided to manage them this way and not with a .env file because we had problems with the .env file
try:
    from .API import API_KEY, gemini_api_key, hf_api_key    
except:
    from .API import API_KEY, gemini_api_key, hf_api_key  #Testing purposes
    
from openai import OpenAI as OpenAI

from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI as llmOpenAI

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold



# ================ IMAGE GENERATION ================

illustrations_dir = "media\\illustrations\\"


# --------------- OPENAI (DALL-E) ---------------

client_openai = OpenAI(api_key=API_KEY)

def image_generator_DallE(prompt):
    '''Through OpenAI API, uses dall-e-3'''

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
        i = randint(0, 999999999999999999)

        image_url = image_data.url

        image_response = requests.get(image_url)

        #with open(os.path.join(image_dir, f"image_{i}.png"), "wb") as f:
            #f.write(image_response.content)
            #return image_data.url

        #image_route = f"{illustrations_dir}image_{i}.png"
        image_dir = f"media\\illustrations\\image_DE_{i}.png"
        image_bytes = image_response.content
        image = Image.open(BytesIO(image_bytes))
        image.save(image_dir)
        #image.show()
        return image_dir.replace('\\', '/')


# --------------- HUGGINGFACE (STABLE DIFFUSION) ---------------

StabDiff_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

headers = {"Authorization": f"Bearer {hf_api_key}"}

def StabDiff_query(payload):
	response = requests.post(StabDiff_API_URL, headers=headers, json=payload)
	return response.content

def image_generator_StabDiff(prompt_input):
    '''Through HuggingFace API, uses stable diffusion x1 1.0'''

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
    image_route = f"media\\illustrations\\image_SD_{i}.png"
    
    image = Image.open(BytesIO(image_bytes))
    image.save(image_route)
    #image.show()
    #return image
    return image_route.replace('\\', '/')



# ================ TEXT GENERATION ================

# --------------- OPENAI (GPT) + LANGCHAIN ---------------

template = """Question: {question}

Answer: Let's think step by step, supossing that i am in a fantastical role-playing game, and i am the player's character.
"""
#Answer: Let's think step by step, supossing that i am in a fantastical role-playing game, and i am a character. BTW im gay

prompt_template = PromptTemplate.from_template(template)

llm = llmOpenAI(openai_api_key=API_KEY)

llm_chain = LLMChain(prompt=prompt_template, llm=llm)

def continue_history_gpt(prompt):
    response = llm_chain.invoke(prompt)
    return response['text'].replace('\n', '<br>')


# ------------------ GOOGLE (GEMINI) ------------------

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gemini_api_key

gemini_model = genai.GenerativeModel('gemini-pro')

genai.configure(api_key=gemini_api_key)

# later, initialice as None, and ask if it's none on the views. If it is None, initialize it with the campaign context. 
# if it's not None, let's assume that it has already the history of the campaign. 
gemini_chat = gemini_model.start_chat(history=[])

safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

def create_initial_stories_gemini(prompt:str="", n:int=3) -> list:
    stories = []
    world_type = ["fantasy", "sci-fi", "medieval", "cyberpunk", "post-apocalyptic", "steampunk", "futuristic", "dystopian", "utopian", "magical", "mystical", "mythical", "legendary", "historical", "modern"]

    for _ in range(n):
        story = gemini_model.generate_content(f"Tell me a story about a {choice(world_type)} world where i have to defeat some strong enemies and bosses to win, this is a initial story of a game. Also tell me at least three names of key bosses and it's race and class to be defeated, and why i have to defeat them. Don't talk about a protagonist or a specific hero, just leave it like a mission to fulfill for 'anyone' or 'you (talking to the player)'. "+prompt,
                                              safety_settings=safety_settings)
        stories.append(story.text)
    return stories


def continue_history_gemini(prompt:str="", campaign_story:str="", campaign_achievements:str="") -> str:
    response = gemini_chat.send_message(f"i did this: {prompt}. Progress the story taking in count that i'm in this world: {campaign_story}. and now my party already achieved this: {campaign_achievements}",
                                        safety_settings=safety_settings)
    return response.text


def ask_world_info_gemini(prompt:str="about what to do next", campaign_story:str="", campaign_achievements:str="") -> str:
    response = gemini_chat.send_message(f"Tell me {prompt}. Answer taking in count that i've already achieved this: [{campaign_achievements}].\nIn this world: [{campaign_story}]\n.",
                                        safety_settings=safety_settings)
    return response.text


# ================== TEXT INTERPRETER ==================

# ------------------ GOOGLE (GEMINI) ------------------

def action_interpreter(prompt_input) -> str:
    instruction = """I need you to categorize this natural language desired action into a function (act) according to this definitions. And depending on the function, I need its inputs too, all in just a line, no more. Always add the function at the beginning of the line. Never write the inputs name. Just write something like "attack skeleton james". For move, use specifically its valid values. Here are the functions and their inputs:
    
    "levelup <stat_or_weaponstat>"
    "use <item_name>"
    "equip <weapon_name(optional)>"
    "take <treasure_name(optional)>"
    "attack <target(optional)>"
    "move <direction>"
    "info <question>"

    valid values for:
    stat_or_weaponstat: "health", "strength", "intelligence", "recursiveness", "dexterity", "phyres", "magres", "constitution", "damage", "range"
    direction: "up", "down", "left", "right", "upright", "upleft", "downright", "downleft"
    treasure_name: "gold", "bag", "chest", "key", "weapon", "tombstone"
    target: literally anyone, the desired target that was said by the player
    weapon_name: literally anything, the desired weapon that was said by the player
    question: literally anything, the desired information interest that was said by the player
    item_name: "potion"

    output examples:
    "duuude, i want to move up" -> "move up"
    "attack Dragon Jessica"
    "attack"
    "move upleft"
    "take gold"
    "take"
    "i want to know about where to go next" -> "info where to go next"
    without saying the function
    """
    #about_what: "player", "enemies", "bosses", "world", "game", "story", "quests", "items", "weapons", "enemies", "bosses", "npcs",

    prompt = f"{instruction} So... now categorize this: {prompt_input}"

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