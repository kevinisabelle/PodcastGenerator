import os, time
from typing import List, Union
from openai import OpenAI
from Entities import Podcast, Section, Chapter

def generate_section(section : Section, chapter : Chapter, podcast_definition : Podcast):
    """
    Generate content for a section using the provided chapter and podcast definition.
    This function should implement the logic to generate meaningful content.
    """
    nb_words = podcast_definition.words_per_minute * section.duration_in_minutes

    # Geneate the prompt that will include the titles and descriptions
    prompt = f"""
    ## Context
    Podcast: {podcast_definition.title}
    Podcast description: {podcast_definition.description}

    Chapter {chapter.id}: {chapter.title}
    – {chapter.description}

    Section {chapter.id}.{section.id}: {section.title}
    – {section.description}

    ## Instructions
    Write an audio-reader script:
    • Language: {podcast_definition.writing_language}
    • Style: {podcast_definition.writing_style}
    • Length: ≈ {nb_words} words (±10 %).
    • Output only the narration.
    • Begin with the section number and title only in {podcast_definition.writing_language}.
    """

    sys_msgs = [
        "You are a senior podcast script writer.",
        "Follow APA punctuation guidelines.",
    ]

    content = get_response(prompt, sys_msgs)

    return content

def get_response(user_prompt: str,
                 system_prompt: Union[str, List[str]] = "You are a podcast-content generator.") -> str:
    """
    Call OpenAI with chat-style messages.

    Parameters
    ----------
    user_prompt : str
        The main prompt you want answered.
    system_prompt : str | list[str]
        One or many system messages.  Defaults to a single
        “podcast-content generator” instruction.

    Returns
    -------
    str
        The assistant’s reply.
    """
    # Normalise system_prompt into a list of messages
    if isinstance(system_prompt, str):
        system_prompt = [system_prompt]

    messages = [{"role": "system", "content": msg} for msg in system_prompt] # type: ignore
    messages.append({"role": "user", "content": user_prompt})

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    start = time.time()
    response = client.chat.completions.create(
        model="o3-mini",
        messages=messages, # type: ignore
    )
    print(f"Completion in {time.time() - start:.2f}s")

    return response.choices[0].message.content