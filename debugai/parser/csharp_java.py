import re
from .base import StackTraceParser


class CSharpJavaParser(StackTraceParser):

    def match(self, log: str) -> bool:
        return "Exception" in log and "at " in log

    def extract_frames(self, log: str):
        return re.findall(r'at\s+([^\n]+)', log)