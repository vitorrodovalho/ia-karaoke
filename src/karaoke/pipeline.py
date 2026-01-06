from __future__ import annotations

from pathlib import Path

from karaoke.config import DEFAULT_PATHS
from karaoke.schemas import ExportReport
from karaoke.utils.log import setup_logger
from karaoke.utils.paths import SongPaths
from karaoke.steps import (
    s00_validate,
    s01_prepare_audio,
    s02_analyze_tempo_beats,
    s03_extract_chords,
    s04_extract_bass_pitch,
    s05_build_midi,
    s06_render_midi,
    s07_mix_master,
    s08_export,
)


logger = setup_logger()


def run_pipeline(song_id: str, *, root: Path | None = None) -> ExportReport:
    paths = DEFAULT_PATHS if root is None else DEFAULT_PATHS.__class__(root=root)
    logger.info("Iniciando pipeline para %s", song_id)

    input_dir = paths.input / song_id
    work_dir = paths.work / song_id
    output_dir = paths.output / song_id
    song_paths = SongPaths(work_dir)
    song_paths.ensure_all()

    s00_validate.run(song_id, input_dir)
    audio_path = s01_prepare_audio.run(input_dir, song_paths.original_dir)
    bpm, beats = s02_analyze_tempo_beats.run(audio_path, song_paths.analysis_dir)
    chords = s03_extract_chords.run(audio_path, song_paths.analysis_dir)
    bass_pitch = s04_extract_bass_pitch.run(audio_path, song_paths.analysis_dir)

    midi_paths = s05_build_midi.run(
        bpm=bpm,
        beats=beats,
        chords=chords,
        bass_pitch=bass_pitch,
        output_dir=song_paths.midi_dir,
    )

    render_paths = s06_render_midi.run(
        midi_paths=midi_paths,
        output_dir=song_paths.render_dir,
        soundfont=paths.assets / "soundfonts" / "GeneralUser_GS.sf2",
    )
    backing_final = s07_mix_master.run(render_paths, song_paths.mix_dir)
    report = s08_export.run(
        song_id=song_id,
        output_dir=output_dir,
        midi_paths=midi_paths,
        backing_path=backing_final,
        bpm=bpm,
        beats=beats,
        chords=chords,
        bass_pitch=bass_pitch,
    )

    logger.info("Pipeline finalizado para %s", song_id)
    return report
