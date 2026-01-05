from __future__ import annotations

import json
from pathlib import Path

import typer

from karaoke.pipeline import run_pipeline
from karaoke.utils.log import setup_logger


app = typer.Typer(add_completion=False)
logger = setup_logger()


@app.command()
def run(song_id: str, root: Path | None = None) -> None:
    """Executa o pipeline para um song_id."""
    report = run_pipeline(song_id, root=root)
    typer.echo(json.dumps(report.model_dump(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    app()
