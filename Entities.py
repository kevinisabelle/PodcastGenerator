from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import List

@dataclass
class Section:
    """A leaf-level section of a course chapter."""
    id: int
    title: str
    description: str
    duration_in_minutes: int
    content: str = ""


@dataclass
class Chapter:
    """A top-level chapter that contains multiple sections."""
    id: int
    title: str
    description: str
    sections: List[Section] = field(default_factory=list)


@dataclass
class Podcast:
    """Root object representing the whole course."""
    title: str
    description: str
    words_per_minute: int
    writing_language: str = "fr"
    writing_style: str = "conversational"
    chapters: List[Chapter] = field(default_factory=list)

def load_podcast(path: str | Path) -> Podcast:
    """
    Charge un fichier JSON décrivant le cours et retourne
    un objet Course entièrement instancié.
    """
    text = Path(path).read_text(encoding="utf-8")
    data = json.loads(text)

    def to_section(raw: dict) -> Section:
        return Section(
            id=raw["Id"],
            title=raw["Title"],
            description=raw["Description"],
            duration_in_minutes=raw["DurationInMinutes"],
            content=raw.get("Content", "")
        )

    def to_chapter(raw: dict) -> Chapter:
        return Chapter(
            id=raw["Id"],
            title=raw["Title"],
            description=raw["Description"],
            sections=[to_section(s) for s in raw.get("Sections", [])]
        )

    return Podcast(
        title=data["Title"],
        description=data["Description"],
        words_per_minute=data["WordsPerMinute"],
        writing_language=data.get("WritingLanguage", "fr"),
        writing_style=data.get("WritingStyle", "conversational"),
        chapters=[to_chapter(c) for c in data.get("Chapters", [])]
    )

def save_podcast(podcast: Podcast, path: str | Path) -> None:
    """
    Save the podcast object to a JSON file.
    """
    data = {
        "Title": podcast.title,
        "Description": podcast.description,
        "WordsPerMinute": podcast.words_per_minute,
        "WritingLanguage": podcast.writing_language,
        "WritingStyle": podcast.writing_style,
        "Chapters": [
            {
                "Id": chapter.id,
                "Title": chapter.title,
                "Description": chapter.description,
                "Sections": [
                    {
                        "Id": section.id,
                        "Title": section.title,
                        "Description": section.description,
                        "DurationInMinutes": section.duration_in_minutes,
                        "Content": section.content
                    } for section in chapter.sections
                ]
            } for chapter in podcast.chapters
        ]
    }
    Path(path).write_text(json.dumps(data, indent=4), encoding="utf-8")

def get_podcast_duration(podcast: Podcast) -> int:
    """
    Calculate the total duration of the podcast in minutes.
    """
    return sum(
        section.duration_in_minutes
        for chapter in podcast.chapters
        for section in chapter.sections
    )