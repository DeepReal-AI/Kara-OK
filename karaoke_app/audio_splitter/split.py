'''Split an mp3 file into .wav files of vocal and accompaniment
'''

import os
from pathlib import Path

def split_audio(input_filepath: Path, output_dir: Path):
    os.system(f"spleeter separate -o \"{output_dir}\" \"{input_filepath}\"")
    print("split done ?")

if __name__ == "__main__":
    test_folder = Path.cwd().joinpath("tests")
    file = "audio_example.mp3"
    split_audio(test_folder.joinpath(file), test_folder.joinpath("output"))
    file = "Baby.mp3"
    split_audio(test_folder.joinpath(file), test_folder.joinpath("output"))
