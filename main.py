import random
import string
import os
import sys
import requests
from string import ascii_letters
from random import choice

# clear
if sys.platform in ('linux', 'darwin'):
    CLEAR = 'clear'
elif sys.platform == 'win32':
    CLEAR = 'cls'
else:
    print('Plateforme non supportée', file=sys.stderr)
    exit(1)

def clear_term() -> None:
    os.system(CLEAR)

def get_letters(number: int):
    letters = ''.join([choice(ascii_letters) for i in range(number)])
    letters = letters.lower();
    return letters

def get_words_by_length(letters: str) -> dict[int, dict] | None:
    url = 'https://api.poocoo.fr/api/v1/words-from-letters'
    parameters: dict[str, str] = {"letters": letters}
    response = requests.get(url=url, params=parameters)

    if response.status_code >= 200 and response.status_code < 400:
        data = response.json()
        words_by_length = {}
        for group in data["data"]["wordGroups"]:
            words_by_length[group["length"]] = {
                "words": group["words"],
                "count": group["count"]
            }
        return words_by_length
    else:
        return None

def crossword():
    test: bool = False
    while not test:
        print("""Choisissez la difficulté :
            1 - Facile
            2 - Moyen
            3 - Difficile
            4 - Tres difficile
    """)
        difficulte = int(input("\nVotre choix : "))
        clear_term()
        print(f"Vous avez choisi {difficulte} etes vous sur ?")
        verif = str(input("Oui / Non : ")).lower()
        
        if verif == "oui":
            test = True
        if verif == "non":
            clear_term()
            continue
        else:
            print("Mauvais choix...")
            clear_term()
    
    l: int = 0
    if difficulte == 1:
        l = 3
    elif difficulte == 2:
        l = 4
    elif difficulte == 3:
        l = 5
    elif difficulte == 4:
        l = 6
    
    letters = get_letters(l)

    print(f"{letters}")
    result = get_words_by_length(letters)
    if result is None:
    # gérer le cas d'échec/ régénérer des lettres etc.
    else:
    # utiliser result normalement

crossword()