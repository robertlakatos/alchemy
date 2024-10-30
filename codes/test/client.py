import json
import socket

# Object(s)
with open('../mount/config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

history = []

print("Hello, mizu?")

while True:
    question = input()
    if len(question) == 0:
        #continue
        print("")
    else:
        history.append({"role": "user", "content": question})
        # print(history)
        
        # Host beállítása
        if config["bridge"]["host"] == "0.0.0.0":
            host = "127.0.0.1"
        else:
            host = config["bridge"]["host"]
        
        # Kliens kapcsolat létrehozása és kérés küldése
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, config["bridge"]["port"]))
            message = json.dumps(history, ensure_ascii=False)
            # print(f"Küldés a szervernek: {question}")
            
            client_socket.sendall(message.encode('utf-8'))  # Kérdés küldése

            # Válasz stream fogadása
            full_response = ""
            while True:
                data = client_socket.recv(32)  # Válasz fogadása
                if not data:
                    break  # Ha nincs több adat, kilép a ciklusból
                full_response += data.decode('utf-8')
                print(data.decode('utf-8'), end='', flush=True)  # Részleges válasz kiírása a streamből
            
            history.append({"role": "assistant", "content": full_response})
            # print("\nTeljes válasz:", full_response)
    print("")
