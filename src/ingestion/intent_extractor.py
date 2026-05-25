import os
import json
import time
from typing import List

from dotenv import load_dotenv
from openai import OpenAI

from src.ingestion.parser import Utterance

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def extract_intents(
    utterances: List[Utterance],
    max_retries: int = 3
):

    if not utterances:
        return []

    
    transcript_text = "\n".join(
        [
            f"[{u.timestamp}] {u.speaker}: {u.text}"
            for u in utterances
        ]
    )

    

    system_prompt = """
You are an AI meeting analysis assistant.

Your task is to classify meeting transcript segments into one of:

1. ACTION_ITEM
2. TECHNICAL_DECISION
3. OPEN_QUESTION
4. CONTEXT

Return ONLY valid JSON.

Expected JSON format:

{
  "items": [
    {
      "speaker": "John",
      "timestamp": "00:10:12",
      "text": "We should build the auth API by Friday",
      "intent_type": "ACTION_ITEM",
      "summary": "Build authentication API",
      "priority": "HIGH"
    }
  ]
}

Rules:
- Return valid JSON only
- No markdown
- No explanation text
- Every utterance must have an intent
- Priority should be HIGH, MEDIUM, or LOW
"""



    for attempt in range(max_retries):

        try:

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0.2,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": transcript_text
                    }
                ]
            )

            content = response.choices[0].message.content

           

            parsed = json.loads(content)

            

            if "items" not in parsed:
                raise ValueError(
                    "Missing 'items' key in response"
                )

            return parsed["items"]

        except json.JSONDecodeError:

            print(
                f"[Retry {attempt+1}] Invalid JSON received"
            )

        except Exception as e:

            print(
                f"[Retry {attempt+1}] Error: {str(e)}"
            )

        # ---------------------------------------------------
        # Exponential Backoff
        # ---------------------------------------------------

        wait_time = min(2 ** attempt, 60)

        time.sleep(wait_time)

    # ---------------------------------------------------
    # Final Failure
    # ---------------------------------------------------

    return [
        {
            "speaker": "SYSTEM",
            "timestamp": "00:00:00",
            "text": "Intent extraction failed",
            "intent_type": "CONTEXT",
            "summary": "LLM extraction failed after retries",
            "priority": "LOW"
        }
    ]