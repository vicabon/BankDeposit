"""資料模型。

本模組只定義與驗證資料結構，不負責連線或擷取銀行網站。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PlanStatus(str, Enum):
    AVAILABLE = "available"
    NOT_STARTED = "not_started"
    ENDED = "ended"
    CANCELLED = "cancelled"
    FULL = "full"
    UNKNOWN = "unknown"
    NEEDS_REVIEW = "needs_review"


@dataclass
class DepositPlan:
    bank: str
    product_name: str
    currency: str = "TWD"
    term: str = "官方資料未載明"
    annual_rate: str = "官方資料未載明"
    minimum_amount: str = "官方資料未載明"
    maximum_amount: str = "官方資料未載明"
    interest_payment: str = "官方資料未載明"
    eligibility: str = "官方資料未載明"
    new_customer_only: bool | None = None
    new_account_only: bool | None = None
    new_funds_required: bool | None = None
    status: PlanStatus = PlanStatus.UNKNOWN
    start_date: str | None = None
    end_date: str | None = None
    official_url: str | None = None
    evidence_urls: list[str] = field(default_factory=list)
    evidence_notes: list[str] = field(default_factory=list)
    checked_at: str | None = None
    source_status: str = "尚未取得官方資料"

    def to_dict(self) -> dict[str, Any]:
        result = dict(self.__dict__)
        result["status"] = self.status.value
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DepositPlan":
        values = dict(data)
        values["status"] = PlanStatus(values.get("status", PlanStatus.UNKNOWN))
        return cls(**values)


@dataclass
class BankRecord:
    bank: str
    search_status: str = "尚未搜尋"
    last_attempted_at: str | None = None
    last_successful_check_at: str | None = None
    data_version: str | None = None
    plans: list[DepositPlan] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        result = dict(self.__dict__)
        result["plans"] = [plan.to_dict() for plan in self.plans]
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BankRecord":
        values = dict(data)
        values["plans"] = [DepositPlan.from_dict(item) for item in values.get("plans", [])]
        return cls(**values)


@dataclass
class Dataset:
    schema_version: str = "1.0"
    generated_at: str | None = None
    timezone: str = "Asia/Taipei"
    data_status: str = "尚未取得官方資料"
    banks: list[BankRecord] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        result = dict(self.__dict__)
        result["banks"] = [bank.to_dict() for bank in self.banks]
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Dataset":
        values = dict(data)
        values["banks"] = [BankRecord.from_dict(item) for item in values.get("banks", [])]
        return cls(**values)
