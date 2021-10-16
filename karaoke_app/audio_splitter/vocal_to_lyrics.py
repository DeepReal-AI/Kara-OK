from .transcribe import transcribe_long_file
from .word_to_sentence import word_to_sentences
from pathlib import Path
import json

def vocal_to_lyrics(speech_filepath: Path, save_path: Path):
    """Transcribe a vocals.wav file into a json file with lyrics data
    
    """
    # convert into Path if the arguments are originally strings
    if type(speech_filepath) == str:
        speech_filepath = Path(speech_filepath)
    if type(save_path) == str:
        save_path = Path(save_path)
    print("transcribing starts")
    word_df = transcribe_long_file(speech_file=speech_filepath)
    print("transcribing done, starting grouping")
    sentence_df = word_to_sentences(data=word_df)
    print("done with grouping words")
    with save_path.open("w") as output_file:
        json.dump(sentence_df, output_file, indent=4)

if __name__ == "__main__":
    vocal_to_lyrics(Path("./tests/output/Baby/vocals.wav"), Path("./tests/output/Baby/data.json"))
