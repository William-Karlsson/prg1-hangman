import time
from core.visuals.hangman_visuals import figure
from core.visuals.color import colors
from core.visuals.clear_screen import clear_screen
from core.wordlist_handler import is_word_allowed

def hangman(word:str):
    word = word.lower().strip()

    lives_remaining = 6

    has_guessed_correctly = False

    guesses = []
    while not has_guessed_correctly:
        clear_screen()

        show_figure(lives_remaining)
        print(word_progressively_unveiled(guesses, word))

        if len(guesses) >= 1:
            print(f"Du har gissat på: {", ".join(guesses)}")

        if lives_remaining > 0:
            guess = ""
            has_submitted_guess = False
            while not has_submitted_guess:
                guess = input(f"{colors.GRAY}Vänligen skriv din nästa gissning:{colors.ENDC} ").strip().lower()

                if is_word_allowed(guess):
                    guesses.append(guess)

                    has_submitted_guess = True
                else: 
                    print(f"{colors.RED}Du kan inte gissa på det. Se till att dina gissningar följer spelreglerna!{colors.ENDC}")

            if word_progressively_unveiled(guesses, word) == word:
                print(f"{colors.CYAN}Du gissade rätt!{colors.ENDC} Ordet var {colors.GREEN}{word}{colors.ENDC}.")
                has_guessed_correctly = True
            else:
                if guess not in word:
                    lives_remaining -= 1
        else:
            print(f"Du gissade {colors.RED}inte{colors.ENDC} rätt och förlorade!")
            print(f"Ordet var: {colors.CYAN}{word}{colors.ENDC}")
            break

    time.sleep(1)

    has_made_play_again_choice = False
    while not has_made_play_again_choice:
        play_again_choice = input("Vill du spela en till runda? (y/n): ").strip().lower()

        if play_again_choice in ["y", "n"]:
            has_made_play_again_choice = True
            if play_again_choice == "n":
                exit()
        else:
            print(f"{colors.RED}Vänligen skriv antingen 'y' eller 'n'.{colors.ENDC}")            

def word_progressively_unveiled(guesses:list[str], word:str) -> str:
    hidden_word = list("_" * len(word))

    for guess in guesses:
        if len(guess) == 1:
            for index, letter in enumerate(word):
                if letter == guess:
                    hidden_word[index] = guess 
        elif guess == word:
            hidden_word = word

    return "".join(hidden_word)

def show_figure(lives_remaining:int):
    print(figure[lives_remaining])

def intro():
    print(f"Välkommen till {colors.CYAN}Hangman{colors.ENDC}!")
    print("Här har du alla spelregler: ")
    show_game_rules()

def show_game_rules():
    print("- Du kan antingen gissa på ett helt ord eller en enda bokstav.")
    print("- Versaler och gemener spelar ingen roll.")
    print("- Ord kan bara innehålla bokstäver från det svenska alfabetet (abcdefghijklmnopqrstuvwxyzåäö).")
    print("- Ord kan inte innehålla mellanslag.")
    print("- Du vinner om du gissar rätt med färre än 6 fel.")