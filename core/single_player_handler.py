from core.visuals.color import colors
from core.visuals.clear_screen import clear_screen
from core.wordlist_handler import handle_initial_wordlist_existance_check, handle_choose_wordlist, pick_random_word
from core.hangman_game import hangman, intro

wordlist_path = "wordlists/"

def handle_singleplayer():
    handle_initial_wordlist_existance_check(wordlist_path)
    
    wordlist = handle_choose_wordlist(wordlist_path)

    clear_screen()

    intro()

    input(f"{colors.GREEN}Tryck på enter när du vill påbörja spelet!{colors.ENDC}")

    play(wordlist)

def play(wordlist_path: str):
    word = pick_random_word(wordlist_path)
    
    if word is None:
        print("Spelet kunde inte starta: Inga giltiga ord hittades.")
        return

    hangman(word)