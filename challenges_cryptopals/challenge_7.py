from Crypto.Cipher import AES
import base64

key = b"YELLOW SUBMARINE"

with open("challenge_7.txt", "r") as file:
    ciphertext_base64 = file.read()

ciphertext = base64.b64decode(ciphertext_base64)

cipher = AES.new(key, AES.MODE_ECB)
plaintext = cipher.decrypt(ciphertext)

print("Message:\n", plaintext.decode(errors="ignore"))