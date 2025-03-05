import string

def score_english(text):
    common_letters = "ETAOIN SHRDLUetaoinshrdlu"
    common_words = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for"]

    letter_score = sum(text.count(char) for char in common_letters)
    word_score = sum(text.lower().count(word) for word in common_words)

    return letter_score + (word_score * 5)

def is_english_text(text):
    if not text:
        return False

    printable_chars = set(string.printable)
    printable_ratio = sum(1 for c in text if c in printable_chars) / len(text)

    return printable_ratio > 0.85 and score_english(text) > 10

def decrypt(_string):
    cipher_bytes = bytes.fromhex(_string.strip())

    for key in range(256):
        decoded_bytes = bytes(c ^ key for c in cipher_bytes)
        
        try:
            decoded_string = decoded_bytes.decode("utf-8")

            if is_english_text(decoded_string):
                print(f"Clé : {key} ({chr(key)}) | Message : {decoded_string}")

        except UnicodeDecodeError:
            continue

with open("challenge_4.txt", "r") as file:
    for line in file:
        decrypt(line)