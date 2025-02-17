import socket
import threading

SERVER_IP = '127.0.0.1'  # Adresse du serveur (met l'IP publique si distant)
PORT = 12345             # Doit être le même que le serveur

def receive_messages(client_socket):
    """Reçoit et affiche les messages des autres clients"""
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(message.decode())
        except:
            break

    client_socket.close()

def start_client():
    """Démarre un client"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))

    print("Connecté au serveur ! Vous pouvez envoyer des messages.")

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    while True:
        message = input("")
        if message.lower() == "quit":
            break
        client_socket.send(message.encode())

    client_socket.close()

if __name__ == "__main__":
    start_client()