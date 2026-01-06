from __future__ import annotations

from pathlib import Path

from karaoke.utils.log import setup_logger
from karaoke.utils.proc import run_command


logger = setup_logger()


def run(audio_path: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    backing_path = output_dir / "backing.wav"
    logger.info("Removendo voz com cancelamento de centro")
    run_command(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(audio_path),
            "-af",
            "pan=stereo|c0=c0-c1|c1=c1-c0",
            str(backing_path),
        ]
    )
    return backing_path
