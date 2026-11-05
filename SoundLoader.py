import asyncio
from fileinput import filename
from pathlib import Path
from uuid import uuid4

BASE_DIR =  Path(__file__).resolve().parent
SOUNDS_DIR = BASE_DIR / 'sounds'
ORIGINAL_SOUNDS = SOUNDS_DIR / 'origins'
ALLOWED_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".mp4"}
MAX_FILE_SIZE = 40 * 1024 * 1024

class FileLoadError(Exception):
    pass
class SoundLoader:
    def __init__(self):
        ORIGINAL_SOUNDS.mkdir(parents=True,exist_ok=True)
        self.uploads = {}
        self.max_concurrent_uploads  = 3
        if ORIGINAL_SOUNDS.is_dir():
            print('Директория для оригинальных звуков создана')

    def validate_sound(self, filename: str):
        if  Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
            raise FileLoadError(f"Недопустимый формат файла. Допустимые форматы: {', '.join(sorted(ALLOWED_EXTENSIONS))}")
        print('Проверка прошла успешно')

    def _generate_sound_path_original(self, filename: str):
        file_format = Path(filename).suffix
        sound_id = uuid4().hex

        return ORIGINAL_SOUNDS / f'{sound_id}{file_format}'

    def save_original(self, source_file, filename: str):
        self.validate_sound(filename)
        save_path = self._generate_sound_path_original(filename)
        save_path_tmp = save_path.with_suffix(save_path.suffix + '.tmp')

        try:
            final_size = 0
            with open(save_path_tmp, "wb") as destination:
                while True:
                    chunk = source_file.read(1024 * 1024)

                    if not chunk:
                        break
                    final_size += len(chunk)
                    if final_size > MAX_FILE_SIZE:
                        raise FileLoadError('Превышен размер загружаемого файла, Максимальный размер 40МБ')
                    destination.write(chunk)

            if final_size != save_path_tmp.stat().st_size:
                raise FileLoadError("Ошибка при загрузке файла, пожалуйста повторите заново")

            save_path_tmp.replace(save_path)

            return save_path
        finally:
            save_path_tmp.unlink(missing_ok=True)




