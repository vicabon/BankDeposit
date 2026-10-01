"""JSON 讀寫工具。"""

from __future__ import annotations

import json
from pathlib import Path

from .models import Dataset


def read_dataset(path: str | Path) -> Dataset:
    with Path(path).open("r", encoding="utf-8") as handle:
        return Dataset.from_dict(json.load(handle))


def write_dataset(dataset: Dataset, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(dataset.to_dict(), handle, ensure_ascii=False, indent=2)
        handle.write("\n")
