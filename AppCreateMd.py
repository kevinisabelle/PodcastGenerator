from Audio import convert_to_audio_and_save_mp3
from Entities import load_podcast
import os

jsonfile = "./podcasts/cities_skylines2.json"
files_location = "./text_files/"
voice = "fr-FR-Standard-A"

podcast_definition = load_podcast(jsonfile)

md_filename = f"{files_location}{podcast_definition.title}.md"
md_content = f"# {podcast_definition.title}\n\n{podcast_definition.description}\n\n"
md_file = open(md_filename, 'w', encoding='utf-8')

def sanitize_filename(filename: str) -> str:
    """
    Sanitize the filename by removing or replacing invalid characters.
    Also replaces spaces with underscores.
    """
    result = "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in filename)
    return result.strip().replace(" ", "_")


for chapter in podcast_definition.chapters:
    md_content += f"# {chapter.id} - {chapter.title}\n\n"
    md_content += f"{chapter.description}\n\n"
    for section in chapter.sections:
        md_content += f"## {chapter.id}.{section.id} - {section.title}\n\n"
        md_content += f"*{section.description}*\n\n"
        md_content += f"{section.content}\n\n"

# write the markdown content to the file
md_file.write(md_content)
