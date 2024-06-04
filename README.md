**`Winners of Inventiva 2024-1 on the "Best Performance" category!`** *Thanks to everybody, you're the real heroes :)*

![The Pibes](unpaid_creators.jpg)

We are already developing a `new version on Go`, with most of the functions `migrated into Javascript`, give it a look: [DnD-AI 2.0](https://github.com/QuitoTactico/DnD-AI-2.0)

# Welcome to DnD-AI!

Each year, 10 million Dungeons and Dragons sessions are created, but did you know that more than half of these cannot take place due to a `lack of a Dungeon Master?` Dungeons and Dragons is a game that relies entirely on the imagination of its players, and among them, the Dungeon Master is `the one who creates the story` the players will follow, develops characters, their abilities, monsters, maps, and items – essentially, `the heart of the game`. We depend heavily on them, and there isn't always someone willing to take on the role.

What if we replaced them with an `artificial intelligence` that is available at all times? One that allows you and your friends to play a quality session whenever you want, `generating the map and enemies` automatically. That's us, DnD-AI, and we want to offer you this new way of playing – much more focused on immediate gameplay and with a faster pace.

Unlike similar ideas, we have various visual enhancements, such as `real-time map` visualization and the `generation of images` for the epic scenes that, until now, you could only imagine.

`Our wiki:` https://github.com/QuitoTactico/DnD-AI/wiki

`Our backlog:` https://github.com/users/QuitoTactico/projects/1

## To run *(do the pip install if it's your first time running the project):*

```
pip install -r "requirements.txt"
python manage.py runserver
```

Or ```sudo python3 manage.py runserver 0.0.0.0:80``` if you want your own public instance.

## Software requirements

- The needed dependencies and libraries defined in requirements.txt. To get them, run ```pip install -r "requirements.txt"```

## AI usage requirements

- For image generation is needed either a `OpenAI API key` or a `HuggingFace API key`.  
- For action interpretation, storytelling and campaign's info providing, a `Google Gemini API key` is needed. OpenAI GPT option will be re-added in the future.

You can provide this keys either creating a file called `api_keys.env` on the root dir of the project.

```
# api_keys.env
# on root dir of the project

openai_api_key = 
hf_api_key = 
gemini_api_key = 
```

Or a file called `API.py` on `/DnD_AI/` (the application, not the project). At the same level of `functions_AI.py`, the file that uses the api keys.
```
# API.py
# on same folder as /DnD_AI/functions_AI.py

openai_api_key = " "
hf_api_key = " "
gemini_api_key = " "
```

In any case, `the game is still playable with some (or none) of the API keys`. While AI generated images being replaced with placeholder images and action inputs not being interpreted, but supporting the use of commands instead.

## What's should to be seen:

![image](https://github.com/QuitoTactico/DnD-AI/assets/99926526/4bac83d7-8e10-4661-bfef-7cbe5681a18f)

![image](https://github.com/QuitoTactico/DnD-AI/assets/99926526/21186308-4e1e-4799-bc64-f393180639c0)

https://github.com/QuitoTactico/DnD-AI/assets/99926526/f426ac7c-4650-45de-a765-424f47cc1a3c


## Created by:
> - [Esteban Vergara Giraldo](https://github.com/QuitoTactico)
> - [Miguel Angel Cock Cano](https://github.com/MiguelCock)
> - [Sebastian Salazar Osorio](https://github.com/Sebasalazaro)
>
> For the EAFIT course: Integrator project 1
