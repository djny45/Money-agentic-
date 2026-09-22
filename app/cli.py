import asyncio
import typer
from rich import print
from .db import init_db
from .swarm import MoneySwarm
from .banner import BannerBrief
from .creative_pipeline import CreativePipeline

app = typer.Typer(help="Money-Agentic CPA optimization swarm.")

@app.command()
def init():
    asyncio.run(init_db())
    print("[green]Database initialized.[/green]")

@app.command()
def banner(title: str, subtitle: str, cta: str = "Learn more", slug: str = "creative"):
    """Build a local ad creative package; no ad is published or charged."""
    package = CreativePipeline().build(BannerBrief(title, subtitle, cta), slug)
    manifest = CreativePipeline().write_manifest(package)
    print({"creative": package.__dict__, "manifest": manifest})

@app.command()
def plan(offer: str, channel: str = "dry-run"):
    """Generate a strategy and content plan without publishing."""
    print(MoneySwarm().plan(offer, channel))

def main():
    app()

if __name__ == "__main__":
    main()
