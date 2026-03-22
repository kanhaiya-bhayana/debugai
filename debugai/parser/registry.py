from .csharp_java import CSharpJavaParser
from .python import PythonParser
from .node import NodeParser


PARSERS = [
    CSharpJavaParser(),
    PythonParser(),
    NodeParser()
]


def get_parser(log: str):

    for parser in PARSERS:
        if parser.match(log):
            return parser

    return None