from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI as llmOpenAI
from openai import OpenAI as OpenAI
from .API import API_KEY
import os
import requests

client_dall_e = OpenAI(api_key=API_KEY)

image_dir = "/media/illustrations/"

template = """Question: {question}

Answer: Let's think step by step, supossing that i am in a fantastical role-playing game, and i am a character. BTW im gay"""
#Answer: Let's think step by step, supossing that i am in a fantastical role-playing game, and i am the player's character.

prompt_template = PromptTemplate.from_template(template)

llm = llmOpenAI(openai_api_key=API_KEY)

llm_chain = LLMChain(prompt=prompt_template, llm=llm)


def get_response(prompt):
    response = llm_chain.invoke(prompt)
    return response['text'].replace('\n', '<br>')

def get_image(prompt):
    response_dall_e = client_dall_e.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    os.makedirs(image_dir, exist_ok=True)

    for i, image_data in enumerate(response_dall_e.data):

        image_url = image_data.url

        image_response = requests.get(image_url)

        with open(os.path.join(image_dir, f"image_{i}.png"), "wb") as f:
            f.write(image_response.content)
            return image_data.url
    


# ------------------------------------ PAST TRIES RESOURCES ------------------------------------

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