from __future__ import annotations

import json
from pathlib import Path

import librosa

from karaoke.utils.audio import load_audio, normalize_audio
from karaoke.utils.log import setup_logger


logger = setup_logger()


def run(audio_path: Path, output_dir: Path) -> tuple[float, list[float]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    audio, sr = load_audio(audio_path)
    audio = normalize_audio(audio)

    tempo, beats = librosa.beat.beat_track(y=audio, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr).tolist()

    (output_dir / "bpm.json").write_text(json.dumps({"bpm": float(tempo)}, indent=2))
    (output_dir / "beats.json").write_text(json.dumps({"beats": beat_times}, indent=2))

    logger.info("BPM detectado: %.2f", tempo)
    return float(tempo), beat_times
