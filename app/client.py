import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

def receive_messages(client_socket):
    """Reçoit les messages du serveur en continu"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Déconnecté du serveur.")
            client_socket.close()
            break

def start_client():
    # Démarrer un nouveau client et le connecter au serveur
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Attend que le serveur demande un pseudo
    prompt = client_socket.recv(1024).decode('utf-8')
    print(prompt, end="")

    # Le client entre son usernam
    username = input("")
    client_socket.send(username.encode('utf-8'))

    print("Connecté au chat ! Tapez 'quit' pour quitter.")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("")
        if message.lower() == "quit":
            client_socket.send(message.encode('utf-8'))
            client_socket.close()
            break
        client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    start_client()