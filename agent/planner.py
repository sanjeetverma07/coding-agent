import json
from prompts import PLANNER_SYSTEM_PROMPT

def create_plan(llm, task):

    messages = [
        {
            "role": "system",
            "content": PLANNER_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": task
        }
    ]
    response = llm.chat(
        messages=messages
    )
    try:
        data = json.loads(response.content)
        return data["plan"]
    except Exception:
        return [
            "Inspect the relevant files",
            "Inspect the related tests",
            "Identify the problem",
            "Modify the required code",
            "Run the tests",
            "Fix any failures",
            "Verify the final result"
        ]