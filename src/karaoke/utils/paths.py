from __future__ import annotations

from pathlib import Path


class SongPaths:
    def __init__(self, base: Path):
        self.base = base

    def ensure(self) -> None:
        self.base.mkdir(parents=True, exist_ok=True)

    @property
    def original_dir(self) -> Path:
        return self.base / "00_original"

    @property
    def analysis_dir(self) -> Path:
        return self.base / "01_analysis"

    @property
    def midi_dir(self) -> Path:
        return self.base / "02_midi"

    @property
    def render_dir(self) -> Path:
        return self.base / "03_render"

    @property
    def mix_dir(self) -> Path:
        return self.base / "04_mix"

    def ensure_all(self) -> None:
        for path in [
            self.original_dir,
            self.analysis_dir,
            self.midi_dir,
            self.render_dir,
            self.mix_dir,
        ]:
            path.mkdir(parents=True, exist_ok=True)
