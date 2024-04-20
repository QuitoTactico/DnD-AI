import os
import PIL
import json
from PIL import Image
from io import BytesIO
import numpy as np
from dotenv import load_dotenv, find_dotenv
from PIL import Image
import requests

import google.generativeai as genai

# Definición de funciones
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

# Configuración de API Keys de Gemini y HuggingFace
_ = load_dotenv('api_keys.env')
genai.configure(api_key=os.environ.get('gemini_api_key'))
hf_api_key = os.environ.get('hf_api_key')

# Se carga la lista de películas
with open('movie_titles.json', 'r') as file:
    file_content = file.read()
    movies = json.loads(file_content)


# 1. Generación de descripción de las películas
model = genai.GenerativeModel('gemini-pro')
#Se carga la lista de películas de movie_titles.json
idx_movie = np.random.randint(len(movies)-1)
movie = movies[idx_movie]
movie_title = movie["title"]
print(movie_title)

instruction = "Vas a actuar como un aficionado del cine que sabe describir de forma clara, concisa y precisa \
cualquier película en menos de 200 palabras. La descripción debe incluir el género de la película y cualquier \
información adicional que sirva para crear un sistema de recomendación."

prompt = f"{instruction} Has una descripción de la película {movie_title}"

response = model.generate_content(prompt)

print(response.text)


#2 Generación de las imágenes de las películas

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {hf_api_key}"}

prompt = f"Carátula de la película {movie_title}"

image_bytes = query({
	"inputs": prompt,
})
# You can access the image with PIL.Image for example
image = Image.open(BytesIO(image_bytes))
image.show()


#3 Generación de embeddings
response_emb = genai.embed_content(
    model="models/embedding-001",
    content=response.text,
    task_type="retrieval_document",
    title="Embedding of single string")

# 1 input > 1 vector output
print(str(response_emb['embedding'])[:50], '... TRIMMED]')