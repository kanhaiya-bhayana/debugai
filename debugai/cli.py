import typer
from rich.console import Console
from rich.panel import Panel

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
        ai_result = analyze_with_ai(log)

        Panel(
            ai_result["root_cause"],
            title="[bold magenta]🤖 AI Root Cause[/bold magenta]",
            title_align="left",
            expand=False,
            padding=(1,2)
        )

        console.print(
            Panel(
                str(ai_result.get("fix", "Not available")),
                title="[bold cyan]🛠 AI Suggested Fix[/bold cyan]",
                title_align="left",
                expand=False
            )
        )

        console.print(
            Panel(
                str(ai_result.get("prevention", "Not available")),
                title="[bold yellow]🛡 AI Prevention[/bold yellow]",
                title_align="left",
                expand=False
            )
        )