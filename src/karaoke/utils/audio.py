from __future__ import annotations

from pathlib import Path

import librosa
import numpy as np


def load_audio(path: Path, sr: int = 44100) -> tuple[np.ndarray, int]:
    audio, sample_rate = librosa.load(path, sr=sr, mono=True)
    return audio, sample_rate


def normalize_audio(audio: np.ndarray) -> np.ndarray:
    peak = np.max(np.abs(audio))
    if peak == 0:
        return audio
    return audio / peak
