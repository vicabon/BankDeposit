"""依 README 規則判斷方案狀態與是否可進入主要結果。"""

from __future__ import annotations

from datetime import date

from .models import DepositPlan, PlanStatus


def status_for_date(plan: DepositPlan, today: date) -> PlanStatus:
    """依日期與官方已知狀態判斷；缺少必要資料時保留未知，不猜測。"""
    if plan.status in {PlanStatus.CANCELLED, PlanStatus.FULL}:
        return plan.status
    if plan.status == PlanStatus.NEEDS_REVIEW:
        return plan.status
    if plan.start_date:
        try:
            if today < date.fromisoformat(plan.start_date):
                return PlanStatus.NOT_STARTED
        except ValueError:
            return PlanStatus.UNKNOWN
    if plan.end_date:
        try:
            if today > date.fromisoformat(plan.end_date):
                return PlanStatus.ENDED
        except ValueError:
            return PlanStatus.UNKNOWN
    if not plan.official_url or plan.source_status != "已完成官方資料校對":
        return PlanStatus.UNKNOWN
    return PlanStatus.AVAILABLE


def is_new_customer_restricted(plan: DepositPlan) -> bool:
    return plan.new_customer_only is True or plan.new_account_only is True


def eligible_for_display(plan: DepositPlan, today: date) -> bool:
    """只有官方可確認、非新客／新開戶限定、且今日可承作才顯示。"""
    if plan.currency != "TWD":
        return False
    if is_new_customer_restricted(plan):
        return False
    return status_for_date(plan, today) == PlanStatus.AVAILABLE


def filter_display_plans(plans: list[DepositPlan], today: date) -> list[DepositPlan]:
    return [plan for plan in plans if eligible_for_display(plan, today)]
