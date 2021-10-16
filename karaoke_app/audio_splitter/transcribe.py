import os
from pathlib import Path
import json
import wave
from google.cloud import storage
from google.cloud import speech

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# google authentication, ensure that this file lies outside of the entire source code folder
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(Path.cwd().parent.parent.joinpath("key.json"))
bucket_name = "karaoke_app_bucket"

def frame_rate_channel(audio_file_name: str):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate, channels

def transcribe_file(speech_file: Path, content: bytes=None, save_json: bool=False, save_path: Path=None) -> list:
    """Transcribe a short (<60s) given audio file asynchronously. 
    
    The audio file is assumed to have `.wav` format with proper header
    
    """
    if content is None:
        if (speech_file is None):
            raise Exception("Please input either filepath or data for the function") 
        else:
            with speech_file.open("rb") as audio_file:
                content = audio_file.read()

    client = speech.SpeechClient()

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    audio = speech.RecognitionAudio(content=content)

    frame_rate, channels = frame_rate_channel(str(speech_file))

    config = speech.RecognitionConfig(
        language_code="en-US",
        enable_word_time_offsets=True,
        sample_rate_hertz=frame_rate,
        audio_channel_count=channels,
        model="video",
        use_enhanced=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    logger.info("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    df = []
    for i in range(len(response.results)):
        transcript_result = response.results[i].alternatives[0]
        # The first alternative is the most likely one for this portion.
        logger.debug("Transcript: {%s}", transcript_result.transcript)
        logger.debug("Confidence: {%s}", transcript_result.confidence)
        
        word_df = [*map(lambda word: {
            "word": word.word,
            "start_time": word.start_time.total_seconds(),
            "end_time": word.end_time.total_seconds(),
            }, transcript_result.words
        )]
        df.extend(word_df)

    if not save_json:
        return df

    if save_path is None:
        if speech_file is None:
            raise Exception("Please input a save path if the word file path is not present")
        else:
            save_path = speech_file.parent.joinpath(speech_file.stem + "_transcript.json")

    with save_path.open("w") as output_file:
        json.dump(df, output_file, indent=4)

    return df

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

def transcribe_long_file(speech_file: Path, content: bytes=None, save_json: bool=False, save_path: Path=None) -> list:
    """Transcribe a given audio file (<480minutes) asynchronously.
    
    The audio file is assumed to have `.wav` format with proper header
    
    """
    if content is None:
        if (speech_file is None):
            raise Exception("Please input either filepath or data for the function") 
        else:
            with speech_file.open("rb") as audio_file:
                content = audio_file.read()

    audio_file_name = speech_file.name
    destination_blob_name = audio_file_name
    
    upload_blob(bucket_name, speech_file, destination_blob_name)
    
    gcs_uri = 'gs://' + bucket_name + '/' + audio_file_name


    frame_rate, channels = frame_rate_channel(str(speech_file))

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        language_code="en-US",
        enable_word_time_offsets=True,
        sample_rate_hertz=frame_rate,
        audio_channel_count=channels,
        model="video",
        use_enhanced=True,)

    # Detects speech in the audio file
    operation = client.long_running_recognize(config=config, audio=audio)

    logger.info("Waiting for operation to complete...")
    response = operation.result(timeout=10000)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    df = []
    for i in range(len(response.results)):
        transcript_result = response.results[i].alternatives[0]
        # The first alternative is the most likely one for this portion.

        logger.debug("Transcript: {%s}", transcript_result.transcript)
        logger.debug("Confidence: {%s}", transcript_result.confidence)
        
        word_df = [*map(lambda word: {
            "word": word.word,
            "start_time": word.start_time.total_seconds(),
            "end_time": word.end_time.total_seconds(),
            }, transcript_result.words
        )]
        df.extend(word_df)

    with speech_file.parent.joinpath(speech_file.stem + "_transcript.json").open("w") as output_file:
        json.dump(df, output_file, indent=4)
    
    delete_blob(bucket_name, destination_blob_name)

    if not save_json:
        return df

    if save_path is None:
        if speech_file is None:
            raise Exception("Please input a save path if the word file path is not present")
        else:
            save_path = speech_file.parent.joinpath(speech_file.stem + "_transcript.json")

    with save_path.open("w") as output_file:
        json.dump(df, output_file, indent=4)

    return df

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    short_speech_file = Path('./tests/output/audio_example/vocals.wav')
    print(transcribe_file(short_speech_file, save_json=True))

    long_speech_file = Path('./tests/output/Baby/vocals.wav')
    print(transcribe_long_file(long_speech_file, save_json=True))
