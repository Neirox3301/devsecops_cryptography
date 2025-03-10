def hamming_distance(_str1, _str2):
    assert len(_str1) == len(_str2)
    
    # Convertir en bytes si c'est une chaîne de caractères
    bytes1 = _str1.encode() if isinstance(_str1, str) else _str1
    bytes2 = _str2.encode() if isinstance(_str2, str) else _str2

    # XOR chaque byte et compter les bits à 1
    return sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(bytes1, bytes2))

# Test avec l'exemple du challenge
str1 = "this is a test"
str2 = "wokka wokka!!!"

print(hamming_distance(str1, str2))