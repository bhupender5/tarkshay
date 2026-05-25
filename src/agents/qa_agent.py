from typing import List, Dict



def run_qa_agent(
    pm_output: List[Dict],
    architect_output: str
):

    actions = []


    for idx, task in enumerate(pm_output):

        risk_level = "LOW"

        title = task.get("title", "").lower()
        description = task.get("description", "").lower()

        # ---------------------------------------------------
        # High-Risk Keyword Detection
        # ---------------------------------------------------

        high_risk_keywords = [
            "delete",
            "drop database",
            "production",
            "payment",
            "billing",
            "shutdown",
            "remove",
            "critical",
            "admin access",
            "security",
            "live api",
            "external api",
            "migration"
        ]

        for keyword in high_risk_keywords:

            if keyword in title or keyword in description:
                risk_level = "HIGH"
                break

        # ---------------------------------------------------
        # Medium Risk Rules
        # ---------------------------------------------------

        if (
            task.get("priority") == "HIGH"
            and risk_level != "HIGH"
        ):
            risk_level = "MEDIUM"

        # ---------------------------------------------------
        # Missing Fields Check
        # ---------------------------------------------------

        missing_fields = []

        required_fields = [
            "title",
            "description",
            "assignee",
            "priority"
        ]

        for field in required_fields:

            if not task.get(field):
                missing_fields.append(field)

        # ---------------------------------------------------
        # Build QA Action
        # ---------------------------------------------------

        action = {
            "id": idx + 1,
            "task_title": task.get("title"),
            "risk_level": risk_level,
            "status": (
                "REVIEW_REQUIRED"
                if risk_level == "HIGH"
                else "APPROVED"
            ),
            "summary": (
                f"Task '{task.get('title')}' "
                f"requires {risk_level} risk review."
            ),
            "missing_fields": missing_fields
        }

        actions.append(action)

    # ---------------------------------------------------
    # Architect Output Validation
    # ---------------------------------------------------

    architect_review = {
        "document_present": bool(architect_output),
        "contains_architecture": (
            "architecture" in architect_output.lower()
        ),
        "contains_security": (
            "security" in architect_output.lower()
        ),
        "contains_scalability": (
            "scalability" in architect_output.lower()
        )
    }

    # ---------------------------------------------------
    # Final QA Decision
    # ---------------------------------------------------

    high_risk_count = len(
        [
            a for a in actions
            if a["risk_level"] == "HIGH"
        ]
    )

    final_status = (
        "HUMAN_APPROVAL_REQUIRED"
        if high_risk_count > 0
        else "APPROVED"
    )

    # ---------------------------------------------------
    # Final Response
    # ---------------------------------------------------

    return {
        "status": final_status,
        "total_tasks_reviewed": len(pm_output),
        "high_risk_actions": high_risk_count,
        "actions": actions,
        "architect_review": architect_review
    }