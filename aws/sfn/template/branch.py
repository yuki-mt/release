def get_json(start: str, states: dict) -> dict:
    return {
        "StartAt": start,
        "States": states
    }
