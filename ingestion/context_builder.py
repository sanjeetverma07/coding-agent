
def build_context(results, max_chars=12000):
    """
    Build a compact code context from retrieved search results.
    """
    if not results:
        return "No relevant code was found."
    context_parts = []
    total_chars = 0

    for result in results:
        path = result["path"]
        start_line = result["start_line"]
        end_line = result["end_line"]
        content = result["content"]
        block = (
            f"\n--- {path} "
            f"(lines {start_line}-{end_line}) ---\n"
            f"{content}\n"
        )
        if total_chars + len(block) > max_chars:
            break
        context_parts.append(block)
        total_chars += len(block)
    return "\n".join(context_parts)