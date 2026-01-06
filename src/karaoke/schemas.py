from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any


class AnalysisReport(BaseModel):
    bpm: float
    beats: list[float]
    chords: list[dict[str, Any]]
    bass_pitch: list[dict[str, Any]]


class ExportReport(BaseModel):
    song_id: str
    backing_path: str
    mode: str
    midi_paths: dict[str, str] = Field(default_factory=dict)
    analysis: AnalysisReport | None = None
