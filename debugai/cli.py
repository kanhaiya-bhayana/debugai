import typer
from rich.console import Console
from rich.panel import Panel
from debugai.analyzer import explain_error

app = typer.Typer()
console = Console()


@app.command()
def explain(file: str):

    with open(file, "r") as f:
        log = f.read()

    result = explain_error(log)

    console.print(
        Panel(result["origin"], title="[bold_cyan]📍 Failure Origin", title_align="left", expand=False)
    )

    console.print(
        Panel(result["root_cause"], title="[bold_green]🔍 Root Cause", title_align="left", expand=False)
    )

    console.print(
        Panel(result["fix"], title="[bold_yellow]💡 Suggested Fix", title_align="left", expand=False)
    )

    console.print(
        Panel(result["prevention"], title="[bold_orange]⚠️ Prevention", title_align="left", expand=False)
    )


if __name__ == "__main__":
    app()