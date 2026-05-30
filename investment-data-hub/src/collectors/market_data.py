# -*- coding: utf-8 -*-
"""行情数据 collector（示例骨架）。

接入真实数据源时，在 `collect_quotes` 内调用对应 SDK / API，
并把原始字段映射成 STANDARD_OHLCV_COLUMNS 标准列名。
"""
import logging
from typing import Any, Optional

from .base import BaseCollector

logger = logging.getLogger(__name__)


class MarketDataCollector(BaseCollector):
    """行情（OHLCV）数据源骨架。

    TODO: 在此接入 tushare / efinance / akshare / yfinance 等具体源，
    并实现内部限流与字段标准化。
    """

    priority = 10

    def __init__(self, token: str = ""):
        self._token = token

    @property
    def name(self) -> str:
        return "market_data"

    def available(self) -> bool:
        # 免费源无需凭据即可用；接入付费源后改为校验 token
        return True

    def collect_quotes(self, symbol: str) -> Optional[Any]:
        # 占位实现：返回 None 表示尚未接入真实源，交由 manager 继续降级。
        logger.debug("MarketDataCollector 暂未接入真实数据源: %s", symbol)
        return None
