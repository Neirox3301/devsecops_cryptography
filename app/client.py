from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from tkinter import scrolledtext
import base64
import os
import socket
import threading
import tkinter as tk

# paramètres
HOST = "127.0.0.1"
PORT = 5555
ALPHABET = "abcdefghijklmnopqrstuvwxyz1234567890,?;./!§ù%^é¨'$£¤&(-è_çà)=~#[|`^@]*-+"
FIRST_MESSAGE = True

# choisir la clé des chiffrement
CODE_METHOD = "aes"

# CESAR
CESAR_SHIFT = 1

# VIGENERE
VIGENERE_KEY = "SECURITE"

# AES
def generate_aes_key_from_password(password, salt=b"MonSelUnique"):
    return PBKDF2(password, salt, dkLen=32)
AES_KEY = generate_aes_key_from_password("MotDePasseUltraSecret")

# visuel de l'application
class ChatClient(tk.Tk):
    # différents éléments visuels de l'application
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

    # se connecter au serveur
    def connect_to_server(self):
        global username 
        username = self.username_entry.get()
        
        if username:
            self.send_callback(username)
            self.username_entry.config(state="disabled")
            self.username_button.config(state="disabled")
            self.username_label.config(text=f"Connecté en tant que {username}")

    # chiffre et envoyer un message
    def send_message(self, event=None):
        global FIRST_MESSAGE
        connected_user = encryption_method(CODE_METHOD, "encrypt", f"[NOUVELLE CONNEXION] {username} s'est connecté")
        message = encryption_method(CODE_METHOD, "encrypt", f"{username}: {self.entry_message.get()}")

        if message:
            # messae à la première connexion
            if FIRST_MESSAGE == True:
                self.display_message(connected_user)
                self.send_callback(connected_user)
                FIRST_MESSAGE = False

            self.display_message(message)
            self.send_callback(message)
            self.entry_message.delete(0, tk.END)

    # déchiffre et afficher le message
    def display_message(self, _message):
        message = encryption_method(CODE_METHOD, "decrypt", _message)

        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state="disabled")
        self.chat_area.yview(tk.END)

def receive_messages(_client_socket, _gui):
    # recoit les messages du serveur
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

# choisir la fonction de chiffrement
def encryption_method(_method, _way, _message):
    if _method == "cesar":
        if _way == "encrypt":
            return cesar(_message, ALPHABET, CESAR_SHIFT)
        if _way == "decrypt":
            return cesar(_message, ALPHABET, -CESAR_SHIFT)
    elif _method == "vigenere":
        return vigenere(_message, ALPHABET, VIGENERE_KEY, decrypt=(_way == "decrypt"))
    elif _method == "aes":
        if _way == "encrypt":
            return encrypt_aes(_message, AES_KEY)
        if _way == "decrypt":
            return decrypt_aes(_message, AES_KEY)

# fonction de chiffrement par cesar
def cesar(_message, _alphabet, _shift):
    encrypted_message = ""

    for letter in _message:
        if letter.lower() in _alphabet:
            new_index = (_alphabet.index(letter.lower()) + _shift) % len(ALPHABET)
            new_letter = _alphabet[new_index]

            if letter.isupper():
                new_letter = new_letter.upper()
            encrypted_message += new_letter
        else:
            encrypted_message += letter

    return encrypted_message

# fonction de chiffrement par vigenere
def vigenere(_message, _alphabet, _key, decrypt=False):
    encrypted_message = ""
    key = _key.lower()
    key_length = len(key)

    for i, letter in enumerate(_message):
        if letter.lower() in _alphabet:
            key_letter = key[i % key_length]
            key_shift = _alphabet.index(key_letter)
            text_index = _alphabet.index(letter.lower())

            if decrypt:
                new_index = (text_index - key_shift) % len(_alphabet)
            else:
                new_index = (text_index + key_shift) % len(_alphabet)

            new_letter = _alphabet[new_index]
            if letter.isupper():
                new_letter = new_letter.upper()

            encrypted_message += new_letter
        else:
            encrypted_message += letter

    return encrypted_message

# fonction de chiffrement par AES
def encrypt_aes(_message, _key):
    iv = os.urandom(16)
    cipher = AES.new(_key, AES.MODE_CBC, iv)

    ciphertext = cipher.encrypt(pad(_message.encode(), AES.block_size))
    return base64.b64encode(iv + ciphertext).decode()

# fonction de déchiffrement par AES
def decrypt_aes(_message, _key):
    encrypted_bytes = base64.b64decode(_message)
    iv = encrypted_bytes[:16]
    ciphertext = encrypted_bytes[16:]

    cipher = AES.new(_key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

if __name__ == "__main__":
    start_client()