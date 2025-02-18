import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

CESAR_SHIFT = 1

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(cesar_encryption(message, -CESAR_SHIFT))
        except:
            print("Déconnecté du serveur.")
            client_socket.close()
            break

def start_client():
    # démarrer un nouveau client et le connecter au serveur
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # attend que le serveur demande un pseudo
    prompt = client_socket.recv(1024).decode('utf-8')
    print(prompt, end="")

    # le client entre son usernam
    username = input("")
    client_socket.send(username.encode('utf-8'))

    print("Connecté au chat ! Tapez 'quit' pour quitter.")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("Vous: ")
        if message.lower() == "quit":
            client_socket.send(message.encode('utf-8'))
            client_socket.close()
            break
        
        client_socket.send((cesar_encryption(message, CESAR_SHIFT)).encode('utf-8'))

def cesar_encryption(message, shift):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    encrypted_message = ""

    for letter in message:
        if letter.lower() in alphabet:
            new_index = (alphabet.index(letter.lower()) + shift) % 26
            new_letter = alphabet[new_index]

            if letter.isupper():
                new_letter = new_letter.upper()
            
            encrypted_message += new_letter
        else:
            encrypted_message += letter

    return encrypted_message

if __name__ == "__main__":
    start_client()