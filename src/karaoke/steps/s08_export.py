from __future__ import annotations

from pathlib import Path

from karaoke.schemas import AnalysisReport, ExportReport
from karaoke.utils.log import setup_logger


logger = setup_logger()


def run(
    *,
    song_id: str,
    output_dir: Path,
    midi_paths: dict[str, Path],
    backing_path: Path,
    bpm: float,
    beats: list[float],
    chords: list[dict[str, float | str]],
    bass_pitch: list[dict[str, float | None]],
) -> ExportReport:
    output_dir.mkdir(parents=True, exist_ok=True)
    midi_output = output_dir / "midi"
    midi_output.mkdir(parents=True, exist_ok=True)

    for stem, path in midi_paths.items():
        target = midi_output / path.name
        target.write_bytes(path.read_bytes())

    backing_target = output_dir / "backing.wav"
    backing_target.write_bytes(backing_path.read_bytes())

    report = ExportReport(
        song_id=song_id,
        backing_path=str(backing_target),
        midi_paths={stem: str(midi_output / path.name) for stem, path in midi_paths.items()},
        analysis=AnalysisReport(
            bpm=bpm,
            beats=beats,
            chords=chords,
            bass_pitch=bass_pitch,
        ),
    )

    report_path = output_dir / "report.json"
    report_path.write_text(report.model_dump_json(indent=2, ensure_ascii=False))
    logger.info("Relatório exportado: %s", report_path)
    return report
