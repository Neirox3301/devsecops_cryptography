string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

for key in range(256):
    decoded_bytes = bytes(c ^ key for c in bytes.fromhex(string))
    
    try:
        decoded_string = decoded_bytes.decode()
        print(f"Clé : {key} ({chr(key)}) | Message : {decoded_string}")
    except UnicodeDecodeError:
        continue
