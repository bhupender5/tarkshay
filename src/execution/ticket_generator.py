from pathlib import Path
from typing import List, Dict


# ---------------------------------------------------
# Output Directory
# ---------------------------------------------------

TICKET_DIR = Path("output/tickets")

TICKET_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ---------------------------------------------------
# Generate Markdown Tickets
# ---------------------------------------------------

def generate_tickets(
    tasks: List[Dict]
):

    if not tasks:
        print("No tasks found for ticket generation.")
        return

    # ---------------------------------------------------
    # Generate One Markdown File Per Task
    # ---------------------------------------------------

    for idx, task in enumerate(tasks, start=1):

        ticket_id = f"TICKET-{idx:03d}"

        filename = TICKET_DIR / f"{ticket_id}.md"

        title = task.get("title", "Untitled Task")
        description = task.get(
            "description",
            "No description provided."
        )
        assignee = task.get("assignee", "Unassigned")
        priority = task.get("priority", "MEDIUM")
        deadline = task.get("deadline", "N/A")

        acceptance_criteria = task.get(
            "acceptance_criteria",
            []
        )

        labels = task.get(
            "labels",
            []
        )

        story_points = task.get(
            "story_points",
            1
        )

        # ---------------------------------------------------
        # Markdown Content
        # ---------------------------------------------------

        markdown_content = f"""# {ticket_id}

## Title
{title}

---

## Description
{description}

---

## Assignee
{assignee}

---

## Deadline
{deadline}

---

## Priority
{priority}

---

## Labels
{", ".join(labels) if labels else "None"}

---

## Story Points
{story_points}

---

## Acceptance Criteria
"""

        # ---------------------------------------------------
        # Add Acceptance Criteria
        # ---------------------------------------------------

        if acceptance_criteria:

            for item in acceptance_criteria:

                markdown_content += f"- {item}\n"

        else:

            markdown_content += "- No acceptance criteria provided.\n"

        # ---------------------------------------------------
        # Write Markdown File
        # ---------------------------------------------------

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(markdown_content)

        print(
            f"Generated ticket: {filename}"
        )