from __future__ import annotations

from pathlib import Path

from karaoke.utils.log import setup_logger
from karaoke.utils.proc import run_command


logger = setup_logger()


def run(render_paths: dict[str, Path], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    backing_final = output_dir / "backing_final.wav"

    if "arrangement" in render_paths:
        run_command(["ffmpeg", "-y", "-i", str(render_paths["arrangement"]), str(backing_final)])
        logger.info("Backing final exportado via arrangement")
        return backing_final

    inputs = [str(path) for path in render_paths.values()]
    command = ["ffmpeg", "-y"]
    for path in inputs:
        command.extend(["-i", path])
    command.extend([
        "-filter_complex",
        f"amix=inputs={len(inputs)}:normalize=0",
        str(backing_final),
    ])
    run_command(command)
    logger.info("Backing final mixado")
    return backing_final
