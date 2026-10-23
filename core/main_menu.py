from core.singleplayer_handler import handle_singleplayer
from core.multiplayer_handler import handle_multiplayer
from core.visuals.color import colors
from core.visuals.clear_screen import clear_screen
from core.hangman_game import hangman
import time

def main_menu():
    while True:
        clear_screen()

        print(f"Välkommen till {colors.GREEN}Hangman{colors.ENDC}!")
        print("")
        print("Det här spelet har två spellägen!")
        print("")
        print(f"[{colors.PURPLE}1{colors.ENDC}] - {colors.CYAN}En{colors.ENDC} spelare {colors.GRAY}(Ord tas från ordlista){colors.ENDC}")
        print(f"[{colors.PURPLE}2{colors.ENDC}] - {colors.CYAN}Två{colors.ENDC} spelare {colors.GRAY}(Ena spelaren väljer ord){colors.ENDC}")
        print("")
        print(f"[{colors.PURPLE}stäng{colors.ENDC}] - {colors.RED}Stäng{colors.ENDC} programmet")
        print("")

        choice = input("Vänligen gör ett val('1', '2' eller 'stäng'): ")

        if choice in ["1", "2", "stäng"]:
            if choice == "1":
                handle_singleplayer()
            if choice == "2":
                handle_multiplayer()
            if choice == "stäng":
                exit()
        else:
            print(f"{colors.RED}Vänligen skriv antingen '1' eller '2'!{colors.ENDC}")
            time.sleep(3)