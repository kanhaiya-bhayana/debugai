import sys
import os
import typer
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.progress import SpinnerColumn, Progress

from debugai.analyzer import explain_error
from debugai.ai_analyzer import analyze_with_ai
from debugai.analyzer import extract_stack_trace_from_log

app = typer.Typer()
console = Console()

@app.command()
def explain(
    input_value: str = typer.Argument(None),
    ai: bool = typer.Option(False, "--ai", help="Enable AI analysis"),
    paste: bool = typer.Option(False, "--paste", help="Read input from clipboard")
):

    # Case 1: clipboard
    if paste:
        try:
            log = subprocess.check_output("pbpaste").decode("utf-8")
        except Exception:
            console.print("[red]Failed to read clipboard[/red]")
            raise typer.Exit()

    # Case 2: piped input
    elif not sys.stdin.isatty():
        log = sys.stdin.read()

    # Case 3: file input
    elif input_value and os.path.exists(input_value):
        with open(input_value) as f:
            log = f.read()

    # Case 4: direct input
    elif input_value:
        log = input_value

    else:
        console.print("[red]No input provided[/red]")
        raise typer.Exit()

    log = extract_stack_trace_from_log(log)
    
    result = explain_error(log)

    console.print(Panel(result["exception"], title="🔥 Exception Type", title_align="left"))
    console.print(Panel(result["origin"], title="📍 Failure Origin", title_align="left"))
    console.print(Panel(result["chain"], title="🔗 Execution Chain", title_align="left"))

    if ai:
        with console.status("[bold cyan]🧠 DebugAI analyzing stack trace..."):
            ai_result = analyze_with_ai(log)

        console.print(
            Panel(
                ai_result["root_cause"],
                title="[bold magenta]🤖 AI Root Cause[/bold magenta]",
                title_align="left",
                expand=False
            )
        )

        console.print(
            Panel(
                ai_result["fix"],
                title="[bold cyan]🛠 Suggested Fix[/bold cyan]",
                title_align="left",
                expand=False
            )
        )

        console.print(
            Panel(
                ai_result["prevention"],
                title="[bold yellow]🛡 Prevention[/bold yellow]",
                title_align="left",
                expand=False
            )
        )

        console.print("[green]✔ AI analysis complete[/green]")