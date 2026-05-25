import time
from typing import List, Dict

from dotenv import load_dotenv
from openai import OpenAI
import os


# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# Groq / OpenAI Client
# ---------------------------------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# ---------------------------------------------------
# Architect Agent
# ---------------------------------------------------

def run_architect_agent(
    intents: List[Dict],
    max_retries: int = 3
):

    if not intents:
        return "# No technical decisions found."

    # ---------------------------------------------------
    # Filter Technical Decisions
    # ---------------------------------------------------

    technical_items = [
        item for item in intents
        if item.get("intent_type") == "TECHNICAL_DECISION"
    ]

    if not technical_items:
        return "# No technical decisions identified."

    # ---------------------------------------------------
    # Prompt
    # ---------------------------------------------------

    system_prompt = """
You are a Senior Solutions Architect.

Your task is to analyze technical meeting decisions and generate a professional
System Requirements Document (SRD).

The document must include:

1. Project Overview
2. Proposed Architecture
3. Database Design
4. API Contracts
5. Scalability Considerations
6. Security Considerations
7. Open Technical Risks
8. Recommended Tech Stack
9. Deployment Strategy
10. Future Improvements

Return ONLY markdown text.

Rules:
- Use proper markdown headings
- Be concise but technical
- Do not return JSON
- Do not explain outside markdown
"""

    # ---------------------------------------------------
    # Retry Logic
    # ---------------------------------------------------

    for attempt in range(max_retries):

        try:

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": str(technical_items)
                    }
                ]
            )

            content = response.choices[0].message.content

            if not content:
                raise ValueError(
                    "Empty architect response"
                )

            return content

        except Exception as e:

            print(
                f"[Architect Retry {attempt+1}] {str(e)}"
            )

        # ---------------------------------------------------
        # Exponential Backoff
        # ---------------------------------------------------

        wait_time = min(2 ** attempt, 60)

        time.sleep(wait_time)

    # ---------------------------------------------------
    # Fallback
    # ---------------------------------------------------

    return """
# System Requirements Document

## Error
Architect Agent failed to generate the specification document.

## Recommended Action
Check API connectivity and retry pipeline execution.
"""