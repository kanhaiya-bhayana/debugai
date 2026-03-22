import re
from .base import StackTraceParser


class PythonParser(StackTraceParser):

    def match(self, log: str) -> bool:
        return "File " in log and "line" in log

    def extract_frames(self, log: str):
        return re.findall(r'File ".*", line \d+, in ([^\n]+)', log)