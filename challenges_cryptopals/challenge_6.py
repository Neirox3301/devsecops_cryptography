import base64

# calculer la distance de Hamming
def hamming_distance(_str1, _str2):
    assert len(_str1) == len(_str2)
    return sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(_str1, _str2))

# devine la taille de la clef KEYSIZE en testant plusieurs valeurs entre 2 et 40
# utilise la distance de Hamming pour mesurer la similarité des blocs chiffrés de même taille
# retourne les 3 tailles de clef les plus probables avec la plus petite distance normalisée
def guess_keysize(_ciphertext):
    keysize_scores = []
    for keysize in range(2, 41):
        # calculer la distance de Hamming moyenne entre plusieurs blocs
        chunks = [_ciphertext[i:i + keysize] for i in range(0, len(_ciphertext), keysize)][:4]
        distances = [hamming_distance(chunks[i], chunks[i + 1]) / keysize for i in range(len(chunks) - 1)]
        avg_distance = sum(distances) / len(distances)
        keysize_scores.append((keysize, avg_distance))

    # retourne les 3 résultats les plus probables
    return sorted(keysize_scores, key=lambda x: x[1])[:3]

# divise le texte chiffré en blocs de taille KEYSIZE
def split_into_blocks(_ciphertext, _keysize):
    return [_ciphertext[i:i + _keysize] for i in range(0, len(_ciphertext), _keysize)]

# tester chaques blocs entre eux avec la clef
def transpose_blocks(_blocks, _keysize):
    return [bytes(block[i] for block in _blocks if i < len(block)) for i in range(_keysize)]

# teste si le texte contient des lettres beaucoup utilisées en anglais et retourne un score
def score_english(_text):
    common_letters = "ETAOIN SHRDLUetaoinshrdlu"
    return sum(_text.count(char) for char in common_letters)

# décrypter chaque bloc de XORé avec un seul octet
def single_byte_xor_decrypt(_block):
    possible_keys = range(256)
    decrypted_texts = [(key, bytes(b ^ key for b in _block)) for key in possible_keys]
    return max(decrypted_texts, key=lambda pair: score_english(pair[1].decode(errors="ignore")))[0]

# trouver la clef en entière en analysant chaques blocs
def find_xor_key(_ciphertext, _keysize):
    blocks = split_into_blocks(_ciphertext, _keysize)
    transposed_blocks = transpose_blocks(blocks, _keysize)
    return bytes(single_byte_xor_decrypt(block) for block in transposed_blocks)

# applique le XOR avec une clef répétitive pour déchiffrer le texte
def repeating_key_xor(_ciphertext, _key):
    return bytes(_ciphertext[i] ^ _key[i % len(key)] for i in range(len(_ciphertext)))

with open("challenge_6.txt", "r") as file:
    ciphertext_base64 = file.read()

ciphertext = base64.b64decode(ciphertext_base64)

best_keysizes = guess_keysize(ciphertext)

best_decryption = None
best_score = 0

for keysize, _ in best_keysizes:
    key = find_xor_key(ciphertext, keysize)
    decrypted_text = repeating_key_xor(ciphertext, key).decode(errors="ignore")
    
    # appelle la fonction vérifiant si c'est probablement un texte en anglais
    text_score = score_english(decrypted_text)

    if text_score > best_score:
        best_score = text_score
        best_decryption = (key, decrypted_text)

if best_decryption:
    print(f"Clef : {best_decryption[0].decode(errors='ignore')}")
    print(f"Message :\n{best_decryption[1]}")
else:
    print("Échec du déchiffrement.")