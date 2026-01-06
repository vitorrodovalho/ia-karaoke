from __future__ import annotations

import json
from pathlib import Path

import librosa
import numpy as np

from karaoke.utils.audio import load_audio, normalize_audio
from karaoke.utils.log import setup_logger
from karaoke.utils.midi import NOTE_NAMES


logger = setup_logger()


def run(audio_path: Path, output_dir: Path) -> list[dict[str, float | str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    audio, sr = load_audio(audio_path)
    audio = normalize_audio(audio)

    chroma = librosa.feature.chroma_cqt(y=audio, sr=sr)
    np.save(output_dir / "chroma.npy", chroma)

    times = librosa.frames_to_time(range(chroma.shape[1]), sr=sr)
    chords: list[dict[str, float | str]] = []
    last_chord = None
    for time_index, time_value in enumerate(times):
        pitch_class = int(np.argmax(chroma[:, time_index]))
        chord_name = NOTE_NAMES[pitch_class]
        if chord_name == last_chord:
            continue
        chords.append({"time": float(time_value), "chord": chord_name})
        last_chord = chord_name

    (output_dir / "chords.json").write_text(json.dumps({"chords": chords}, indent=2))
    logger.info("Acordes extraídos: %d frames", len(chords))
    return chords
