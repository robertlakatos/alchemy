import os
import json
import socket
import requests
import searcher

from transformers import AutoConfig
from transformers import AutoTokenizer

from sentence_transformers import util
from sentence_transformers import SentenceTransformer

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

## Method(s)

def question_checkker(question, refq, treshold=0.5, model=None):
    if model is not None:
        emb_refq = model.encode(refq)
        emb_actq = model.encode([question])

        cosine_similarities = util.cos_sim(emb_refq, emb_actq)

        return cosine_similarities.mean() > treshold
    else:
        return False
    
def cleaning_stream(batch):
    if len(batch['text_output']) == 0:
        return False
    elif batch['text_output'] == "\n\n":
        return False
    elif "<|start_header_id|>" in batch['text_output']:
        return False
    elif "assistant" in batch['text_output']:
        return False
    elif "<|end_header_id|>" in batch['text_output']:
        return False
    else:
        return True
    
def reduce_message(chat, max_len):
    tokenizer.apply_chat_template(chat, tokenize=False)
    len_chat = len(tokenizer.encode(message))      
    while len_chat > max_len:
        chat = chat[0] + chat[2:]

        tokenizer.apply_chat_template(chat, tokenize=False)
        len_chat = len(tokenizer.encode(message))

    return tokenizer.apply_chat_template(chat, tokenize=False)   

# Object(s)
with open('config.json', 'r') as file:
    config = json.load(file)
print("LOADED\t\t\t: config")

url = f"{config['triton']['host']}:{config['triton']['port']}/v2/{config['triton']['model']}/{config['triton']['generation']}"
print("URL\t\t\t:", url)

tokenizer = AutoTokenizer.from_pretrained(config["tokenizer"])
print("TOKENIZER\t\t:", config["tokenizer"])

autoconfig = AutoConfig.from_pretrained(config["tokenizer"])
limit_pe = autoconfig.max_position_embeddings - config["guard"]["reduce_max_position_embeddings"]
print("MAX TOKEN INPUT SIZE\t:", autoconfig.max_position_embeddings)

model_st = SentenceTransformer(config["embedder"])
print("EMBEDDER\t\t:",config["embedder"])

# TCP szerver inicializálása
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((config["bridge"]["host"], config["bridge"]["port"]))
    server_socket.listen()
    print("SERVER\t\t\t: live",config["bridge"]["host"],config["bridge"]["port"])

    while True:
        client_socket, client_address = server_socket.accept()
        with client_socket:
            print(f"Kapcsolat létrejött: {client_address}")

            # Üzenet fogadása a kliens felől
            message = client_socket.recv(1024).decode('utf-8')
            print(f"Üzenet a klienstől: {message}")

            message = json.loads(message)
            
            # Alap chat beállítása
            chat = config["chat history"].copy()
            # History hozzáadása
            if len(message) > 1:
                chat = chat + message[:-1]
            # Contextus hozzáadsa
            chat.append({"role": "assistant", "content": searcher.get_contexts()})
            if question_checkker(question=message[-1]["content"], 
                    refq=config["filters"]["reference questions"], 
                    treshold=config["filters"]["treshold"], 
                    model=model_st):

                # Új kérdés hozzáadása
                chat.append(message[-1])
                print(chat)
                # megerősítés hozzáadása
                chat[-1]["content"] = chat[-1]["content"] + config["guard"]["reinforce"]
                
                # Üzenet létrehozzása limit határon belül
                chat = reduce_message(chat, limit_pe)
                print(f"Teljes üzenet a modelnek: {message}")

                # Triton kérés összeállítása
                payload = {
                    "text_input": message,
                    "max_tokens": config['triton']['max_tokens'],
                    "temperature": config['triton']['temperature'],
                    "stream": ("stream" in config['triton']['generation'])
                }

                # Kérelem küldése Triton szerverhez és stream feldolgozása
                with requests.post(url, json=payload, stream=True) as response:
                    if response.status_code == 200:
                        for line in response.iter_lines():
                            if line:
                                batch = json.loads(line.decode('utf-8').replace("data: ", ""))
                                if cleaning_stream(batch):
                                    # Stream válasz küldése a kliens felé
                                    client_socket.sendall(batch['text_output'].encode('utf-8'))
                    else:
                        error_message = f"Hiba történt: {response.status_code}"
                        print(error_message)
                        client_socket.sendall(error_message.encode('utf-8'))
            else:
                client_socket.sendall(config["guard"]["no information"].encode('utf-8'))