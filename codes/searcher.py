DATA = None
SORUCES = None

def load_data(sources):
    SORUCES = sources
    with open(f"{SORUCES}/total.txt", 'r', encoding='utf-8') as file:
        DATA = file.read()
        # print(DATA)
    print("SEMANTIC SEARCH ENGINE\t: ready")

def get_contexts(question=""):
    return f"Páratartalom adatai:{str(DATA)}\n\n"