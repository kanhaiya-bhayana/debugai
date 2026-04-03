HIGH_PRIORITY = [
    "NullReferenceException",
    "OutOfMemory",
    "Segmentation fault",
    "Unhandled"
]

MEDIUM_PRIORITY = [
    "KeyNotFoundException",
    "Timeout",
    "Connection",
    "IOException"
]


def score_trace(trace: str) -> int:
    score = 0

    score += 100 * sum(keyword in trace for keyword in HIGH_PRIORITY)
    score += 50 * sum(keyword in trace for keyword in MEDIUM_PRIORITY)

    score += len(trace.splitlines())

    return score


def select_most_relevant(traces: list[str]) -> str:
    if not traces:
        return ""

    scored = [(trace, score_trace(trace)) for trace in traces]

    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)

    return scored[0][0]