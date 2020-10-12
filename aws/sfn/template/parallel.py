from typing import List

def get_json(branches: List[dict], next_task: str) -> dict:
    return {
        "Type": "Parallel",
        "Branches": branches,
        "OutputPath": "$",
        "InputPath": "$",
        "ResultPath": "$.result",
        "Next": next_task
    }
