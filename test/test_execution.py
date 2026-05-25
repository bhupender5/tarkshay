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