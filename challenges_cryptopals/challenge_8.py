with open("challenge_8.txt", "r") as file:
    potential_ecb_lines = []

    for line_number, line in enumerate(file):
        line = line.strip()
        
        try:
            decoded_bytes = bytes.fromhex(line)

            blocks = [decoded_bytes[i:i + 16] for i in range(0, len(decoded_bytes), 16)]

            # compter le nombre de bloc répétés
            unique_blocks = set(blocks)
            num_repeated_blocks = len(blocks) - len(unique_blocks)

            # si il y a une répétition, alors la stocker dans potential_ecb_lines
            if num_repeated_blocks > 0:
                potential_ecb_lines.append((line_number, line, num_repeated_blocks))

        except ValueError:
            print(f"Erreur")

# afficher les infos de la ligne la plus probable de potential_ecb_lines
for line in potential_ecb_lines:
    print(f"ligne {line[0]}, nombre de répétitions : {line[2]}, ligne: \n{line[1]}")