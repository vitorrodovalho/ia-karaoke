from __future__ import annotations

from pathlib import Path

import numpy as np
import pretty_midi

from karaoke.utils.log import setup_logger
from karaoke.utils.midi import add_notes, build_chord, chord_root_to_midi


logger = setup_logger()


def _build_drums(bpm: float, beats: list[float], duration: float) -> pretty_midi.PrettyMIDI:
    midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
    drums = pretty_midi.Instrument(program=0, is_drum=True)

    beat_interval = 60.0 / bpm if bpm > 0 else 0.5
    if beats:
        for index, beat_time in enumerate(beats):
            if beat_time > duration:
                break
            drums.notes.append(
                pretty_midi.Note(velocity=100, pitch=36, start=beat_time, end=beat_time + 0.1)
            )
            drums.notes.append(
                pretty_midi.Note(velocity=70, pitch=42, start=beat_time, end=beat_time + 0.05)
            )
            if index % 2 == 1:
                drums.notes.append(
                    pretty_midi.Note(velocity=95, pitch=38, start=beat_time, end=beat_time + 0.1)
                )
    else:
        time = 0.0
        while time < duration:
            drums.notes.append(
                pretty_midi.Note(velocity=100, pitch=36, start=time, end=time + 0.1)
            )
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


def _build_bass(
    bpm: float,
    bass_pitch: list[dict[str, float | None]],
    duration: float,
) -> pretty_midi.PrettyMIDI:
    midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
    bass = pretty_midi.Instrument(program=33)
    current_note = None
    current_start = None
    for point in bass_pitch:
        time = float(point["time"])
        pitch = point["pitch"]
        midi_note = None
        if pitch is not None and np.isfinite(pitch):
            midi_note = int(round(pretty_midi.hz_to_note_number(float(pitch))))
        if current_note is None:
            if midi_note is not None:
                current_note = midi_note
                current_start = time
            continue

        if midi_note != current_note:
            if current_start is not None and time > current_start:
                bass.notes.append(
                    pretty_midi.Note(
                        velocity=90,
                        pitch=int(current_note),
                        start=float(current_start),
                        end=float(time),
                    )
                )
            current_note = midi_note
            current_start = time if midi_note is not None else None

    if current_note is not None and current_start is not None:
        end_time = max(duration, float(current_start))
        if end_time > current_start:
            bass.notes.append(
                pretty_midi.Note(
                    velocity=90,
                    pitch=int(current_note),
                    start=float(current_start),
                    end=float(end_time),
                )
            )

    if not bass.notes:
        bass.notes.append(pretty_midi.Note(velocity=80, pitch=36, start=0.0, end=duration))
    midi.instruments.append(bass)
    return midi


def _build_strummed_chord(
    root_note: int,
    duration: float,
    start: float,
    strum_delay: float = 0.03,
) -> list[pretty_midi.Note]:
    notes = []
    for index, interval in enumerate([0, 4, 7]):
        note_start = start + strum_delay * index
        note_end = max(note_start + 0.05, start + duration)
        notes.append(
            pretty_midi.Note(
                velocity=75,
                pitch=root_note + interval,
                start=note_start,
                end=note_end,
            )
        )
    return notes


def _build_chords(
    bpm: float,
    chords: list[dict[str, float | str]],
    duration: float,
) -> pretty_midi.PrettyMIDI:
    midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
    instrument = pretty_midi.Instrument(program=0)

    for index, chord in enumerate(chords):
        start = float(chord["time"])
        end = float(chords[index + 1]["time"]) if index + 1 < len(chords) else duration
        if end <= start:
            continue
        if chord.get("instrument") not in ("piano", "keys", "keyboard"):
            continue
        root = str(chord["chord"]).replace("m", "")
        root_note = chord_root_to_midi(root, octave=4)
        add_notes(instrument, build_chord(root_note, duration=end - start, start=start))

    if instrument.notes:
        midi.instruments.append(instrument)
    return midi


def _build_guitar(
    bpm: float,
    chords: list[dict[str, float | str]],
    duration: float,
) -> pretty_midi.PrettyMIDI:
    midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
    instrument = pretty_midi.Instrument(program=24)

    for index, chord in enumerate(chords):
        start = float(chord["time"])
        end = float(chords[index + 1]["time"]) if index + 1 < len(chords) else duration
        if end <= start:
            continue
        if chord.get("instrument") != "guitar":
            continue
        root = str(chord["chord"]).replace("m", "")
        root_note = chord_root_to_midi(root, octave=4)
        add_notes(instrument, _build_strummed_chord(root_note, duration=end - start, start=start))

    if instrument.notes:
        midi.instruments.append(instrument)
    return midi


def run(
    *,
    bpm: float,
    beats: list[float],
    chords: list[dict[str, float | str]],
    bass_pitch: list[dict[str, float | None]],
    output_dir: Path,
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    duration_candidates: list[float] = []
    if beats:
        duration_candidates.append(max(beats))
    if chords:
        duration_candidates.append(max(float(chord["time"]) for chord in chords))
    if bass_pitch:
        duration_candidates.append(max(float(point["time"]) for point in bass_pitch))
    duration = max(duration_candidates, default=30.0)
    if bpm > 0:
        duration += 60.0 / bpm

    drums_midi = _build_drums(bpm, beats, duration)
    bass_midi = _build_bass(bpm, bass_pitch, duration)
    chords_midi = _build_chords(bpm, chords, duration)
    guitar_midi = _build_guitar(bpm, chords, duration)

    arrangement = pretty_midi.PrettyMIDI(initial_tempo=bpm)
    arrangement.instruments = (
        drums_midi.instruments
        + bass_midi.instruments
        + chords_midi.instruments
        + guitar_midi.instruments
    )

    paths = {
        "drums": output_dir / "drums.mid",
        "bass": output_dir / "bass.mid",
        "chords": output_dir / "chords.mid",
        "guitar": output_dir / "guitar.mid",
        "arrangement": output_dir / "arrangement.mid",
    }

    drums_midi.write(str(paths["drums"]))
    bass_midi.write(str(paths["bass"]))
    chords_midi.write(str(paths["chords"]))
    guitar_midi.write(str(paths["guitar"]))
    arrangement.write(str(paths["arrangement"]))

    logger.info("MIDIs gerados em %s", output_dir)
    return paths
