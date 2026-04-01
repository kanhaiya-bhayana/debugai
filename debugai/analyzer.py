import re

from debugai.parser.registry import get_parser

def extract_all_stack_traces(log: str):
    """
    Extract multiple stack traces from logs.
    """

    lines = log.splitlines()

    traces = []
    current_trace = []
    capture = False

    for line in lines:

        # Start of stack trace
        if re.search(r'\w+Exception', line):
            if current_trace:
                traces.append("\n".join(current_trace))
                current_trace = []

            capture = True

        if capture:
            current_trace.append(line)

            # End condition: blank line OR next log entry
            if line.strip() == "":
                capture = False

    # Add last trace
    if current_trace:
        traces.append("\n".join(current_trace))

    return traces

def extract_stack_frames(log: str):

    parser = get_parser(log)

    if parser:
        return parser.extract_frames(log)

    return []

def extract_exception_type(log: str):
    pattern = r'(\w+Exception)'
    match = re.search(pattern, log)

    if match:
        return match.group(1)

    return "UnknownException"


def extract_failure_origin(log: str):

    frames = extract_stack_frames(log)

    if frames:
        return frames[0]

    return "Unknown origin"


def extract_stack_chain(log: str):

    frames = extract_stack_frames(log)

    if not frames:
        return "No stack trace detected"

    chain = list(reversed(frames))

    return "\n   ↓\n".join(chain)


def explain_error(log: str):

    exception_type = extract_exception_type(log)
    origin = extract_failure_origin(log)
    stack_chain = extract_stack_chain(log)
    source_file = detect_source_file(origin)

    if "NullReferenceException" in log:
        return {
            "exception": exception_type,
            "origin": origin,
            "chain": stack_chain,
            "source": source_file,
            "root_cause": "A null object is being accessed.",
            "fix": "Check if the object is initialized before using it.",
            "prevention": "Add null checks before accessing object properties."
        }

    return {
        "exception": exception_type,
        "origin": origin,
        "chain": stack_chain,
        "source": source_file,
        "root_cause": "Unknown error detected.",
        "fix": "Check the stack trace and logs.",
        "prevention": "Add better exception handling."
    }

def detect_source_file(origin: str):
    """
    Try to detect the likely source file from the method name.
    """

    if "." not in origin:
        return "Unknown file"

    class_name = origin.split(".")[0]

    return f"{class_name}.cs"

def extract_stack_trace_from_log(log: str):
    """
    Extracts the first stack trace found in raw logs.
    """

    lines = log.splitlines()

    stack_trace = []
    capture = False

    for line in lines:

        # Detect exception line
        if re.search(r'\w+Exception', line):
            capture = True

        if capture:
            stack_trace.append(line)

            # Stop when stack trace ends (empty line or no 'at')
            if line.strip() == "":
                break

    return "\n".join(stack_trace) if stack_trace else log