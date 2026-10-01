"""資料集基本驗證，供 CI 或更新流程使用。"""

from __future__ import annotations

from .models import Dataset


REQUIRED_BANKS = {"LINE Bank", "樂天國際銀行", "將來銀行", "王道銀行", "匯豐銀行"}


def validate_dataset(dataset: Dataset) -> list[str]:
    errors: list[str] = []
    names = {bank.bank for bank in dataset.banks}
    missing = REQUIRED_BANKS - names
    if missing:
        errors.append(f"缺少指定銀行：{', '.join(sorted(missing))}")
    for bank in dataset.banks:
        for plan in bank.plans:
            if plan.currency != "TWD":
                errors.append(f"{bank.bank}／{plan.product_name} 不是新台幣方案")
            if plan.official_url == "" or plan.official_url == "待填官方網址":
                errors.append(f"{bank.bank}／{plan.product_name} 官方網址不可為空白佔位值")
    return errors
