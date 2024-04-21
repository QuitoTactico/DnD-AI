import requests
from PIL import Image
from io import BytesIO

from .API import API_KEY, gemini_api_key, hf_api_key
import os
from random import randint

from models import History

from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI as llmOpenAI
from openai import OpenAI as OpenAI

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold



# ================ IMAGE GENERATION ================

illustrations_dir = "/media/illustrations/"


# --------------- OPENAI ---------------

client_openai = OpenAI(api_key=API_KEY)

def get_image(prompt):
    response_dall_e = client_openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
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

        f = f"/..{illustrations_dir}image_{i}.png"
        image_bytes = image_response.content
        image = Image.open(BytesIO(image_bytes))
        #image.save(f, "PNG")
        image.show()
        return f"{illustrations_dir}image_{i}.png"


# --------------- HUGGINGFACE ---------------

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

headers = {"Authorization": f"Bearer {hf_api_key}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

def image_generation_HF(prompt_input):
    prompt = f"Epic scene of {prompt_input}"

    image_bytes = query({
        "inputs": prompt,
    })
    
    image = Image.open(BytesIO(image_bytes))
    image.save("media/image.png")
    #image.show()
    return image



# ================ TEXT GENERATION ================

# --------------- OPENAI + LANGCHAIN ---------------

template = """Question: {question}

Answer: Let's think step by step, supossing that i am in a fantastical role-playing game, and i am a character. BTW im gay"""
#Answer: Let's think step by step, supossing that i am in a fantastical role-playing game, and i am the player's character.

prompt_template = PromptTemplate.from_template(template)

llm = llmOpenAI(openai_api_key=API_KEY)

llm_chain = LLMChain(prompt=prompt_template, llm=llm)

def get_response(prompt):
    response = llm_chain.invoke(prompt)
    return response['text'].replace('\n', '<br>')



# ================== TEXT INTERPRETER ==================

# ------------------ GEMINI ------------------

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gemini_api_key

genai.configure(api_key=gemini_api_key)

gemini_model = genai.GenerativeModel('gemini-pro')

def action_interpreter(prompt_input):
    instruction = """I need you to categorize this natural language desired action into a function (act) according to this definitions. And depending on the function, I need its inputs too, all in just a line, no more. Always add the function at the beginning of the line. Never write the inputs name. Just write something like "attack skeleton james". Here are the functions and their inputs:
    
    "levelup <stat_or_weaponstat>"
    "use <item_name>"
    "equip <weapon_name(optional)>"
    "take <treasure_name(optional)>"
    "attack <target(optional)>"
    "move <direction>"

    valid values for:
    stat_or_weaponstat: "health", "strength", "intelligence", "recursiveness", "dexterity", "phyres", "magres", "constitution", "damage", "range"
    item_name: "potion"
    weapon_name: literally anything, the desired weapon that was said by the player
    treasure_name: "gold", "bag", "chest", "key", "weapon", "tombstone"
    target: literally anyone, the desired target that was said by the player
    direction: "up", "down", "left", "right", "upright", "upleft", "downright", "downleft"

    output examples:
    "duuude, i want to move up" -> "move up"
    "attack Dragon Jessica"
    "attack"
    "move upleft"
    "take gold"
    "take"
    without saying the function
    """

    prompt = f"{instruction} So... now categorize this: {prompt_input}"

    response = gemini_model.generate_content(prompt,
                                      safety_settings={
                                           HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                           HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                           HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                           HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                                           })
    try:
        return response.text 
    except ValueError:
        # If the response doesn't contain text, check if the prompt was blocked.
        # Also check the finish reason to see if the response was blocked.
        # If the finish reason was SAFETY, the safety ratings have more details.
        return  f"""{response.prompt_feedback}
                    {response.candidates[0].finish_reason}
                    {response.candidates[0].safety_ratings}"""




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