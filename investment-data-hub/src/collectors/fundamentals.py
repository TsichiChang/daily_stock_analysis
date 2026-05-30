# -*- coding: utf-8 -*-
"""基本面数据 collector（示例骨架）。"""
import logging
from typing import Any, Optional

from .base import BaseCollector

logger = logging.getLogger(__name__)


class FundamentalsCollector(BaseCollector):
    """基本面（PE / PB / 市值等）数据源骨架。"""

    priority = 20

    @property
    def name(self) -> str:
        return "fundamentals"

    def available(self) -> bool:
        return True

    def collect_fundamentals(self, symbol: str) -> Optional[Any]:
        logger.debug("FundamentalsCollector 暂未接入真实数据源: %s", symbol)
        return None
