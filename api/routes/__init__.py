from fastapi import APIRouter,UploadFile,File,Body
from fastapi.responses import FileResponse
from pydantic import BaseModel
import aiofiles
from typing import List
import os
from karaoke_app.audio_splitter.split import split_audio as split
from karaoke_app.audio_splitter.vocal_to_lyrics import vocal_to_lyrics as convert2lyrics
from pathlib import Path
router = APIRouter()

class SongDesc(BaseModel):
    name:str

@router.get("/songs")
async def get_all_songs() -> List[str]:
    song_list = os.listdir("karaoke")
    return song_list

@router.get("/song/lyrics/{song_id}",response_class=FileResponse)
async def get_song_lyrics(song_id):
    return os.path.join("karaoke",song_id,"lyrics.json")

@router.get("/song/accom/{song_id}",response_class=FileResponse)
async def get_song_music(song_id):
    return os.path.join("karaoke",song_id,"accompaniment.wav")

@router.post("/convert")
async def convert(name:str=Body(...),in_file: UploadFile=File(...),):
    print("received")
    song_name = name
    folder_path = "karaoke"
    raw_folder_path = "karaoke_raw"
    raw_file_path = os.path.join(raw_folder_path,song_name+".mp3")
    async with aiofiles.open(raw_file_path, 'wb') as out_file:
        content = await in_file.read()  # async read
        await out_file.write(content)  # async write
    split(raw_file_path,folder_path)
    print("start vocal to lyrics")
    convert2lyrics(os.path.join(folder_path,song_name,"vocals.wav"),os.path.join(folder_path,song_name,"lyrics.json"))
