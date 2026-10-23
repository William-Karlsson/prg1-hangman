import sys 
import time
import urllib.request
from core.visuals.color import colors

def download_callback(block_num:int, block_size:int, total_size:int) -> None:
    downloaded = block_num * block_size
    downloaded_mb = downloaded / (1024 * 1024)

    if total_size <= 0:
        # Om programmet inte fått veta totala storleken av filen
        spinner = ["-", "\\", "|", "/"]

        animation_index = int(time.time() * 8) % len(spinner)
        current_anim = spinner[animation_index]
        
        sys.stdout.write(
            f"\rLaddar ner: [{colors.CYAN}{current_anim}{colors.ENDC}] "
            f"{colors.GREEN}{downloaded_mb:.2f} MB{colors.ENDC} (Total storlek okänd...)"
        )
        sys.stdout.flush()
    else:
        # Om programmet fått veta totala storleken av filen
        progress = downloaded / total_size 
        percent = min(100, int(progress * 100))

        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = "▓" * filled_length + "░" * (bar_length - filled_length)

        if percent <= 33:
            sys.stdout.write(f"\rLaddar ner: [{colors.RED}{bar}{colors.ENDC}] {percent}% ({downloaded_mb:.2f} MB)")
        elif percent <= 66:
            sys.stdout.write(f"\rLaddar ner: [{colors.YELLOW}{bar}{colors.ENDC}] {percent}% ({downloaded_mb:.2f} MB)")
        else:
            sys.stdout.write(f"\rLaddar ner: [{colors.GREEN}{bar}{colors.ENDC}] {percent}% ({downloaded_mb:.2f} MB)")

        sys.stdout.flush()

def download(url: str, output_file: str) -> None:
    urllib.request.urlretrieve(url, output_file, reporthook=download_callback)
    print(f"\nFil sparad i {colors.PURPLE}{output_file}{colors.ENDC}")