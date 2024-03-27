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


def get_response(prompt):
    response = llm_chain.invoke(prompt)
    return response['text'].replace('\n', '<br>')



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