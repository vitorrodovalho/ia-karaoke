from __future__ import annotations

from pathlib import Path

import numpy as np
import pretty_midi

from karaoke.utils.log import setup_logger
from karaoke.utils.midi import add_notes, build_chord, chord_root_to_midi


logger = setup_logger()


def _build_drums(bpm: float, duration: float) -> pretty_midi.PrettyMIDI:
    midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
    drums = pretty_midi.Instrument(program=0, is_drum=True)

    beat_interval = 60.0 / bpm
    time = 0.0
    while time < duration:
        drums.notes.append(pretty_midi.Note(velocity=100, pitch=36, start=time, end=time + 0.1))
        drums.notes.append(
            pretty_midi.Note(velocity=90, pitch=42, start=time, end=time + 0.05)
        )
        drums.notes.append(
            pretty_midi.Note(
                velocity=90,
                pitch=38,
                start=time + beat_interval,
                end=time + beat_interval + 0.1,
            )
        )
        drums.notes.append(
            pretty_midi.Note(
                velocity=90,
                pitch=42,
                start=time + beat_interval,
                end=time + beat_interval + 0.05,
            )
        )
        time += beat_interval * 2
    midi.instruments.append(drums)
    return midi


def _build_bass(bpm: float, chords: list[dict[str, float | str]], duration: float) -> pretty_midi.PrettyMIDI:
    midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
    bass = pretty_midi.Instrument(program=33)
    beat_interval = 60.0 / bpm

    for chord in chords[::4]:
        chord_name = str(chord["chord"])
        root = chord_name.replace("m", "")
        note = chord_root_to_midi(root, octave=2)
        bass.notes.append(
            pretty_midi.Note(
                velocity=90,
                pitch=note,
                start=float(chord["time"]),
                end=float(chord["time"]) + beat_interval * 2,
            )
        )

    if not bass.notes:
        bass.notes.append(
            pretty_midi.Note(velocity=80, pitch=36, start=0.0, end=duration)
        )
    midi.instruments.append(bass)
    return midi


def _build_chords(bpm: float, chords: list[dict[str, float | str]], duration: float) -> pretty_midi.PrettyMIDI:
    midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
    instrument = pretty_midi.Instrument(program=0)

    for chord in chords[::4]:
        root = str(chord["chord"])
        root_note = chord_root_to_midi(root, octave=4)
        add_notes(
            instrument,
            build_chord(root_note, duration=1.5, start=float(chord["time"])),
        )

    if not instrument.notes:
        add_notes(instrument, build_chord(chord_root_to_midi("C"), duration=duration, start=0.0))
    midi.instruments.append(instrument)
    return midi


def run(
    *,
    bpm: float,
    beats: list[float],
    chords: list[dict[str, float | str]],
    bass_pitch: list[float],
    output_dir: Path,
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    duration = max(beats) if beats else float(np.mean(bass_pitch) or 30.0)

    drums_midi = _build_drums(bpm, duration)
    bass_midi = _build_bass(bpm, chords, duration)
    chords_midi = _build_chords(bpm, chords, duration)

    arrangement = pretty_midi.PrettyMIDI(initial_tempo=bpm)
    arrangement.instruments = drums_midi.instruments + bass_midi.instruments + chords_midi.instruments

    paths = {
        "drums": output_dir / "drums.mid",
        "bass": output_dir / "bass.mid",
        "chords": output_dir / "chords.mid",
        "arrangement": output_dir / "arrangement.mid",
    }

    drums_midi.write(str(paths["drums"]))
    bass_midi.write(str(paths["bass"]))
    chords_midi.write(str(paths["chords"]))
    arrangement.write(str(paths["arrangement"]))

    logger.info("MIDIs gerados em %s", output_dir)
    return paths
