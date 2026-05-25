import re
from dataclasses import dataclass
from typing import List


@dataclass
class Utterance:
    timestamp: str
    speaker: str
    text: str


def parse_transcript(filepath: str) -> List[Utterance]:

    pattern = r"\[(\d{2}:\d{2}:\d{2})\]\s+(.+?):\s+(.+)"

    utterances = []

    with open(filepath, "r", encoding="utf-8") as f:

        for line in f:

            match = re.match(pattern, line.strip())

            if match:

                utterances.append(
                    Utterance(*match.groups())
                )

    return utterances