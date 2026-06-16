import random
import string
import os
import sys
import requests
from string import ascii_letters
from random import choice, choices

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

#bypass cloudfare for api
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "fr-FR,fr;q=0.9",
    "Referer": "https://poocoo.fr/",
}

FRENCH_LETTER_FREQ = {
    'a': 7.64, 'b': 0.90, 'c': 3.26, 'd': 3.67, 'e': 14.71,
    'f': 1.07, 'g': 0.87, 'h': 0.74, 'i': 7.53, 'j': 0.61,
    'k': 0.05, 'l': 5.46, 'm': 2.97, 'n': 7.10, 'o': 5.38,
    'p': 3.02, 'q': 1.36, 'r': 6.69, 's': 7.95, 't': 7.24,
    'u': 6.31, 'v': 1.84, 'w': 0.04, 'x': 0.43, 'y': 0.13, 'z': 0.33
}


def get_letters(number: int) -> str:
    population = list(FRENCH_LETTER_FREQ.keys())
    weights = list(FRENCH_LETTER_FREQ.values())
    letters = ''.join(choices(population, weights=weights, k=number))
    return letters.lower()


def get_words_by_length(letters: str) -> dict[int, dict] | None:
    url = 'https://api.poocoo.fr/api/v1/words-from-letters'
    parameters: dict[str, str] = {"letters": letters}
    response = requests.get(url=url, params=parameters, headers=HEADERS)

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


def total_words(result: dict[int, dict]) -> int:
    return sum(group["count"] for group in result.values())


def crossword():
    test: bool = False
    difficulte: int = 0

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
        elif verif == "non":
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
    result = get_words_by_length(letters)

    while result is None or total_words(result) < 4:
        letters = get_letters(l)
        result = get_words_by_length(letters)

    print(f"Your letters are : {letters.upper()}")


crossword()