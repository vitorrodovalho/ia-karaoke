from __future__ import annotations

from pathlib import Path

from karaoke.config import DEFAULT_PATHS
from karaoke.schemas import AnalysisReport, ExportReport
from karaoke.utils.log import setup_logger
from karaoke.utils.paths import SongPaths
from karaoke.steps import (
    s00_validate,
    s01_prepare_audio,
    s02_analyze_tempo_beats,
    s03_extract_chords,
    s04_extract_bass_pitch,
    s05_build_midi,
    s06_separate_vocals,
    s06_render_midi,
    s07_mix_master,
    s08_export,
)


logger = setup_logger()


def run_pipeline(
    song_id: str,
    *,
    root: Path | None = None,
    mode: str = "source",
) -> ExportReport:
    paths = DEFAULT_PATHS if root is None else DEFAULT_PATHS.__class__(root=root)
    logger.info("Iniciando pipeline para %s", song_id)

    input_dir = paths.input / song_id
    work_dir = paths.work / song_id
    output_dir = paths.output / song_id
    song_paths = SongPaths(work_dir)
    song_paths.ensure_all()

    s00_validate.run(song_id, input_dir)
    if mode not in ("ai", "source"):
        raise ValueError("Modo inválido. Use 'ai' ou 'source'.")

    audio_channels = 2 if mode == "source" else 1
    audio_path = s01_prepare_audio.run(
        input_dir,
        song_paths.original_dir,
        channels=audio_channels,
    )

    if mode == "ai":
        bpm, beats = s02_analyze_tempo_beats.run(audio_path, song_paths.analysis_dir)
        chords = s03_extract_chords.run(audio_path, song_paths.analysis_dir)
        bass_pitch = s04_extract_bass_pitch.run(audio_path, song_paths.analysis_dir)

        midi_paths = s05_build_midi.run(
            bpm=bpm,
            beats=beats,
            chords=chords,
            bass_pitch=bass_pitch,
            output_dir=song_paths.midi_dir,
            include_stems=False,
        )

        render_paths = s06_render_midi.run(
            midi_paths=midi_paths,
            output_dir=song_paths.render_dir,
            soundfont=paths.assets / "soundfonts" / "GeneralUser_GS.sf2",
        )
        backing_final = s07_mix_master.run(render_paths, song_paths.mix_dir)
        analysis = AnalysisReport(
            bpm=bpm,
            beats=beats,
            chords=chords,
            bass_pitch=bass_pitch,
        )
        midi_output = midi_paths
    elif mode == "source":
        backing_render = s06_separate_vocals.run(audio_path, song_paths.render_dir)
        backing_final = s07_mix_master.run(
            {"arrangement": backing_render},
            song_paths.mix_dir,
        )
        analysis = None
        midi_output = {}
    report = s08_export.run(
        song_id=song_id,
        output_dir=output_dir,
        midi_paths=midi_output,
        backing_path=backing_final,
        analysis=analysis,
        mode=mode,
    )

    logger.info("Pipeline finalizado para %s", song_id)
    return report
