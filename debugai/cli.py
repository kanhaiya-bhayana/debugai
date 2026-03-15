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

    console.print(
        Panel(result["exception"], title="🔥 Exception Type", title_align="left", expand=False)
    )

    console.print(
        Panel(result["origin"], title="📍 Failure Origin", title_align="left", expand=False)
    )

    console.print(
        Panel(result["source"], title="📂 Likely Failure File", title_align="left", expand=False)
    )

    console.print(
        Panel(result["chain"], title="🔗 Execution Chain", title_align="left", expand=False)
    )

    console.print(
        Panel(result["root_cause"], title="🔍 Root Cause", title_align="left", expand=False)
    )

    console.print(
        Panel(result["fix"], title="💡 Suggested Fix", title_align="left", expand=False)
    )

    console.print(
        Panel(result["prevention"], title="⚠️ Prevention", title_align="left", expand=False)
    )


if __name__ == "__main__":
    app()
