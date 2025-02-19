import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ChatClient(tk.Tk):
    def __init__(self, send_callback):
        super().__init__()

        self.title("Client Chat")
        self.geometry("400x500")
        self.configure(bg="#f0f0f0")

        # Zone d'affichage des messages
        self.chat_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, state="disabled", height=15)
        self.chat_area.pack(padx=10, pady=10, fill="both", expand=True)

        # Zone de saisie du message
        self.entry_message = tk.Entry(self, font=("Arial", 12))
        self.entry_message.pack(padx=10, pady=5, fill="x")
        self.entry_message.bind("<Return>", self.send_message)  # Envoi avec "Entrée"

        # Bouton d'envoi
        self.send_button = tk.Button(self, text="Envoyer", font=("Arial", 12), command=self.send_message)
        self.send_button.pack(pady=5)

        # Champ pour entrer le pseudo
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
            # Ensuite, tu pourras appeler la fonction qui commence à recevoir des messages et à envoyer des messages au serveur.

    def send_message(self, event=None):
    #Envoi du message au serveur et affichage immédiat dans l'interface
        message = self.entry_message.get()
        if message:
            self.display_message(f"Moi: {message}")  # Afficher directement le message
            self.send_callback(message)  # Envoyer au serveur
            self.entry_message.delete(0, tk.END)  # Effacer l'entrée après envoi


    def display_message(self, message):
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state="disabled")
        self.chat_area.yview(tk.END)


HOST = "127.0.0.1"
PORT = 5555

def receive_messages(client_socket, gui):
    """Reçoit les messages du serveur en continu"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            gui.display_message(message)
        except:
            print("Déconnecté du serveur.")
            client_socket.close()
            break

def start_client():
    # démarrer un nouveau client et le connecter au serveur
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Attendre que le serveur demande un pseudo
    prompt = client_socket.recv(1024).decode('utf-8')
    print(prompt, end="")

    # Lancer l'interface graphique Tkinter
    gui = ChatClient(send_callback=lambda msg: client_socket.send(msg.encode('utf-8')))
    
    # Recevoir des messages en parallèle
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, gui))
    receive_thread.daemon = True  # Permet de quitter le programme même si le thread est en cours d'exécution
    receive_thread.start()

    gui.mainloop()  # Lancer Tkinter en parallèle


if __name__ == "__main__":
    start_client()


#salut