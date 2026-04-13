"""
Tests for debugai/parser/  — match() and extract_frames() for each parser.
"""
import pytest
from debugai.parser.python import PythonParser
from debugai.parser.csharp_java import CSharpJavaParser
from debugai.parser.node import NodeParser
from debugai.parser.registry import get_parser

# ── Fixtures ─────────────────────────────────────────────────────────────────

PYTHON_TRACE = """\
Traceback (most recent call last):
  File "server.py", line 10, in handle_request
    result = process_data(payload)
  File "processor.py", line 25, in process_data
    value = parse_input(raw)
  File "parser.py", line 8, in parse_input
    return int(raw)
ValueError: invalid literal for int() with base 10: 'abc'"""

PYTHON_TRACE_SINGLE_FRAME = """\
Traceback (most recent call last):
  File "app.py", line 42, in process
    result = int(value)
ValueError: invalid literal for int() with base 10: 'abc'"""

PYTHON_TRACE_KEY_ERROR = """\
Traceback (most recent call last):
  File "config.py", line 5, in load
    return data["missing_key"]
KeyError: 'missing_key'"""

CSHARP_TRACE = """\
System.NullReferenceException
at TradeService.CalculatePnl()
at PricingService.ProcessTrade()
at TradeController.ExecuteTrade()"""

JAVA_TRACE = """\
java.lang.NullPointerException
at com.example.OrderService.calculateTotal(OrderService.java:42)
at com.example.OrderController.placeOrder(OrderController.java:18)"""

NODE_TRACE = """\
TypeError: Cannot read properties of undefined
    at processTicksAndRejections (node:internal/process/task_queues:95:5)
    at Object.handler (/app/routes/user.js:22:18)"""


# ── PythonParser ──────────────────────────────────────────────────────────────

class TestPythonParser:
    parser = PythonParser()

    def test_match_standard_traceback(self):
        assert self.parser.match(PYTHON_TRACE) is True

    def test_match_single_frame(self):
        assert self.parser.match(PYTHON_TRACE_SINGLE_FRAME) is True

    def test_no_match_csharp(self):
        assert self.parser.match(CSHARP_TRACE) is False

    def test_no_match_plain_text(self):
        assert self.parser.match("Everything is fine, nothing to see here.") is False

    def test_extract_frames_order(self):
        """Innermost frame (parse_input) must be first — failure origin."""
        frames = self.parser.extract_frames(PYTHON_TRACE)
        assert frames[0] == "parse_input"

    def test_extract_frames_full_chain(self):
        frames = self.parser.extract_frames(PYTHON_TRACE)
        assert frames == ["parse_input", "process_data", "handle_request"]

    def test_extract_frames_single(self):
        frames = self.parser.extract_frames(PYTHON_TRACE_SINGLE_FRAME)
        assert frames == ["process"]

    def test_extract_exception_type_value_error(self):
        assert self.parser.extract_exception_type(PYTHON_TRACE) == "ValueError"

    def test_extract_exception_type_key_error(self):
        assert self.parser.extract_exception_type(PYTHON_TRACE_KEY_ERROR) == "KeyError"


# ── CSharpJavaParser ──────────────────────────────────────────────────────────

class TestCSharpJavaParser:
    parser = CSharpJavaParser()

    def test_match_csharp(self):
        assert self.parser.match(CSHARP_TRACE) is True

    def test_match_java(self):
        assert self.parser.match(JAVA_TRACE) is True

    def test_no_match_plain_text(self):
        assert self.parser.match("no error here") is False

    def test_extract_frames_csharp(self):
        frames = self.parser.extract_frames(CSHARP_TRACE)
        assert "TradeService.CalculatePnl()" in frames
        assert "TradeController.ExecuteTrade()" in frames

    def test_extract_frames_order_csharp(self):
        """First frame should be innermost for C# traces."""
        frames = self.parser.extract_frames(CSHARP_TRACE)
        assert frames[0] == "TradeService.CalculatePnl()"


# ── NodeParser ────────────────────────────────────────────────────────────────

class TestNodeParser:
    parser = NodeParser()

    def test_match_node(self):
        assert self.parser.match(NODE_TRACE) is True

    def test_no_match_python(self):
        assert self.parser.match(PYTHON_TRACE) is False

    def test_extract_frames_node(self):
        frames = self.parser.extract_frames(NODE_TRACE)
        assert len(frames) > 0


# ── Registry ──────────────────────────────────────────────────────────────────

class TestRegistry:

    def test_routes_python(self):
        parser = get_parser(PYTHON_TRACE)
        assert isinstance(parser, PythonParser)

    def test_routes_csharp(self):
        parser = get_parser(CSHARP_TRACE)
        assert isinstance(parser, CSharpJavaParser)

    def test_routes_node(self):
        parser = get_parser(NODE_TRACE)
        assert isinstance(parser, NodeParser)

    def test_returns_none_for_garbage(self):
        parser = get_parser("this is not a stack trace at all")
        assert parser is None
