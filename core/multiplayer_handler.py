from core.wordlist_handler import is_word_allowed
from core.hangman_game import hangman, intro
from core.visuals.color import colors
from core.visuals.clear_screen import clear_screen
import time

def handle_multiplayer():
    clear_screen()

    intro()

    word = ask_for_word()

    clear_screen()

    print(f"{colors.GRAY}(Ge nu datorn till spelaren som ska gissa){colors.ENDC}")

    time.sleep(5)

    intro()

    input(f"{colors.GREEN}Tryck på enter när du vill påbörja spelet!{colors.ENDC}")

    hangman(word)

def ask_for_word() -> str:
    has_chosen_a_word = False

    while not has_chosen_a_word:
        word = input("Personen som inte ska gissa, vänligen skriv ett godtyckligt ord: ").lower().strip()

        if is_word_allowed(word):
            print(f"Du har valt ordet {colors.GREEN}{word}{colors.ENDC}")
            return word
        else: 
            print(f"{colors.RED}Vänligen ange ett ord som följer spelreglerna.{colors.ENDC}")