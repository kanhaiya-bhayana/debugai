import re

from debugai.parser.registry import get_parser

# Matches both Python-style errors (ValueError, KeyError) and
# Java/C#-style exceptions (NullReferenceException, IOException)
_EXCEPTION_PATTERN = re.compile(r'\w+(?:Exception|Error)')


def extract_all_stack_traces(log: str):
    """
    Extract multiple stack traces from a log string.
    Handles Python (Traceback header), C#/Java, and Node.js formats.
    """
    lines = log.splitlines()
    traces = []
    current_trace = []
    capture = False

    for line in lines:

        # Python traceback starts with a dedicated header
        if "Traceback (most recent call last)" in line:
            if current_trace:
                traces.append("\n".join(current_trace))
                current_trace = []
            capture = True

        # C# / Java / Node: exception type on its own line triggers capture
        elif _EXCEPTION_PATTERN.search(line) and not capture:
            if current_trace:
                traces.append("\n".join(current_trace))
                current_trace = []
            capture = True

        if capture:
            current_trace.append(line)

            # End condition: blank line signals end of trace block
            if line.strip() == "":
                traces.append("\n".join(current_trace))
                current_trace = []
                capture = False

    # Flush any trailing trace that wasn't followed by a blank line
    if current_trace:
        traces.append("\n".join(current_trace))

    return traces


def extract_stack_frames(log: str):
    parser = get_parser(log)
    if parser:
        return parser.extract_frames(log)
    return []


def extract_exception_type(log: str):
    """
    Extract the exception/error type from a stack trace.
    Handles Python (ValueError, KeyError, TypeError …) and
    C#/Java (NullReferenceException, IOException …) conventions.
    """
    # For Python traces: the exception is on the LAST non-blank line
    # e.g. "ValueError: invalid literal for int()"
    parser = get_parser(log)
    if parser and hasattr(parser, 'extract_exception_type'):
        result = parser.extract_exception_type(log)
        if result and result != "UnknownException":
            return result

    # Generic fallback: find any word ending in Error or Exception
    match = _EXCEPTION_PATTERN.search(log)
    if match:
        return match.group(0)

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
    source_file = detect_source_file(log, origin)

    return {
        "exception": exception_type,
        "origin": origin,
        "chain": stack_chain,
        "source": source_file,
        "root_cause": "Unknown error detected.",
        "fix": "Check the stack trace and logs.",
        "prevention": "Add better exception handling."
    }


def detect_source_file(log: str, origin: str) -> str:
    """
    Detect the likely source file from the trace, using language-aware logic.
    """
    # Python: pull the file path directly from the trace
    python_file = re.search(r'File "(.+\.py)", line \d+', log)
    if python_file:
        return python_file.group(1)

    # Node.js: .js file reference
    node_file = re.search(r'at .+\((.+\.js):\d+:\d+\)', log)
    if node_file:
        return node_file.group(1)

    # Java: class name → .java
    java_frame = re.search(r'at\s+([\w$.]+)\((\w+\.java):\d+\)', log)
    if java_frame:
        return java_frame.group(2)

    # C# fallback: derive from class name
    if origin and "." in origin:
        class_name = origin.split(".")[0]
        return f"{class_name}.cs"

    return "Unknown file"


def extract_stack_trace_from_log(log: str):
    """
    Extracts the first stack trace found in raw logs.
    """
    lines = log.splitlines()
    stack_trace = []
    capture = False

    for line in lines:
        if "Traceback (most recent call last)" in line or _EXCEPTION_PATTERN.search(line):
            capture = True

        if capture:
            stack_trace.append(line)
            if line.strip() == "":
                break

    return "\n".join(stack_trace) if stack_trace else log
