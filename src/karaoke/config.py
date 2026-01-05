from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    root: Path

    @property
    def input(self) -> Path:
        return self.root / "input" / "songs"

    @property
    def work(self) -> Path:
        return self.root / "work" / "songs"

    @property
    def output(self) -> Path:
        return self.root / "output" / "songs"

    @property
    def assets(self) -> Path:
        return self.root / "assets"


DEFAULT_PATHS = ProjectPaths(root=Path(__file__).resolve().parents[2])
