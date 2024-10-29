import json
import socket

# Object(s)
with open('config.json', 'r') as file:
    config = json.load(file)

history = []

print("Hello, mizu?")

while True:
    question = input()
    if len(question) == 0:
        continue
    else:
        history.append({"role": "user", "content": question})
        
        # Kliens kapcsolat létrehozása és kérés küldése
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((config["bridge"]["host"], config["bridge"]["port"]))
            message = json.dumps(history)
            # print(f"Küldés a szervernek: {question}")
            client_socket.sendall(message.encode('utf-8'))  # Kérdés küldése

            # Válasz stream fogadása
            full_response = ""
            while True:
                data = client_socket.recv(16)  # Válasz fogadása
                if not data:
                    break  # Ha nincs több adat, kilép a ciklusból
                full_response += data.decode('utf-8')
                print(data.decode('utf-8'), end='')  # Részleges válasz kiírása a streamből
            
            history.append({"role": "assistant", "content": full_response})
            # print("\nTeljes válasz:", full_response)
    print("")
