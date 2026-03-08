def explain_error(log: str):

    if "NullReferenceException" in log:
        return {
            "root_cause": "A null object is being accessed.",
            "fix": "Check if the object is initialized before using it.",
            "prevention": "Add null checks before accessing object properties."
        }

    return {
        "root_cause": "Unknown error",
        "fix": "Check stack trace and recent code changes.",
        "prevention": "Add better logging and exception handling."
    }