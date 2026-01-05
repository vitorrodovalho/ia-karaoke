from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import pretty_midi


NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


@dataclass(frozen=True)
class MidiStem:
    name: str
    midi: pretty_midi.PrettyMIDI


def note_name_from_pitch(pitch: int) -> str:
    return NOTE_NAMES[pitch % 12]


def chord_root_to_midi(root: str, octave: int = 4) -> int:
    index = NOTE_NAMES.index(root)
    return 12 * (octave + 1) + index


def build_chord(root_note: int, duration: float, start: float) -> list[pretty_midi.Note]:
    intervals = [0, 4, 7]
    return [
        pretty_midi.Note(
            velocity=80,
            pitch=root_note + interval,
            start=start,
            end=start + duration,
        )
        for interval in intervals
    ]


def add_notes(instrument: pretty_midi.Instrument, notes: Sequence[pretty_midi.Note]) -> None:
    instrument.notes.extend(notes)
