from fastapi import FastAPI, status, UploadFile, File
from fastapi import HTTPException
from SoundLoader import SoundLoader, FileLoadError
import asyncio


app = FastAPI()
loader = SoundLoader()


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "ok"}

@app.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_sound(file: UploadFile = File(...)):
    try:
        saved_path = await asyncio.to_thread(
            loader.save_original,
            file.file,
            file.filename)

        await asyncio.to_thread(loader.convert_to_pcm, saved_path)
        return {"filename": file.filename, 'saved_path': saved_path}
    except FileLoadError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error))
