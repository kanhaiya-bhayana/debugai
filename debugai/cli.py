import typer
from rich.console import Console
from rich.panel import Panel
from debugai.analyzer import explain_error

app = typer.Typer()
console = Console()

@app.command()
def explain(file: str):
    """
    Explain an error log
    """

    with open(file, "r") as f:
        log = f.read()

    result = explain_error(log)

    console.print(
        Panel(result["root_cause"], title="🔍 Root Cause", expand=False)
    )

    console.print(
        Panel(result["fix"], title="💡 Suggested Fix", expand=False)
    )

    console.print(
        Panel(result["prevention"], title="⚠️ Prevention", expand=False)
    )


if __name__ == "__main__":
    app()