import json
from prompts import PLANNER_SYSTEM_PROMPT
def create_plan(llm, task):
    messages = [
        {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
        {"role": "user", "content": task}
    ]

    default_plan = [
        "Inspect the relevant files",
        "Inspect the related tests",
        "Identify the problem",
        "Modify the required code",
        "Run the tests",
        "Fix any failures",
        "Verify the final result"
    ]

    try:
        response = llm.chat_without_tool(messages=messages)
        data = json.loads(response.content)
        return data["plan"]
    except (json.JSONDecodeError, KeyError, Exception):
        return default_plan