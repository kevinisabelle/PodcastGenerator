# Load the podcast from json file
from Ai import generate_section
from Entities import load_podcast, get_podcast_duration, save_podcast

jsonfile = "./podcasts/kotlin_forcsharpdev_frqc.json"

podcast_definition = load_podcast(jsonfile)

expected_duration = get_podcast_duration(podcast_definition)
print(f"Expected Podcast Duration: {expected_duration} minutes")

for chapter in podcast_definition.chapters:
    for section in chapter.sections:
        if not section.content or section.content.strip() == "":
            # We need to generate content for this section
            print(f"Generating content for section: {chapter.id}.{section.id}: {section.title}")
            section.content = generate_section(section, chapter, podcast_definition)
            # Save the generated content to the jsonfile in json format
            save_podcast(podcast_definition, jsonfile)
            print(f"Generated content for section: {section.title}")
        else:
            # The content is already provided, so we can use it directly
            pass


# Display the podcast title and description
print(f"Podcast Title: {podcast_definition.title}")
print(f"Podcast Description: {podcast_definition.description}")
