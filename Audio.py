import os
import time
from google.cloud import texttospeech
import google.auth
import requests

import re



def split_text_into_chunks(text, max_chunk_size=3000):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []

    for sentence in sentences:
        current_chunk_size = sum(len(s) for s in current_chunk)
        if current_chunk_size + len(sentence) <= max_chunk_size:
            current_chunk.append(sentence)
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks




def text_to_mp3(files_path, text, mp3file, tts_client, voice='fr-CA-Standard-C'):
    target_text = text
    target_text_chunks = split_text_into_chunks(target_text, max_chunk_size=500)
    index = 0

    for text in target_text_chunks:
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        voice_config = texttospeech.VoiceSelectionParams(
            language_code='fr-CA', ssml_gender=texttospeech.SsmlVoiceGender.FEMALE, name=voice)
        synthesis_input = texttospeech.SynthesisInput(text=text)

        response = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice_config, audio_config=audio_config
        )

        filename = f"{files_path}{mp3file}{index}.mp3"
        print(f"Saving MP3 file to {filename}...")
        # Save MP3 file
        with open(filename, 'wb') as out:
            out.write(response.audio_content)

        index += 1

    # Merge MP3 files
    print("Merging MP3 files...")
    mp3_files = [f"{files_path}{mp3file}{i}.mp3" for i in range(index)]
    with open(f"{files_path}{mp3file}.mp3", 'wb') as outfile:
        for mp3_file in mp3_files:
            with open(mp3_file, 'rb') as infile:
                outfile.write(infile.read())

    # Delete MP3 files
    print("Deleting MP3 files...")
    for mp3_file in mp3_files:
        os.remove(f"{mp3_file}")

    print(f"Saved MP3 file to {files_path}{mp3file}")


def text_to_mp3_with_open_ai(files_path, text, mp3file, voice):
    target_text = text
    target_text_chunks = split_text_into_chunks(target_text, max_chunk_size=500)
    index = 0

    # curl https://api.openai.com/v1/audio/speech \
    # -H "Authorization: Bearer $OPENAI_API_KEY" \
    # -H "Content-Type: application/json" \
    # -d '{
    #  "model": "tts-1",
    #  "input": "Today is a wonderful day to build something people love!",
    #  "voice": "alloy"
    # }' \
    # --output speech.mp3

    for text in target_text_chunks:
        # use a simple http request to get the audio file using standard httpclient
        response = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers={
                "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                "Content-Type": "application/json"
            },
            json={
                "model": "tts-1",
                "input": text,
                "voice": voice
            }
        )

        filename = f"{files_path}{mp3file}{index}.mp3"
        print(f"Saving MP3 file to {filename}...")

        with open(filename, 'wb') as out:
            out.write(response.content)

        index += 1

    # Merge MP3 files
    print("Merging MP3 files...")
    mp3_files = [f"{files_path}{mp3file}{i}.mp3" for i in range(index)]
    with open(f"{files_path}{mp3file}.mp3", 'wb') as outfile:
        for mp3_file in mp3_files:
            with open(mp3_file, 'rb') as infile:
                outfile.write(infile.read())

    # Delete MP3 files
    print("Deleting MP3 files...")
    for mp3_file in mp3_files:
        os.remove(f"{mp3_file}")

    print(f"Saved MP3 file to {files_path}{mp3file}")




def convert_to_audio_and_save_mp3(text, filename, files_location, voice):
    start_time = time.time()
    creds, _ = google.auth.default()
    tts_client = texttospeech.TextToSpeechClient()

    target_voice = voice

    # Convert text to MP3
    if voice.startswith('fr-'):
        text_to_mp3(files_location, text, filename, tts_client, voice)
    else:
        text_to_mp3_with_open_ai(files_location, text, filename, target_voice)

    total_time = time.time() - start_time
    print(f"Audio generation took {total_time:.2f} seconds for {filename}.mp3")