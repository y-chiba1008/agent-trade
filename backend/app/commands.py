"""開発用コマンド。

`pyproject.toml` の `[project.scripts]` から `uv run dev` / `uv run lint` で起動する。
プロセスを置き換えることで、終了コードとシグナルをそのまま伝える。
"""

import os
import sys
from collections.abc import Sequence
from typing import NoReturn


def _exec(argv: Sequence[str]) -> NoReturn:
    os.execvp(argv[0], list(argv))


def dev() -> None:
    """開発サーバーを起動する（`uvicorn app.main:app --reload`）。"""
    _exec(['uvicorn', 'app.main:app', '--reload', *sys.argv[1:]])


def lint() -> None:
    """Ruff で Lint チェックする（`ruff check .`）。"""
    _exec(['ruff', 'check', '.', *sys.argv[1:]])
