import binascii

def xor(_string, _key):
    rawBytes1 = binascii.unhexlify(_string)
    rawBytes2 = binascii.unhexlify(_key)

    if len(rawBytes1) != len(rawBytes2):
        raise ValueError("le texte et la clef doivent avoir la meme longueur")

    xor_result = bytes(a ^ b for a, b in zip(rawBytes1, rawBytes2))
    return binascii.hexlify(xor_result).decode()

string = '1c0111001f010100061a024b53535009181c'
key = '686974207468652062756c6c277320657965'

print(xor(string, key))