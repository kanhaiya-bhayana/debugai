import re


def extract_failure_origin(log: str):
    """
    Extract the first stack trace method call.
    """

    pattern = r'at\s+([^\n]+)'

    matches = re.findall(pattern, log)

    if matches:
        return matches[0]

    return "Unknown origin"


def explain_error(log: str):

    origin = extract_failure_origin(log)

    if "NullReferenceException" in log:
        return {
            "root_cause": "A null object is being accessed.",
            "fix": "Check if the object is initialized before using it.",
            "prevention": "Add null checks before accessing object properties.",
            "origin": origin
        }

    return {
        "root_cause": "Unknown error detected.",
        "fix": "Check the stack trace and logs.",
        "prevention": "Add better exception handling.",
        "origin": origin
    }