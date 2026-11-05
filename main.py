import asyncio
from pathlib import Path

from SoundManager import SoundManager
from SoundLoader import *

def main():
    sound_loader = SoundLoader()
    source = Path("pro-metei-dimon-www.exe")
    try:
        saved = sound_loader.save_original(source)
    except FileLoadError as e:
        print(e)
if __name__ == '__main__':
    main()