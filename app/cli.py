import asyncio
import typer
from rich import print
from .db import init_db
from .swarm import MoneySwarm

app = typer.Typer(help="Money-Agentic CPA optimization swarm.")

@app.command()
def init():
    asyncio.run(init_db())
    print("[green]Database initialized.[/green]")

@app.command()
def plan(offer: str, channel: str = "dry-run"):
    """Generate a strategy and content plan without publishing."""
    print(MoneySwarm().plan(offer, channel))

def main():
    app()

if __name__ == "__main__":
    main()
