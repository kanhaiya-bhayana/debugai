import re


def extract_exception_type(log: str):
    pattern = r'(\w+Exception)'
    match = re.search(pattern, log)

    if match:
        return match.group(1)

    return "UnknownException"


def extract_failure_origin(log: str):
    pattern = r'at\s+([^\n]+)'
    matches = re.findall(pattern, log)

    if matches:
        return matches[0]

    return "Unknown origin"


def extract_stack_chain(log: str):
    """
    Extract full stack trace chain.
    """

    pattern = r'at\s+([^\n]+)'
    matches = re.findall(pattern, log)

    if not matches:
        return "No stack trace detected"

    # reverse for execution flow (top → bottom)
    chain = list(reversed(matches))

    return "\n   ↓\n".join(chain)


def explain_error(log: str):

    exception_type = extract_exception_type(log)
    origin = extract_failure_origin(log)
    stack_chain = extract_stack_chain(log)

    if "NullReferenceException" in log:
        return {
            "exception": exception_type,
            "origin": origin,
            "chain": stack_chain,
            "root_cause": "A null object is being accessed.",
            "fix": "Check if the object is initialized before using it.",
            "prevention": "Add null checks before accessing object properties."
        }

    return {
        "exception": exception_type,
        "origin": origin,
        "chain": stack_chain,
        "root_cause": "Unknown error detected.",
        "fix": "Check the stack trace and logs.",
        "prevention": "Add better exception handling."
    }