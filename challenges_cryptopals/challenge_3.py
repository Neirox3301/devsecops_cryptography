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

cipher_bytes = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")

for key in range(256):
    decoded_bytes = bytes(c ^ key for c in cipher_bytes)
    
    try:
        decoded_string = decoded_bytes.decode("utf-8")

        if is_english_text(decoded_string):
            print(f"Clé : {key} ({chr(key)}) | Message : {decoded_string}")

    except UnicodeDecodeError:
        continue