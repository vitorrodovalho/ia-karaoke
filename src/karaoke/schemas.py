from __future__ import annotations

from pydantic import BaseModel
from typing import Any


class AnalysisReport(BaseModel):
    bpm: float
    beats: list[float]
    chords: list[dict[str, Any]]
    bass_pitch: list[dict[str, Any]]


class ExportReport(BaseModel):
    song_id: str
    backing_path: str
    midi_paths: dict[str, str]
    analysis: AnalysisReport
