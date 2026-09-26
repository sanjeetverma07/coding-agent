def ask_user_for_approval(tool_name, arguments):

    print("\n" + "=" * 60)
    print("APPROVAL REQUIRED")
    print("=" * 60)

    if tool_name == "replace_in_file":
        print(f"File: {arguments.get('path', '<missing>')}")
        print("\n------- OLD -------")
        print(arguments.get("old", "<missing>"))
        print("\n------- NEW -------")
        print(arguments.get("new", "<missing>"))
    elif tool_name == "write_file":
        print(f"File: {arguments.get('path', '<missing>')}")
        print("\n------- CONTENT -------")
        print(arguments.get("content", "<missing>"))
    elif tool_name == "run_command":
        print(f"Command: {arguments.get('command', '<missing>')}")
    else:
        print("Tool:", tool_name)
        print("Arguments:", arguments)

    answer = input("\nApprove? (Y/n): ").strip().lower()
    if answer == "":
        return True

    return answer == "y"