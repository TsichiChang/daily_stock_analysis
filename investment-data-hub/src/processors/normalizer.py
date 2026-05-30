# -*- coding: utf-8 -*-
"""标准化工具。

把不同数据源采集到的原始记录归一为统一结构，便于存储与下游消费。
"""
from typing import Any


def normalize_record(symbol: str, raw: dict[str, Any]) -> dict[str, Any]:
    """归一化一条采集记录。

    约定输出至少包含 symbol 字段；缺失值保留为 None，由下游决定如何处理。
    """
    record = dict(raw or {})
    record.setdefault("symbol", symbol)
    return record
