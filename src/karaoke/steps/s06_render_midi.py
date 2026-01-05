from __future__ import annotations

from pathlib import Path

from karaoke.utils.log import setup_logger
from karaoke.utils.proc import run_command


logger = setup_logger()


def run(
    *,
    midi_paths: dict[str, Path],
    output_dir: Path,
    soundfont: Path,
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if not soundfont.exists():
        raise FileNotFoundError(
            f"SoundFont não encontrado em {soundfont}. Coloque o arquivo .sf2 em assets/soundfonts."
        )

    render_paths: dict[str, Path] = {}
    for stem, midi_path in midi_paths.items():
        wav_path = output_dir / f"{stem}.wav"
        run_command(
            [
                "fluidsynth",
                "-ni",
                str(soundfont),
                str(midi_path),
                "-F",
                str(wav_path),
                "-r",
                "44100",
            ]
        )
        render_paths[stem] = wav_path
        logger.info("Renderizado %s", wav_path.name)

    return render_paths
