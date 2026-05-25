# `README.md`

````md id="qud1tq"
# Autonomous Meeting-to-Action Engine

AI-powered multi-agent workflow system that converts raw meeting transcripts into actionable engineering artifacts automatically.

---

# Problem Statement

Engineering teams spend hours after meetings creating tickets, documenting technical decisions, assigning tasks, and notifying stakeholders manually.

This project automates the entire post-meeting workflow using AI agents capable of parsing transcripts, extracting actionable intents, generating technical documentation, and executing downstream automation.

---

# Features

- Transcript ingestion and parsing
- Speaker-aware dialogue extraction
- Intent classification using LLMs
- Multi-agent orchestration pipeline
- Project Manager Agent
- Solutions Architect Agent
- QA / Governance Agent
- Human-in-the-loop approval system
- Markdown ticket generation
- System specification generation
- README auto-generation
- Webhook payload delivery
- Streamlit web dashboard
- Real-time pipeline execution display
- Error handling and retry logic

---

# Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| LLM Provider | Groq API |
| Agent Framework | LangGraph |
| UI | Streamlit |
| Parsing | Regex + NLP |
| HTTP Client | httpx |
| Environment | python-dotenv |
| Testing | pytest |
| Deployment | Streamlit Cloud |

---

# Architecture Diagram

```txt id="zl6fgh"
                ┌──────────────────┐
                │ Transcript Input │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Ingestion Layer  │
                │ Parser + Intent  │
                └────────┬─────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Multi-Agent Pipeline │
              └────────┬─────────────┘
                       │
     ┌─────────────────┼─────────────────┐
     ▼                 ▼                 ▼
┌──────────┐   ┌──────────────┐   ┌───────────┐
│ PM Agent │   │ Architect AI │   │ QA Agent  │
└────┬─────┘   └──────┬───────┘   └────┬──────┘
     │                │                │
     └────────────────┼────────────────┘
                      ▼
          ┌───────────────────────┐
          │ Execution Layer       │
          │ Tickets + Specs + API │
          └──────────┬────────────┘
                     ▼
            ┌────────────────┐
            │ Generated Files│
            └────────────────┘
````

---

# Installation and Setup

## Clone Repository

```bash id="5t1qt5"
git clone https://github.com/your-username/meeting-to-action-engine.git
cd meeting-to-action-engine
```

## Create Virtual Environment

### Windows

```bash id="61hz9v"
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash id="0g8jwk"
python3 -m venv venv
source venv/bin/activate
```

---

# Install Dependencies

```bash id="1g33je"
pip install -r requirements.txt
```

---

# Environment Variables

Create `.env`

```env id="h5n52p"
GROQ_API_KEY=your_api_key_here
WEBHOOK_URL=https://webhook.site/your-url
```

---

# Run Locally

```bash id="vq9l3u"
streamlit run app.py
```

---

# Project Structure

```txt id="ym9f8o"
meeting-to-action-engine/
│
├── app.py
├── requirements.txt
├── README.md
├── src/
│   ├── ingestion/
│   ├── agents/
│   ├── execution/
│   └── utils/
│
├── tests/
├── output/
└── docs/
```

---

# Sample Transcript Format

```txt id="d5ckns"
[00:00:01] John: We need authentication APIs by Friday.
[00:00:10] Sarah: Use JWT for token management.
[00:00:20] Mike: QA testing should begin next Monday.
```

---

# Expected Outputs

The system generates:

* `output/SYSTEM_SPEC.md`
* `output/tickets/TICKET-001.md`
* Auto-generated README
* Webhook JSON payloads

---

# Human-in-the-Loop (HITL)

High-risk actions are intercepted by the QA Agent before execution.

Examples:

* Database deletion
* Production changes
* Billing modifications
* External API writes

The user must manually approve or reject these actions inside the Streamlit UI.

---

# Future Improvements

* Live audio transcription
* Real Jira API integration
* GitHub Issues automation
* ChromaDB semantic memory
* Multi-language transcript support
* Persistent long-term agent memory
* Docker deployment
* Kubernetes orchestration

---

# Deployment

Deploy easily using:

* Streamlit Cloud
* Hugging Face Spaces

---

# License

MIT License

````

---

# `tests/test_parser.py`

```python id="8wmc5n"
from src.ingestion.parser import parse_transcript


def test_parse_transcript(tmp_path):

    sample_text = """
[00:00:01] John: Build authentication API
[00:00:05] Sarah: Use JWT tokens
"""

    file_path = tmp_path / "sample.txt"

    file_path.write_text(sample_text)

    utterances = parse_transcript(str(file_path))

    assert len(utterances) == 2

    assert utterances[0].speaker == "John"

    assert utterances[1].text == "Use JWT tokens"
````

---

# `tests/test_agents.py`

```python id="hshuqz"
from src.agents.qa_agent import run_qa_agent


def test_qa_agent():

    pm_output = [
        {
            "title": "Delete production database",
            "description": "Remove old database",
            "priority": "HIGH",
            "assignee": "DevOps"
        }
    ]

    architect_output = """
# Architecture
Uses FastAPI and PostgreSQL
"""

    result = run_qa_agent(
        pm_output=pm_output,
        architect_output=architect_output
    )

    assert result["status"] == "HUMAN_APPROVAL_REQUIRED"

    assert result["high_risk_actions"] == 1
```

---

# `tests/test_execution.py`

```python id="c49ps9"
from pathlib import Path

from src.execution.ticket_generator import generate_tickets


def test_ticket_generation():

    tasks = [
        {
            "title": "Build Login API",
            "description": "Create JWT auth system",
            "assignee": "Backend Team",
            "priority": "HIGH",
            "deadline": "2026-05-30",
            "acceptance_criteria": [
                "Login endpoint works"
            ],
            "labels": ["backend"],
            "story_points": 5
        }
    ]

    generate_tickets(tasks)

    ticket_file = Path(
        "output/tickets/TICKET-001.md"
    )

    assert ticket_file.exists()
```

---

# `tests/test_transcript.txt`

```txt id="o3jlwm"
[00:00:01] John: Build authentication API by Friday.
[00:00:10] Sarah: Use JWT tokens for authentication.
[00:00:20] Mike: QA testing starts Monday.
[00:00:35] Alice: We need webhook integration.
```

---

# `requirements.txt`

```txt id="k7ej5s"
streamlit
openai
python-dotenv
httpx
langgraph
langchain
pytest
```

---

# `.env.example`

```env id="fxh7lf"
GROQ_API_KEY=your_groq_api_key
WEBHOOK_URL=https://webhook.site/your-webhook-url
```

---

# `.gitignore`

```gitignore id="6nl8ll"
venv/
.env
__pycache__/
*.pyc
output/
.idea/
.vscode/
```

---

# `docs/architecture.png`

Create this manually using:

* Draw.io
* Excalidraw
* Figma

Suggested flow:

```txt id="4n2kw6"
Transcript
   ↓
Parser
   ↓
Intent Extraction
   ↓
PM Agent
Architect Agent
QA Agent
   ↓
Execution Layer
   ↓
Tickets + Specs + Webhook
```

Now your project structure is almost fully complete.
