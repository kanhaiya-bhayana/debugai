import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import SpinnerColumn, Progress

from debugai.analyzer import explain_error
from debugai.ai_analyzer import analyze_with_ai

app = typer.Typer()
console = Console()

@app.command()
def explain(file: str, ai: bool = False):

    with open(file) as f:
        log = f.read()

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