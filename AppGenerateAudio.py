from Audio import convert_to_audio_and_save_mp3
from Entities import load_podcast
import os

jsonfile = "./podcasts/kotlin_forcsharpdev_frqc.json"
files_location = "./audio_files/"
voice = "fr-FR-Standard-A"

podcast_definition = load_podcast(jsonfile)

def sanitize_filename(filename: str) -> str:
    """
    Sanitize the filename by removing or replacing invalid characters.
    Also replaces spaces with underscores.
    """
    result = "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in filename)
    return result.strip().replace(" ", "_")


for chapter in podcast_definition.chapters:
    for section in chapter.sections:
        if not section.content or section.content.strip() == "":
            # No content provided, skip this section
            print(f"Skipping section: {chapter.id}.{section.id}: {section.title} (no content provided)")
        else:
            # Convert the section content to audio
            print(f"Section {chapter.id}.{section.id}: {section.title} has content.")

            # Check if the mp3 file already exists
            filename = f"{sanitize_filename(podcast_definition.title)}-{chapter.id}_{section.id}_{sanitize_filename(section.title)}"

            # Look for existing files in the audio_files directory

            if os.path.exists(os.path.join(files_location, filename + ".mp3")):
                print(f"Audio file {filename} already exists, skipping generation.")
            else:
                print(f"Generating audio for section: {chapter.id}.{section.id}: {section.title}")
                # Convert text to audio and save as MP3

                convert_to_audio_and_save_mp3(
                    text=section.content,
                    filename=filename,
                    files_location=files_location,
                    voice=voice  # Example voice, adjust as needed
                )
