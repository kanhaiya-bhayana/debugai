import re
from .base import StackTraceParser


class NodeParser(StackTraceParser):

    def match(self, log: str) -> bool:
        return ".js:" in log

    def extract_frames(self, log: str):
        return re.findall(r'at\s+(?:Object\.)?([^\s]+)\s+\([^\)]+\)', log)