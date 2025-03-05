
string = "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"
key = "ICE"

encoded_string = string.encode()
encoded_key = key.encode()

cipher_bytes = []

for i in range(len(encoded_string)):
    key_char = encoded_key[i % len(encoded_key)]
    
    cipher_char = encoded_string[i] ^ key_char
    cipher_bytes.append(cipher_char)

cipher_bytes = bytes(cipher_bytes)

cipher_hex = cipher_bytes.hex()

print(cipher_hex)