from typing import Dict, List

from src.agents.pm_agent import run_pm_agent
from src.agents.architect_agent import run_architect_agent
from src.agents.qa_agent import run_qa_agent


# ---------------------------------------------------
# Main Agent Pipeline
# ---------------------------------------------------

def run_agent_pipeline(
    transcript: List,
    intents: List[Dict]
):

    # ---------------------------------------------------
    # Shared State
    # ---------------------------------------------------

    state = {
        "transcript": transcript,
        "intents": intents,
        "pm_output": None,
        "architect_output": None,
        "qa_output": None,
        "final_artifacts": []
    }

    # ---------------------------------------------------
    # Step 1 - PM Agent
    # ---------------------------------------------------

    print("\n========== PM AGENT ==========\n")

    pm_output = run_pm_agent(intents)

    state["pm_output"] = pm_output

    # ---------------------------------------------------
    # Step 2 - Architect Agent
    # ---------------------------------------------------

    print("\n====== ARCHITECT AGENT ======\n")

    architect_output = run_architect_agent(intents)

    state["architect_output"] = architect_output

    # ---------------------------------------------------
    # Step 3 - QA Agent
    # ---------------------------------------------------

    print("\n========== QA AGENT ==========\n")

    qa_output = run_qa_agent(
        pm_output=pm_output,
        architect_output=architect_output
    )

    state["qa_output"] = qa_output

    # ---------------------------------------------------
    # Final State
    # ---------------------------------------------------

    return state