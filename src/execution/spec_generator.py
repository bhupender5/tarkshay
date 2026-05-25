from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_system_spec(architect_output: str):

    spec_file = OUTPUT_DIR / "SYSTEM_SPEC.md"

    with open(spec_file, "w", encoding="utf-8") as f:
        f.write(architect_output)

    print(f"SYSTEM_SPEC.md generated at {spec_file}")


def generate_readme(project_name: str, architect_output: str):

    readme_file = Path("README.md")

    readme_content = f"""
# {project_name}

## Project Overview

AI-powered Meeting-to-Action Engine.

## Features

- Transcript Parsing
- Intent Extraction
- PM Agent
- Architect Agent
- QA Agent
- Ticket Generation
- Webhook Delivery

## Run Locally

streamlit run app.py

## Environment Variables

GROQ_API_KEY=your_key
WEBHOOK_URL=your_url

## Architecture Notes

{architect_output}

## License

MIT License
"""

    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"README.md generated at {readme_file}")