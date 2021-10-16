from pathlib import Path
import json


def word_to_sentences(word_file: Path=None, data: list=None, save_json: bool=False, save_path: Path=None):
    """Transform list of words to sentences

    Can either pass data in directly, or a path to the file storing the data

    Returns: A list of list (each small list consists of words in a sentence)
    """
    if data is None: 
        if (word_file is None):
            raise Exception("Please input either filepath or data for the function") 
        else:
            with word_file.open("r") as json_file:
                data = json.load(json_file)

    SENT_LENGTH_THRESHOLD = 20
    INTERVAL = 0
    sentences = []
    words = []
    word = ''
    for i in range(len(data)):
        data[i]['startTime'] = data[i]['start_time']
        del data[i]['start_time']
        data[i]['endTime'] = data[i]['end_time']
        del data[i]['end_time']


    for i in range(len(data)):
        data[i]["interval"] = 0
        data[i]['duration'] = data[i]['endTime'] - data[i]['startTime']
    for i in range(1, len(data)):
        data[i]['interval'] = data[i]['startTime'] - data[i - 1]['endTime']

    for i in data:
        if len(word + i['word']) > SENT_LENGTH_THRESHOLD or i['interval'] > INTERVAL:
            sentences.append(words)
            word = i['word']
            words = []
            words.append(i)
        else:
            word += i['word']
            word += ' '
            words.append(i)
    sentences.append(words)

    if not save_json:
        return sentences

    if save_path is None:
        if word_file is None:
            raise Exception("Please input a save path if the word file path is not present")
        else:
            save_path = word_file.parent.joinpath(word_file.stem + "_sentences.json")

    with save_path.open("w") as output_file:
        json.dump(sentences, output_file, indent=4)

    return sentences

if __name__ == "__main__":
    # word_file = Path('/Users/chenlingcui/Desktop/Data-Mining-Project-main/Data-Mining-Project-main/vocals_transcript.json')
    word_file = Path('./tests/output/Baby/vocals_transcript.json')
    print(word_to_sentences(word_file=word_file, save_json=True))

