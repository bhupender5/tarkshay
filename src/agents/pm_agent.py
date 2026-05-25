import json
import time
from typing import List, Dict

from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# Groq / OpenAI Client
# ---------------------------------------------------

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# ---------------------------------------------------
# PM Agent
# ---------------------------------------------------

def run_pm_agent(
    intents: List[Dict],
    max_retries: int = 3
):

    if not intents:
        return []

    # ---------------------------------------------------
    # Filter Action Items
    # ---------------------------------------------------

    action_items = [
        item for item in intents
        if item.get("intent_type") == "ACTION_ITEM"
    ]

    if not action_items:
        return []

    # ---------------------------------------------------
    # Prompt
    # ---------------------------------------------------

    system_prompt = """
You are a Senior Technical Project Manager.

Your job is to convert meeting action items into structured engineering tasks.

For each task return:
- title
- description
- assignee
- deadline
- priority
- acceptance_criteria
- labels
- story_points

Return ONLY valid JSON.

Expected Format:

{
  "tasks": [
    {
      "title": "Build Authentication API",
      "description": "Develop JWT-based authentication endpoints",
      "assignee": "Backend Team",
      "deadline": "2026-05-30",
      "priority": "HIGH",
      "acceptance_criteria": [
        "Login endpoint works",
        "JWT token generation implemented"
      ],
      "labels": [
        "backend",
        "authentication"
      ],
      "story_points": 5
    }
  ]
}

Rules:
- Return valid JSON only
- No markdown
- No explanations
- Priority must be HIGH, MEDIUM, or LOW
"""

    # ---------------------------------------------------
    # Retry Logic
    # ---------------------------------------------------

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
                        "content": json.dumps(
                            action_items,
                            indent=2
                        )
                    }
                ]
            )

            content = response.choices[0].message.content

            parsed = json.loads(content)

            if "tasks" not in parsed:
                raise ValueError(
                    "Missing tasks key"
                )

            return parsed["tasks"]

        except json.JSONDecodeError:

            print(
                f"[PM Agent Retry {attempt+1}] Invalid JSON"
            )

        except Exception as e:

            print(
                f"[PM Agent Retry {attempt+1}] {str(e)}"
            )

        # ---------------------------------------------------
        # Exponential Backoff
        # ---------------------------------------------------

        wait_time = min(2 ** attempt, 60)

        time.sleep(wait_time)

    # ---------------------------------------------------
    # Fallback
    # ---------------------------------------------------

    return [
        {
            "title": "PM Agent Failure",
            "description": "Task generation failed",
            "assignee": "System",
            "deadline": "N/A",
            "priority": "LOW",
            "acceptance_criteria": [],
            "labels": ["system"],
            "story_points": 1
        }
    ]
