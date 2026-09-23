import json

from utils.llm import LLM
from prompts import SYSTEM_PROMPT
from tools import TOOL_DEFINITIONS, TOOLS
from utils.logger import logger

client = LLM()

MAX_STEPS = 15
MAX_SAME_ACTION = 2
MAX_TEST_RETRIES = 3

def ask_user_for_approval(tool_name, arguments):

    print("\n")
    print("=" * 60)
    print("APPROVAL REQUIRED")
    print("=" * 60)

    if tool_name == "replace_in_file":

        print(f"File: {arguments['path']}")

        print("\n------- OLD -------")
        print(arguments["old"])

        print("\n------- NEW -------")
        print(arguments["new"])

    elif tool_name == "write_file":

        print(f"File: {arguments['path']}")

        print("\n------- NEW FILE CONTENT -------")
        print(arguments["content"])

    elif tool_name == "run_command":

        print(
            f"Command: {arguments['command']}"
        )

    answer = input(
        "\nAllow this action? (yes/no): "
    ).strip().lower()

    return answer in {"yes", "y"}


def execute_tool(tool_name, arguments):

    if tool_name not in TOOLS:

        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    try:
        logger.info(f"calling tool {tool_name}")
        tool = TOOLS[tool_name]
        result = tool(**arguments)
        return result

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

def run_agent(user_request):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_request
        }
    ]

    executed_actions = []
    test_failures = 0
    for step in range(1, MAX_STEPS + 1):
        print()
        print(f"========== STEP {step} ==========")
        message = client.chat(
                    messages=messages,
                    tools=TOOL_DEFINITIONS,
                    tool_choice="auto"
                )
        # -----------------------------------------
        # LLM has finished
        # -----------------------------------------
        if not message.tool_calls:
            return message.content

        # Preserve assistant tool call
        messages.append(message)

        # -----------------------------------------
        # Process tool calls
        # -----------------------------------------
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            try:
                arguments = json.loads(
                    tool_call.function.arguments
                )

            except json.JSONDecodeError:
                result = {
                    "success": False,
                    "error": "Invalid JSON arguments"
                }

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
                continue
            # -----------------------------------------
            # Repeated action detection
            # -----------------------------------------
            action = (
                tool_name,
                json.dumps(
                    arguments,
                    sort_keys=True
                )
            )

            if executed_actions.count(action) >= MAX_SAME_ACTION:
                result = {
                    "success": False,
                    "error": (
                        "This exact action has been "
                        "performed too many times."
                    )
                }
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
                continue

            # -----------------------------------------
            # Limit test retries
            # -----------------------------------------

            if tool_name == "run_command":
                if (
                    "pytest" in arguments.get(
                        "command",
                        ""
                    )
                ):
                    if test_failures >= MAX_TEST_RETRIES:
                        result = {
                            "success": False,
                            "error": (
                                "Maximum test retries reached."
                            )
                        }
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result)
                        })
                        continue

            # -----------------------------------------
            # Require approval for dangerous actions
            # -----------------------------------------

            if tool_name in {
                "write_file",
                "replace_in_file",
                "run_command"
            }:
                approved = ask_user_for_approval(
                    tool_name,
                    arguments
                )
                if not approved:
                    result = {
                        "success": False,
                        "error": (
                            "User rejected this action."
                        )
                    }
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })
                    continue
            executed_actions.append(action)
            print(
                f"\nExecuting: {tool_name}"
            )

            print(
                f"Arguments: {arguments}"
            )


            # -----------------------------------------
            # Execute real tool
            # -----------------------------------------

            result = execute_tool(
                tool_name,
                arguments
            )


            # -----------------------------------------
            # Track test failures
            # -----------------------------------------

            if tool_name == "run_command":
                if not result.get("success"):
                    test_failures += 1
                else:
                    test_failures = 0

            # -----------------------------------------
            # Return observation to LLM
            # -----------------------------------------

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })


    return (
        f"Agent stopped after reaching "
        f"the {MAX_STEPS}-step limit."
    )
 