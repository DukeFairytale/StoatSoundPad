import asyncio
from fileinput import filename
from pathlib import Path
from uuid import uuid4
import subprocess

BASE_DIR =  Path(__file__).resolve().parent
SOUNDS_DIR = BASE_DIR / 'sounds'
ORIGINAL_SOUNDS = SOUNDS_DIR / 'origins'
PCM_SOUNDS = SOUNDS_DIR / 'pcm'
ALLOWED_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".mp4"}
MAX_FILE_SIZE = 40 * 1024 * 1024

class FileLoadError(Exception):
    pass
class ConvertationError(Exception):
    pass
class SoundLoader:
    def __init__(self):
        ORIGINAL_SOUNDS.mkdir(parents=True,exist_ok=True)
        PCM_SOUNDS.mkdir(parents=True,exist_ok=True)
        self.uploads = {}
        self.max_concurrent_uploads  = 3

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

    def convert_to_pcm(self, source_path):

        pcm_path = PCM_SOUNDS / f'{Path(source_path).stem}.pcm'
        tmp_path = pcm_path.with_suffix(pcm_path.suffix + '.tmp')

        command = [
            "ffmpeg",
            "-i", str(source_path),
            "-f", "s16le",
            "-ar", "48000",
            "-ac",
            "1",
            str(tmp_path)
        ]

        try:
            subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=True
            )

            if tmp_path.is_file() and tmp_path.stat().st_size > 0:
                tmp_path.replace(pcm_path)
                return pcm_path
            else:
                raise ConvertationError("Не удалось конвертировать аудиофайл")

        finally:
            tmp_path.unlink(missing_ok=True)

    def process_upload(self, source_file, filename: str):

        saved_path = self.save_original(source_file, filename)

        try:
            pcm_path = self.convert_to_pcm(saved_path)
            return pcm_path
        except ConvertationError:
            saved_path.unlink(missing_ok=True)
            raise FileLoadError("Ошибка при загрузке файла, пожалуйста повторите заново")





