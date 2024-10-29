import json

# Object(s)
with open('config.json', 'r') as file:
    config = json.load(file)

with open(f"{config['sources']}/total.json", 'r') as file:
    data = json.load(file)
print("LOADED\t\t\t: data")

def get_contexts(question=""):
    return f"Páratartalom adatai (JSON):{str(data)}\n\n"