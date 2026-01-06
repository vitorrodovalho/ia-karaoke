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

    hop_length = 512
    chroma = librosa.feature.chroma_cqt(y=audio, sr=sr, hop_length=hop_length)
    np.save(output_dir / "chroma.npy", chroma)

    harmonic_audio, _ = librosa.effects.hpss(audio)
    rms = librosa.feature.rms(y=audio, hop_length=hop_length)[0]
    centroid = librosa.feature.spectral_centroid(
        y=harmonic_audio, sr=sr, hop_length=hop_length
    )[0]

    times = librosa.frames_to_time(range(chroma.shape[1]), sr=sr, hop_length=hop_length)
    chords: list[dict[str, float | str]] = []
    last_chord = None
    last_instrument = None
    energy_floor = float(np.quantile(rms, 0.2)) if rms.size else 0.0
    for time_index, time_value in enumerate(times):
        pitch_class = int(np.argmax(chroma[:, time_index]))
        chord_name = NOTE_NAMES[pitch_class]

        frame_rms = float(rms[time_index]) if time_index < rms.size else 0.0
        frame_centroid = float(centroid[time_index]) if time_index < centroid.size else 0.0
        if frame_rms <= max(energy_floor, 0.01):
            instrument = "none"
        elif frame_centroid >= 2000:
            instrument = "guitar"
        else:
            instrument = "piano"

        if chord_name == last_chord and instrument == last_instrument:
            continue
        chords.append(
            {
                "time": float(time_value),
                "chord": chord_name,
                "instrument": instrument,
            }
        )
        last_chord = chord_name
        last_instrument = instrument

    (output_dir / "chords.json").write_text(json.dumps({"chords": chords}, indent=2))
    logger.info("Acordes extraídos: %d frames", len(chords))
    return chords
