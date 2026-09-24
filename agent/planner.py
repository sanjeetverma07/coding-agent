import json


PLANNER_SYSTEM_PROMPT = """
You are a software engineering planning assistant.

Create a short plan for the coding task.

Return ONLY valid JSON:

{
    "plan": [
        "step 1",
        "step 2",
        "step 3"
    ]
}

Do not write code.
"""


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