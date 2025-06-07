import os

files_location = "./audio_files/"
mp3_file_prefix = "Bien_jouer_à_Cities__Skylines_2___Cours_audio_complet"

mp3_files = [f for f in os.listdir(files_location) if f.startswith(mp3_file_prefix) and f.endswith('.mp3')]
# Sort the files to ensure they are in the correct order
mp3_files.sort()

with open(f"{files_location}{mp3_file_prefix}.mp3", 'wb') as outfile:
    for mp3_file in mp3_files:
        with open(os.path.join(files_location, mp3_file), 'rb') as infile:
            outfile.write(infile.read())
