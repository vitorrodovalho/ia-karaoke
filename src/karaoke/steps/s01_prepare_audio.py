from __future__ import annotations

from pathlib import Path

from karaoke.utils.log import setup_logger
from karaoke.utils.proc import run_command


logger = setup_logger()


def run(input_dir: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    source = input_dir / "audio.mp3"
    target = output_dir / "audio.wav"
    logger.info("Convertendo áudio para WAV")
    run_command(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(source),
            "-ar",
            "44100",
            "-ac",
            "1",
            str(target),
        ]
    )
    return target
