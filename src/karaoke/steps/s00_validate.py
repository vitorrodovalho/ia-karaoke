from __future__ import annotations

from pathlib import Path

from karaoke.utils.log import setup_logger


logger = setup_logger()


def run(song_id: str, input_dir: Path) -> None:
    audio_path = input_dir / "audio.mp3"
    if not audio_path.exists():
        raise FileNotFoundError(
            f"Áudio não encontrado para {song_id}. Esperado: {audio_path}"
        )
    logger.info("Validação OK para %s", song_id)
