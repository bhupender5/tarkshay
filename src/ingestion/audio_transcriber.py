import whisper
from pathlib import Path


model = whisper.load_model("base")


def transcribe_audio(audio_path: str) -> str:

    result = model.transcribe(audio_path)

    transcript = result["text"]

    output_path = Path("output/generated_transcript.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    return transcript