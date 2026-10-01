"""提供不抓取銀行網站的資料驗證命令。"""

import argparse
import sys

from .io import read_dataset
from .validate import validate_dataset


def main() -> int:
    parser = argparse.ArgumentParser(description="驗證新台幣定存資料 JSON")
    parser.add_argument("path", help="latest.json 路徑")
    args = parser.parse_args()
    errors = validate_dataset(read_dataset(args.path))
    if errors:
        for error in errors:
            print(f"錯誤：{error}")
        return 1
    print("資料結構驗證通過；本命令不會抓取銀行網站。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
