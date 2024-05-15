import os

folder_path = r'C:\Users\Esteban\Downloads\-CODE-\DnD-AI\media\weapon\images\boss_weapons'
file_names = []

for file_name in os.listdir(folder_path):
    file_names.append(file_name)

print(file_names)