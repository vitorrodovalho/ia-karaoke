from __future__ import annotations

import json
from pathlib import Path

import librosa

from karaoke.utils.audio import load_audio, normalize_audio
from karaoke.utils.log import setup_logger


logger = setup_logger()


def run(audio_path: Path, output_dir: Path) -> list[dict[str, float | None]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    audio, sr = load_audio(audio_path)
    audio = normalize_audio(audio)

    f0 = librosa.yin(audio, fmin=librosa.note_to_hz("C2"), fmax=librosa.note_to_hz("C4"), sr=sr)
    times = librosa.times_like(f0, sr=sr)
    pitch_series = [
        {"time": float(time), "pitch": float(pitch) if float(pitch) == float(pitch) else None}
        for time, pitch in zip(times, f0, strict=True)
    ]

    (output_dir / "bass_pitch.json").write_text(
        json.dumps({"bass_pitch": pitch_series}, indent=2)
    )
    logger.info("Linha de baixo extraída: %d frames", len(pitch_series))
    return pitch_series
