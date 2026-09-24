# 🤖 AI Software Engineering Agent

An AI-powered software engineering agent that can inspect a codebase, understand a development task, plan the required work, modify source files, run tests, and iteratively fix issues based on test results.

The project is being built from the ground up to understand **how coding agents actually work internally**, rather than relying entirely on an existing agent framework.

---

## 🚀 Overview

The agent accepts a software engineering request such as:

> "Fix the authentication test failure in this repository."

Instead of following a hardcoded sequence of operations, the agent uses an LLM to dynamically decide what it needs to do.

A typical execution looks like:

```text
User Request
     │
     ▼
Agent Controller
     │
     ├── Create Task Plan
     │
     ├── Maintain Agent State
     │
     ▼
    LLM
     │
     ▼
 Decide Next Action
     │
     ├── list_files
     ├── read_file
     ├── search_code
     ├── write_file
     ├── replace_in_file
     └── run_command
             │
             ▼
        Tool Executor
             │
             ▼
        Tool Result
             │
             ▼
            LLM
             │
             └──────► Continue / Modify / Test / Finish
```

The core idea is:

> **The LLM decides what should happen. The agent runtime controls how and whether that action is executed.**

---

# ✨ Features

### Repository understanding

The agent can:

* List repository files
* Read source files
* Search for code patterns
* Inspect relevant parts of a repository
* Use tool results as context for subsequent decisions

### Planning

Before executing the task, the agent creates a structured plan containing steps such as:

```text
1. Inspect the relevant files
2. Inspect the related tests
3. Identify the problem
4. Modify the required code
5. Run the tests
6. Fix any failures
7. Verify the final result
```

The plan is represented as structured state rather than being kept only as natural-language conversation.

### Code modification

The agent can:

* Create new files
* Replace existing code
* Make targeted modifications
* Refuse ambiguous replacements

For example, `replace_in_file` verifies that the target text occurs exactly once before changing the file.

### Command execution

The agent can execute repository commands such as:

```bash
pytest
```

Command execution is controlled by the agent runtime and can require human approval.

### Human approval

Potentially destructive operations require explicit approval.

Examples:

```text
write_file
replace_in_file
run_command
```

This prevents the LLM from directly making uncontrolled changes to the development environment.

### Test-driven iteration

The agent can follow an iterative development loop:

```text
Modify
  ↓
Run tests
  ↓
Observe failure
  ↓
Analyze failure
  ↓
Modify again
  ↓
Run tests
  ↓
Verify
```

The agent does not assume that its first modification is correct.

### Safety controls

The runtime includes safeguards such as:

* Maximum agent steps
* Maximum test retries
* Repository path validation
* Safe file access
* Tool argument validation
* Repeated-action detection
* Controlled command execution
* Human approval for modifications

---

# 🧠 Agent Architecture

The system is intentionally divided into several responsibilities.

```text
                    ┌────────────────────┐
                    │    User Request    │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │  Agent Controller  │
                    └─────────┬──────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
        ┌───────────────┐           ┌───────────────┐
        │    Planner    │           │  Agent State  │
        └───────────────┘           └───────────────┘
                │                           │
                └─────────────┬─────────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │        LLM         │
                    └─────────┬──────────┘
                              │
                       Tool decision
                              │
                              ▼
                    ┌────────────────────┐
                    │    Tool Executor   │
                    └─────────┬──────────┘
                              │
          ┌───────────┬───────┼───────────┬───────────┐
          ▼           ▼       ▼           ▼           ▼
      list_files  read_file  search_code  modify    run_command
                                              │
                                              ▼
                                         Repository
                                              │
                                              ▼
                                         Tool Result
                                              │
                                              └──────► LLM
```

---

# 🔄 Agent Execution Loop

The core agent loop is intentionally simple.

```python
while steps < MAX_STEPS:

    response = llm(messages)

    if response contains tool call:

        tool_name = response.tool_name
        arguments = response.arguments

        validate_tool_call()

        if approval_required(tool_name):
            ask_for_approval()

        result = execute_tool(
            tool_name,
            arguments
        )

        messages.append(response)

        messages.append({
            "role": "tool",
            "tool_call_id": response.tool_call_id,
            "content": result
        })

        continue

    return response
```

The loop continues until the LLM determines that the task is complete or the runtime reaches its safety limits.

---

# 🔧 Available Tools

The agent currently exposes repository tools to the LLM.

## `list_files`

Lists files available inside the repository.

Example:

```text
list_files()
```

Useful when the agent does not yet know the repository structure.

---

## `read_file`

Reads the contents of a repository file.

Example:

```text
read_file("auth.py")
```

The agent uses this after discovering potentially relevant files.

---

## `search_code`

Searches the repository for a specific code pattern.

Example:

```text
search_code("verify_token")
```

This is useful for finding:

* Function definitions
* Imports
* Variable names
* Class names
* Configuration references
* Test references

---

## `write_file`

Creates or overwrites a repository file.

The operation is protected by the agent's approval mechanism and repository path validation.

---

## `replace_in_file`

Performs a targeted replacement inside an existing file.

The operation verifies that the requested text appears exactly once.

For example:

```text
old:

payload = verify_token(token)

new:

payload = verify_token(token)
return payload
```

If the old content does not exist, the operation fails safely.

If it appears multiple times, the operation also refuses to make the change automatically.

---

## `run_command`

Executes a repository command.

For example:

```bash
pytest
```

This allows the agent to validate its changes instead of simply assuming they work.

---

# 🛡️ Safety Model

An important design principle is that the LLM should **not have unrestricted control over the machine**.

The architecture separates:

```text
LLM Decision
      │
      ▼
Runtime Validation
      │
      ▼
Permission / Approval
      │
      ▼
Tool Execution
```

For example, the LLM may decide:

```text
replace_in_file(...)
```

But the runtime decides whether that operation is allowed.

This separation makes the system safer and easier to control.

---

# 👤 Human-in-the-Loop

The agent asks for approval before potentially impactful operations.

Example:

```text
Agent wants to execute:

pytest

Approve? [y/n]
```

Or:

```text
Agent wants to modify:

auth.py

Approve? [y/n]
```

This provides a controlled development environment while still allowing the LLM to reason autonomously.

---

# 🧩 Agent State

The agent maintains structured state during execution.

```python
@dataclass
class AgentState:

    task: str

    plan: list[str]

    current_step: int

    files_inspected: list[str]

    changes_made: list[dict]

    tests_run: list[dict]

    completed: bool

    failed: bool
```

This allows the agent to maintain information about what it has already done.

For example:

```text
Task
 └── Fix authentication test

Plan
 ├── Inspect auth.py
 ├── Inspect test_auth.py
 ├── Identify mismatch
 ├── Modify implementation
 └── Run pytest

Files inspected
 ├── auth.py
 └── test_auth.py

Changes made
 └── auth.py

Tests run
 └── pytest

Completed
 └── true
```

This is different from simply storing everything as an unstructured conversation.

---

# 🗺️ Planning

The planner creates a structured task plan before the main execution loop.

The planner returns JSON such as:

```json
{
  "plan": [
    "Inspect the relevant files",
    "Inspect the related tests",
    "Identify the problem",
    "Modify the required code",
    "Run the tests",
    "Fix any failures",
    "Verify the final result"
  ]
}
```

The planner **does not modify the repository**.

Its responsibility is to turn a high-level task into a sequence of engineering objectives.

The execution agent is still responsible for deciding exactly which tools to use.

---

# 🔁 Planning vs Execution

Planning and execution are intentionally separate.

```text
                 User Task
                     │
                     ▼
                ┌─────────┐
                │ Planner │
                └────┬────┘
                     │
                     ▼
                   Plan
                     │
                     ▼
              ┌─────────────┐
              │ Agent Loop  │
              └──────┬──────┘
                     │
             Dynamic decisions
                     │
                     ▼
                  Tools
                     │
                     ▼
                Repository
```

The plan provides direction.

The agent loop handles the actual execution.

This means the agent can adapt when reality differs from the original plan.

For example:

```text
Plan:
    Run tests

Actual result:
    Tests fail

Agent:
    Investigate failure

New action:
    Read failing test

New action:
    Read implementation

New action:
    Modify implementation

New action:
    Run tests again
```

---

# 🧪 Example Task

Suppose the repository contains:

### `auth.py`

```python
def create_token():
    return {
        "user_id": 123
    }


def verify_token(token):
    return token
```

### `app.py`

```python
from auth import verify_token


def authenticate(token):

    payload = verify_token(token)

    return payload["user_id"]
```

### `test_auth.py`

```python
def test_authenticate():

    user_id = authenticate(token)

    assert user_id == "123"
```

The test expects:

```text
"123"
```

while the implementation produces:

```text
123
```

The agent can:

```text
1. Inspect repository
2. Find authentication files
3. Read implementation
4. Read tests
5. Identify type mismatch
6. Propose modification
7. Request approval
8. Modify code
9. Run pytest
10. Observe result
11. Fix if required
12. Run pytest again
13. Return final result
```

---

# 🔍 Why This Is an Agent

A traditional scripted automation might look like:

```python
read_file("auth.py")
replace_in_file(...)
run_command("pytest")
```

The sequence is predetermined.

This system instead allows the LLM to decide:

```text
What should I inspect?
        ↓
Which tool should I use?
        ↓
What did I learn?
        ↓
What should I do next?
```

For example:

```text
User:
"Fix the authentication issue."

LLM:
list_files()

Observation:
auth.py
app.py
test_auth.py

LLM:
read_file("test_auth.py")

Observation:
test expects string user ID

LLM:
read_file("auth.py")

Observation:
user ID is integer

LLM:
modify implementation

Runtime:
request approval

User:
approve

Runtime:
execute modification

LLM:
run pytest

Observation:
tests pass

LLM:
final response
```

The next action is determined dynamically based on observations.

---

# 🧱 Project Structure

A simplified project structure is:

```text
ai-software-engineering-agent/
│
├── main.py
│
├── agent/
│   ├── runtime.py
│   ├── state.py
│   └── planner.py
│
├── tools/
│   ├── filesystem.py
│   ├── search.py
│   └── execution.py
│
├── utils/
│   └── llm.py
│
├── test_repo/
│   ├── auth.py
│   ├── app.py
│   └── test_auth.py
│
└── README.md
```

The exact structure may evolve as the agent gains additional capabilities.

---

# ⚙️ Core Design Principles

## 1. LLM decides, runtime controls

The LLM determines the next action.

The runtime determines whether that action can actually be performed.

---

## 2. Tools are the agent's interface to the environment

The LLM does not directly access the filesystem or execute commands.

Instead:

```text
LLM
 ↓
Tool Call
 ↓
Runtime
 ↓
Tool
 ↓
Result
 ↓
LLM
```

---

## 3. Observations drive decisions

The agent should not assume that an operation succeeded.

It receives the actual result:

```text
Tool → Result → LLM
```

and decides what to do next.

---

## 4. Tests are feedback

Tests are not only a final verification step.

They provide feedback that can drive additional agent actions.

```text
Change
  ↓
Test
  ↓
Failure
  ↓
Reason
  ↓
Change
```

---

## 5. Fail safely

When an operation is ambiguous, the runtime should prefer refusing the operation rather than guessing.

For example:

```text
Target text appears 4 times.

Refusing to make an ambiguous replacement.
```

---

## 6. Limit autonomous execution

The runtime uses limits such as:

```text
MAX_STEPS
MAX_TEST_RETRIES
```

This prevents an agent from running indefinitely.

---

# 🧠 What This Project Demonstrates

This project demonstrates the fundamental building blocks behind AI coding agents:

* LLM tool calling
* Agent execution loops
* Dynamic action selection
* Repository inspection
* Structured agent state
* Task planning
* Human-in-the-loop approval
* Safe filesystem operations
* Code modification
* Command execution
* Automated testing
* Iterative debugging
* Failure recovery
* Runtime safety controls

The goal is not simply to build a chatbot that generates code.

The goal is to build an agent capable of:

```text
Understand
   ↓
Plan
   ↓
Inspect
   ↓
Reason
   ↓
Act
   ↓
Observe
   ↓
Test
   ↓
Correct
   ↓
Verify
```

---

# 🛠️ Technology Stack

Current technologies include:

* **Python**
* **LLM with tool/function calling**
* **OpenAI-compatible API**
* **Groq API**
* **pytest**
* **Git**
* **JSON**
* **Python dataclasses**

The architecture is intentionally kept lightweight so that the underlying agent concepts remain visible.

---

# 🎯 Current Objective

The long-term goal is to evolve this into a more capable software engineering agent that can work with real repositories and perform increasingly sophisticated engineering tasks while maintaining:

* Controlled execution
* Reliable retrieval
* Human approval
* Test validation
* Structured state
* Safe tool execution
* Explainable actions

The system will be expanded incrementally as new capabilities are introduced.

---

# 📌 Key Takeaway

The core architecture can be summarized as:

```text
             ┌──────────────┐
             │     USER     │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │    PLANNER   │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │ AGENT STATE  │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │     LLM      │
             └──────┬───────┘
                    │
               Tool Call
                    │
                    ▼
             ┌──────────────┐
             │    RUNTIME   │
             └──────┬───────┘
                    │
             Validation
             + Approval
                    │
                    ▼
             ┌──────────────┐
             │    TOOLS     │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │  REPOSITORY  │
             └──────┬───────┘
                    │
                 Result
                    │
                    └──────────────► LLM
```

The agent therefore forms a continuous:

**Reason → Act → Observe → Reason**

loop around the software repository.
