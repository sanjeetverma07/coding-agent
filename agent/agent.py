import json
from utils.llm import LLM
from prompts import SYSTEM_PROMPT
# from tools import TOOL_DEFINITIONS, TOOLS
from utils.logger import logger
from agent.state import AgentState
from agent.planner import create_plan
from ingestion.context_builder import build_context
from utils.mcpClient import MCPClient
from .approval import ask_user_for_approval

mcp_client = MCPClient("http://127.0.0.1:8000/mcp")
client = LLM()

MAX_STEPS = 30
MAX_SAME_ACTION = 2
MAX_TEST_RETRIES = 3


def execute_tool(tool_name, arguments):
    if tool_name not in TOOLS:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }
    try:
        logger.info(f"calling tool {tool_name}")
        result = TOOLS[tool_name](**arguments)
        if (
            tool_name == "search_repository_hybrid"
            and result.get("success")
        ):
            context = build_context(
                result["results"]
            )

            result = {
                "success": True,
                "context": context
            }

        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
        
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


# async def run_agent(request):
#     async with MCPClient(
#         "http://127.0.0.1:8000/mcp"
#     ) as mcp_client:

#         mcp_tools = await mcp_client.list_tools()

async def run_agent(user_request):
    mcp_tools=''
    async with mcp_client as mcp:
        mcp_tools = await mcp.list_tools()
    tools = convert_mcp_tools(mcp_tools)
    state = AgentState(
        task=user_request
    )
    print("\n========== CREATING PLAN ==========\n")
    state.plan = create_plan(client, user_request)
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
    for step in range(1, MAX_STEPS + 1):
        print()
        print(f"========== STEP {step} ==========")
        message = client.chat(
                    messages=messages,
                    tools=tools,
                    # tools=TOOL_DEFINITIONS,
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

            # -----------------------------------------
            # Execute real tool
            # -----------------------------------------
            result=''
            async with mcp_client as mcp:
                result = await mcp_client.call_tool(tool_name, arguments)

            # result = execute_tool(
            #     tool_name,
            #     arguments
            # )


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
 