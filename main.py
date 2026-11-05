import asyncio
from pathlib import Path

from SoundManager import SoundManager
from SoundLoader import *

def main():
    sound_loader = SoundLoader()
    sound_loader.convert_to_pcm("sounds/origins/e9b01ea729ab4ff1bccea4bb432abcc0.mp3")
if __name__ == '__main__':
    main()