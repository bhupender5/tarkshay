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