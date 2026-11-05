from fastapi import FastAPI, status, UploadFile, File
from SoundLoader import SoundLoader, FileLoadError
import asyncio


app = FastAPI()
loader = SoundLoader()


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "ok"}

@app.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_sound(file: UploadFile = File(...)):
    saved_path = await asyncio.to_thread(
        loader.save_original,
        file.file,
        file.filename)
    return {"filename": file.filename, 'saved_path' :saved_path}