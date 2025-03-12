import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 5555

clients = {}  # dictionnaire {socket: username}
# générer la clé AES
def generate_aes_key():
    aes_key = os.urandom(32)

    with open("aes_key.bin", "wb") as f:
        f.write(aes_key)

generate_aes_key()

#envoyer un message à tous les utilisateurs connectés
def broadcast(message, sender_socket=None):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                client_socket.close()
                del clients[client_socket]

# traiter les requetes des utilisateurs
def handle_client(client_socket):
    try:
        # demande le psuedo du client
        client_socket.send("Choisissez un pseudo: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username

        # message dans le chat pour dire qu'il y a un nouveau client
        print(f"[NOUVEAU CLIENT] {username} s'est connecté.")

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message.lower() == "quit":
                break  # l'utilisateur se déconnecte
            
            broadcast(message, client_socket)

    except ConnectionResetError:
        pass
    finally:
        print(f"[DÉCONNEXION] {clients[client_socket]} s'est déconnecté.")
        del clients[client_socket]
        client_socket.close()

# démarrer le serveur et attendre des nouvelles connexions
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Serveur démarré sur {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Nouvelle connexion depuis {addr}")

        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()