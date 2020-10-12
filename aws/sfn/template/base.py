def get_json(start: str, states: dict) -> dict:
    return {
        "Comment": "Samle ECS Workflow",
        "StartAt": start,
        "TimeoutSeconds": 600,
        "States": states
    }
