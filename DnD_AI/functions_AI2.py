import os
#import PIL
#import json
from PIL import Image
from io import BytesIO
#import numpy as np
#from dotenv import load_dotenv, find_dotenv
from PIL import Image
import requests
from .API import API_KEY, gemini_api_key, hf_api_key
#from API import API_KEY, gemini_api_key, hf_api_key # for testing purposes

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configuración de API Keys de Gemini y HuggingFace
'''
_ = load_dotenv('/api_keys.env')
genai.configure(api_key=os.environ.get('gemini_api_key'))
hf_api_key = os.environ.get('hf_api_key')
'''
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gemini_api_key
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-pro')

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {hf_api_key}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content


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

    response = model.generate_content(prompt,
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
        return f"{response.prompt_feedback}\n{response.candidates[0].finish_reason}\n{response.candidates[0].safety_ratings}"



def image_generation_HF(prompt_input):
    prompt = f"Epic scene of {prompt_input}"

    image_bytes = query({
        "inputs": prompt,
    })
    #print(image_bytes)
    #print(hf_api_key)
    # You can access the image with PIL.Image for example
    image = Image.open(BytesIO(image_bytes))
    image.save("media/image.png")
    #image.show()
    return image



'''
#3 Generación de embeddings
response_emb = genai.embed_content(
    model="models/embedding-001",
    content=response.text,
    task_type="retrieval_document",
    title="Embedding of single string")

# 1 input > 1 vector output
print(str(response_emb['embedding'])[:50], '... TRIMMED]')
'''

def test():
    while True:
        option = input("1. Action Interpreter\n2. Image Generation\n3. Exit\n-> ")
        if option == "1":
            action = action_interpreter(input("What do you want to do?"))
            print(action)
        elif option == "2":
            image = image_generation_HF(input("What image do you want to see?"))
            image.show()
        else:
            break

test()