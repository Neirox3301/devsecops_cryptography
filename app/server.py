import socket
import threading

HOST = '0.0.0.0'  # Accepte toutes les connexions
PORT = 12345      # Port d'écoute du serveur

clients = []

def broadcast(message, sender_socket):
    """Envoie un message à tous les clients sauf l'émetteur"""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket):
    """Gère les messages reçus d'un client"""
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Message reçu: {message.decode()}")
            broadcast(message, client_socket)
        except:
            break

    client_socket.close()
    clients.remove(client_socket)
    print("Un client s'est déconnecté")

def start_server():
    """Lance le serveur"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Serveur démarré sur {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Nouvelle connexion : {addr}")
        clients.append(client_socket)

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()