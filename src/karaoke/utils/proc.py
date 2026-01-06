from __future__ import annotations

import subprocess
from dataclasses import dataclass


@dataclass
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str


class CommandError(RuntimeError):
    def __init__(self, result: CommandResult):
        super().__init__(f"Command failed: {' '.join(result.command)}")
        self.result = result


def run_command(command: list[str], *, check: bool = True) -> CommandResult:
    completed = subprocess.run(command, capture_output=True, text=True)
    result = CommandResult(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )
    if check and completed.returncode != 0:
        raise CommandError(result)
    return result
