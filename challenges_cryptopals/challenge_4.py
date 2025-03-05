import binascii

def try_decrypt(hex_string):
    for key in range(256):
        try:
            cipher_bytes = bytes.fromhex(hex_string.strip())

            decoded_bytes = bytes(c ^ key for c in cipher_bytes)
            decoded_string = decoded_bytes.decode()

            print(f"Clé : {key} ({chr(key)}) | Message : {decoded_string}")
        except (UnicodeDecodeError, ValueError):
            continue

# Lire le fichier et tester chaque ligne
with open("challenge_4.txt", "r", encoding="utf-8") as file:
    for line in file:
        try_decrypt(line)