import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ChatClient(tk.Tk):
    def __init__(self, send_callback):
        super().__init__()

        self.geometry("400x500")
        self.configure(bg="#f0f0f0")

        self.chat_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, state="disabled", height=15)
        self.chat_area.pack(padx=10, pady=10, fill="both", expand=True)

        self.entry_message = tk.Entry(self, font=("Arial", 12))
        self.entry_message.pack(padx=10, pady=5, fill="x")
        self.entry_message.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self, text="Envoyer", font=("Arial", 12), command=self.send_message)
        self.send_button.pack(pady=5)

        self.username_label = tk.Label(self, text="Choisissez un pseudo :", font=("Arial", 12))
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self, font=("Arial", 12))
        self.username_entry.pack(padx=10, pady=5, fill="x")

        self.username_button = tk.Button(self, text="Se connecter", font=("Arial", 12), command=self.connect_to_server)
        self.username_button.pack(pady=10)

        self.send_callback = send_callback

    def connect_to_server(self):
        """Cette fonction est appelée après avoir entré le pseudo"""
        username = self.username_entry.get()
        if username:
            self.send_callback(username)
            self.username_entry.config(state="disabled")
            self.username_button.config(state="disabled")
            self.username_label.config(text=f"Connecté en tant que {username}")
            print(f"Pseudo choisi : {username}")

    def send_message(self, event=None):
        message = cesar(self.entry_message.get(), CESAR_SHIFT)

        if message:
            self.display_message(f"Moi: {message}")
            self.send_callback(message)
            self.entry_message.delete(0, tk.END)

    def display_message(self, _message):
        message = cesar(_message, -CESAR_SHIFT)

        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state="disabled")
        self.chat_area.yview(tk.END)

HOST = "127.0.0.1"
PORT = 5555
CESAR_SHIFT = 1

def receive_messages(_client_socket, _gui):
    """Reçoit les messages du serveur en continu"""
    while True:
        try:
            message = _client_socket.recv(1024).decode('utf-8')
            _gui.display_message(message)
        except:
            print("Déconnecté du serveur.")
            _client_socket.close()
            break

def start_client():
    # démarrer un nouveau client et le connecter au serveur
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # attendre que le serveur demande un pseudo
    prompt = client_socket.recv(1024).decode('utf-8')
    print(prompt, end="")

    # lancer l'interface sur Tkinter
    gui = ChatClient(send_callback=lambda msg: client_socket.send(msg.encode('utf-8')))
    
    # recevoir des messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, gui))
    receive_thread.daemon = True
    receive_thread.start()

    gui.mainloop()

def cesar(_message, _shift):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    encrypted_message = ""

    for letter in _message:
        if letter.lower() in alphabet:
            new_index = (alphabet.index(letter.lower()) + _shift) % 26
            new_letter = alphabet[new_index]

            if letter.isupper():
                new_letter = new_letter.upper()
            encrypted_message += new_letter
        else:
            encrypted_message += letter

    return encrypted_message

if __name__ == "__main__":
    start_client()