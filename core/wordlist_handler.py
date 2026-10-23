import os 
import time
from core.visuals.color import colors
from core.visuals.clear_screen import clear_screen
from core.download_handler import download
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import random

def handle_initial_wordlist_existance_check(folder_path: str):
    if is_folder_empty(folder_path):
        handle_no_wordlist(folder_path)

def handle_no_wordlist(folder_path: str):
    clear_screen()

    print(f"{colors.RED}Inga nedladdade ordlistor kunde hittas! Du behöver ladda ner en för att kunna spela.{colors.ENDC}")
    handle_wordlist_download(folder_path, False)

def handle_wordlist_download(folder_path: str, clear_screen_before_menu:bool = True):
    if clear_screen_before_menu:
        clear_screen()

    print("Det här programmet förväntar sig ordlistor i LMF-format (Lexical Markup Framework) i XML-format som följer ISO 24613 standarden.")
    
    print("\nHär finna några rekommendationer för ordlistor:")

    recommended = [("Kelly-listan","Svenska","https://svn.spraakbanken.gu.se/sb-arkiv/pub/lmf/kelly/kelly.xml"),
                   ("Open English WordNet","Engelska","https://llds.ling-phil.ox.ac.uk/llds/xmlui/bitstream/handle/20.500.14106/2571-2024/english-wordnet-2024.xml?sequence=5&isAllowed=y")
                   ]

    list_num = 1
    for element in recommended:
        print(f"[{colors.PURPLE}{list_num}{colors.ENDC}] - {colors.GREEN}{element[0]}{colors.ENDC} ({element[1]}) {colors.GRAY}({element[2]}){colors.ENDC}")
        list_num += 1
    
    print("\n")
    choice = input(f"Vänligen välj en av alternativen i listan (1-{len(recommended)}) eller ange en egen url: ")

    url = ""

    try: 
        choice_index = int(choice) - 1
        url = str(recommended[choice_index][2])
    except Exception as e:
        url = choice

    clean_path = urlparse(url).path

    filename = os.path.basename(clean_path)

    try:
        download(url, os.path.join(folder_path, filename))
    except Exception as e:
        print(f"{colors.RED} Någonting gick fel!{colors.ENDC} ", e)

def handle_choose_wordlist(folder_path: str):
    has_chosen_wordlist = False

    while not has_chosen_wordlist:
        clear_screen()
        print(f"Välkommen till enspelar-{colors.CYAN}Hangman{colors.ENDC}!")

        print("\nVänligen välj en ordlista att spela med nedan: ")
        print(f"\n--- {colors.GREEN}Tillgängliga ordlistor{colors.ENDC} ---")

        # Hitta xml filer
        all_files = os.listdir(folder_path)
        xml_files = [f for f in all_files if f.lower().endswith('.xml')]

        # Lista alla hittade xml filer
        if not xml_files:
            print(f"{colors.GRAY}(Inga nedladdade XML-filer hittades i mappen){colors.ENDC}")
        else:
            for index, filename in enumerate(xml_files, start=1):
                print(f"[{colors.PURPLE}{index}{colors.ENDC}] - {colors.GREEN}{filename}{colors.ENDC}")

        print("")

        # Andra menyalternativ
        print(f"[{colors.PURPLE}D{colors.ENDC}] - Ladda ner annan ordlista")
        if xml_files:
            print(f"[{colors.PURPLE}R{colors.ENDC}] - Ta bort ordlista")

        print("")
        choice = input("Välj ett alternativ (nummer eller bokstav): ").strip().upper()

        # Hantera användarens val
        if choice == 'D':
            handle_wordlist_download(folder_path)
        elif choice == 'R' and xml_files:
            delete_wordlist_menu(folder_path, xml_files)
        else:
            try:
                file_index = int(choice) - 1
                if 0 <= file_index < len(xml_files):
                    selected_file = xml_files[file_index]
                    full_path = os.path.join(folder_path, selected_file)
                    print(f"\nDu har valt ordlistan: {colors.GREEN}{selected_file}{colors.ENDC}")
                    has_chosen_wordlist = True
                    return full_path
                else:
                    print(f"{colors.RED}Fel: Ogiltigt nummer.{colors.ENDC}")
                    time.sleep(1)
            except ValueError:
                print(f"{colors.RED}Fel: Ogiltigt val.{colors.ENDC}")
                time.sleep(1)
            
def delete_wordlist_menu(folder_path: str, xml_files: list[str]) -> None:
    clear_screen()

    print(f"\n--- {colors.RED}Ta bort en ordlista{colors.ENDC} ---")
    for index, filename in enumerate(xml_files, start=1):
        print(f"[{colors.PURPLE}{index}{colors.ENDC}] - {colors.GRAY}{filename}{colors.ENDC}")
        
    print(f"[{colors.PURPLE}C{colors.ENDC}] - Avbryt och gå tillbaka")
    print("")
    
    choice = input("Vilken ordlista vill du ta bort? ").strip().upper()
    
    if choice == 'C':
        print("Radering avbruten.")
        return
        
    try:
        file_index = int(choice) - 1
        if 0 <= file_index < len(xml_files):
            file_to_delete = xml_files[file_index]
            full_path = os.path.join(folder_path, file_to_delete)
            
            confirm = input(f"Är du säker på att du vill ta bort {colors.RED}{file_to_delete}{colors.ENDC}? (y/n): ").strip().lower()
            if confirm == 'y':
                os.remove(full_path)
                print(f"{colors.GREEN}Filen raderades framgångsrikt!{colors.ENDC}")
            else:
                print("Radering avbruten.")
        else:
            print(f"{colors.RED}Fel: Numret finns inte i listan.{colors.ENDC}")
            time.sleep(3)
            delete_wordlist_menu(folder_path, xml_files)
    except ValueError:
        print(f"{colors.RED}Fel: Ange ett giltigt nummer.{colors.ENDC}")

        time.sleep(3)
        delete_wordlist_menu(folder_path, xml_files)
    except Exception as e:
        print(f"{colors.RED}Ett fel uppstod när filen skulle tas bort:{colors.ENDC} {e}")

        time.sleep(3)
        delete_wordlist_menu(folder_path, xml_files)

def is_folder_empty(folder_path: str) -> bool:
    empty = True
    for _ in os.scandir(folder_path):
        empty = False
        break

    if empty:
        return True
    else:
        return False
    
def pick_random_word(wordlist_path: str) -> str:
    if not isinstance(wordlist_path, str) or not os.path.isfile(wordlist_path):
        print(f"{colors.RED}Fel: Sökvägen '{wordlist_path}' är inte en giltig fil.{colors.ENDC}")
        return None

    try:
        print(f"{colors.GREEN}Analyserar ditt lexikon...{colors.ENDC}")
        tree = ET.parse(wordlist_path)
        root = tree.getroot()

        all_words = set() 

        for element in root.findall('.//*'):
            tag_name = element.tag.split('}')[-1].lower() if '}' in element.tag else element.tag.lower()
            word_to_add = ""
            
            if tag_name == "feat" and element.get('att') == 'writtenForm':
                val = element.get('val')
                if val:
                    word_to_add = val.strip()
                
            for attr_name, attr_value in element.attrib.items():
                clean_attr = attr_name.split('}')[-1].lower() if '}' in attr_name else attr_name.lower()
                if clean_attr == "writtenform" and attr_value:
                    word_to_add = attr_value.strip()

            if tag_name in ["lemma", "form", "item"] and element.text:
                word_text = element.text.strip()
                if word_text and not word_text.startswith('{'):
                    word_to_add = word_text
            
            # Sortera och se till att ordet faktiskt passar kraven för att fungera i spelet
            if is_word_allowed(word_to_add):
                all_words.add(word_to_add)

        word_list = list(all_words)
        print(f"Total unika ord funna i lexikonet: {len(word_list):,}")

        if not word_list:
            print(f"{colors.RED}XML-filen lästes, men inga ord kunde identifieras. Vänligen prova igen med en annan ordlista.{colors.ENDC}")
            return None
        
        print(f"{colors.GREEN}Färdig med analys, väljer ett ord ur listan.{colors.ENDC}")

        return random.choice(word_list)

    except ET.ParseError:
        print(f"{colors.RED}Fel: Filen är skadad eller är inte en giltig XML-fil.{colors.ENDC}")
        return None
    except PermissionError:
        print(f"{colors.RED}Fel: Saknar behörighet att läsa filen.{colors.ENDC}")
        return None
    except Exception as e:
        print(f"{colors.RED}Ett oväntat fel uppstod{colors.ENDC}: {e}")
        return None
    
def is_word_allowed(word: str) -> bool:
    allowed_letters = set("abcdefghijklmnopqrstuvwxyzåäö")

    try:
        if set(word).issubset(allowed_letters) and word.strip() != "":
            return True 
        else:
            return False
    except:
        # Om någonting går fel, anta att ordet inte är tillåtet. 
        return False