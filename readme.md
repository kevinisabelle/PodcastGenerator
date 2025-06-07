# Podcast Generator

**Disclaimer**: Use only for educational purposes. Do not use this code to participate in AI slop taking over the world.

## Usage

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a json file with your desired chapters and sections.
   You can generate you file using any LLM you like to create the outline that the generator will use to create the podcast.
   Use this JSON schema to output your file in the proper format form the LLM:
   ```json
   {
     "$schema": "https://json-schema.org/draft/2020-12/schema",
     "title": "Audio Course Outline",
     "type": "object",
     "required": [
       "Title",
       "Description",
       "WordsPerMinute",
       "WritingLanguage",
       "WritingStyle",
       "Chapters"
     ],
     "properties": {
       "Title": { "type": "string" },
       "Description": { "type": "string" },
       "WordsPerMinute": { "type": "integer", "minimum": 1 },
       "WritingLanguage": { "type": "string" },
       "WritingStyle": { "type": "string" },
       "Chapters": {
         "type": "array",
         "minItems": 1,
         "items": { "$ref": "#/$defs/Chapter" }
       }
     },
     "additionalProperties": false,
   
     "$defs": {
       "Chapter": {
         "type": "object",
         "required": ["Id", "Title", "Description", "Sections"],
         "properties": {
           "Id": { "type": "integer", "minimum": 1 },
           "Title": { "type": "string" },
           "Description": { "type": "string" },
           "Sections": {
             "type": "array",
             "minItems": 1,
             "items": { "$ref": "#/$defs/Section" }
           }
         },
         "additionalProperties": false
       },
   
       "Section": {
         "type": "object",
         "required": ["Id", "Title", "Description", "DurationInMinutes"],
         "properties": {
           "Id": { "type": "integer", "minimum": 1 },
           "Title": { "type": "string" },
           "Description": { "type": "string" },
           "DurationInMinutes": { "type": "integer", "minimum": 1 },
           "Content": { "type": "string" }
         },
         "additionalProperties": false
       }
     }
   }
   
   ```
3. Edit the AppGenerate.py and set your json file path:
   ```python
   jsonfile = "./podcasts/kotlin_forcsharpdev_frqc.json"
   ```
   
4. Run the script and wait a gazillion years for the AI to generate your podcast:
   ```bash
    python AppGenerate.py
    ```
   
5. Edit the AppGenerateAudio.py and set your json file path and other parameters:
   ```python
   jsonfile = "./podcasts/kotlin_forcsharpdev_frqc.json"
   files_location = "./audio_files/"
   voice = "fr-FR-Standard-A"
   ```
6. Run the script to generate the audio files:
   ```bash
    python AppGenerateAudio.py
    ```
   
Yay! You now have a podcast generated from your json file. You can listen to it using any audio player.
