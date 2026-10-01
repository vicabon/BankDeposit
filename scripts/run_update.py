#!/usr/bin/env python3
"""執行一次安全的資料更新流程。

目前階段只驗證既有資料並同步至 GitHub Pages 目錄；尚未擷取銀行網站。
未來加入官方來源擷取器時，應在此流程的擷取階段產生新的 Dataset，
再通過同一套驗證後發布。
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from qgenie_deposit.io import read_dataset
from qgenie_deposit.validate import validate_dataset


def main() -> int:
    parser = argparse.ArgumentParser(description="驗證並發布靜態資料，不擷取銀行網站")
    parser.add_argument("--source", default="data/latest.json")
    parser.add_argument("--site", default="site")
    parser.add_argument("--dry-run", action="store_true", help="只驗證，不同步 site/latest.json")
    args = parser.parse_args()

    source = Path(args.source)
    site = Path(args.site)
    dataset = read_dataset(source)
    errors = validate_dataset(dataset)
    if errors:
        for error in errors:
            print(f"錯誤：{error}")
        return 1

    checked_at = datetime.now(ZoneInfo("Asia/Taipei")).isoformat(timespec="seconds")
    manifest = {
        "run_status": "validated_only",
        "official_fetch_executed": False,
        "checked_at": checked_at,
        "data_generated_at": dataset.generated_at,
        "message": "目前尚未執行銀行官方網站擷取；資料不代表目前沒有方案。",
    }

    if not args.dry_run:
        site.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, site / "latest.json")
        (site / "update-status.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(f"資料驗證通過；模式={'dry-run' if args.dry_run else '同步靜態站'}；檢查時間={checked_at}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
