import json

DATA = None
SORUCES = None

def load_data(sources):
    SORUCES = sources
    with open(f"{SORUCES}/total.json", 'r') as file:
        DATA = json.load(file)
    print("SEMANTIC SEARCH ENGINE\t: ready")

def get_contexts(question=""):
    return f"Páratartalom adatai (JSON):{str(DATA)}\n\n"