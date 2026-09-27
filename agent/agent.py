import json
from utils.llm import LLM
from prompts import SYSTEM_PROMPT
# from tools import TOOL_DEFINITIONS, TOOLS
from utils.logger import logger
from agent.state import AgentState
from agent.planner import create_plan
from ingestion.context_builder import build_context
from utils.mcpClient import MCPClient
from utils.config import APPROVAL_REQUIRED, MCP_CLIENT_URI

from .approval import ask_user_for_approval

client = LLM()

MAX_STEPS = 30
MAX_SAME_ACTION = 2
MAX_TEST_RETRIES = 3

def trim_messages(messages, max_chars=18000):

    if len(messages) <= 2:
        return messages

    system_message = messages[0]
    user_message = messages[1]

    history = messages[2:]

    def get_content(message):
        if isinstance(message, dict):
            return message.get("content") or ""

        return getattr(message, "content", "") or ""

    while True:

        candidate = [
            system_message,
            user_message,
            *history
        ]

        total_chars = sum(
            len(get_content(message))
            for message in candidate
        )

        if total_chars <= max_chars:
            return candidate

        if len(history) <= 2:
            return candidate

        # Remove oldest messages
        history = history[2:]
        
def convert_mcp_tools(mcp_tools):

    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.input_schema,
            }
        }
        for tool in mcp_tools
    ]




async def run_agent(user_request):

    state = AgentState(
        task=user_request
    )

    print("\n========== CREATING PLAN ==========\n")

    state.plan = create_plan(
        client,
        user_request
    )

    for i, step in enumerate(state.plan, start=1):
        print(f"{i}. {step}")

    print("\n===================================\n")

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
    async with MCPClient(
        MCP_CLIENT_URI
    ) as mcp:

        print("MCP connected")

        # -----------------------------------------
        # Get tools
        # -----------------------------------------

        mcp_tools = await mcp.list_tools()

        tools = convert_mcp_tools(mcp_tools)
        # -----------------------------------------
        # Agent loop
        # -----------------------------------------

        for step in range(1, MAX_STEPS + 1):

            print()
            print(f"========== STEP {step} ==========")
            messages = trim_messages(
                messages,
                max_chars=18000
            )
            message = client.chat(
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            # -------------------------------------
            # LLM finished
            # -------------------------------------

            if not message.tool_calls:
                return message.content

            # Preserve assistant message
            messages.append(message)

            # -------------------------------------
            # Process tool calls
            # -------------------------------------

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

                # ---------------------------------
                # Repeated action detection
                # ---------------------------------

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

                # ---------------------------------
                # Test retry limit
                # ---------------------------------

                if tool_name == "run_command":

                    if "pytest" in arguments.get(
                        "command",
                        ""
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

                # ---------------------------------
                # Approval
                # ---------------------------------

                if tool_name in APPROVAL_REQUIRED:

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

                # ---------------------------------
                # Execute MCP tool
                # ---------------------------------

                try:

                    result = await mcp.call_tool(
                        tool_name,
                        arguments
                    )

                except Exception as e:

                    logger.exception(
                        f"MCP tool failed: {tool_name}"
                    )

                    result = {
                        "success": False,
                        "error": str(e)
                    }

                # ---------------------------------
                # Track test failures
                # ---------------------------------

                if tool_name == "run_command":

                    if not result.get("success"):

                        test_failures += 1

                    else:

                        test_failures = 0

                # ---------------------------------
                # Send result back to LLM
                # ---------------------------------

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

    return (
        f"Agent stopped after reaching "
        f"the {MAX_STEPS}-step limit."
    )
