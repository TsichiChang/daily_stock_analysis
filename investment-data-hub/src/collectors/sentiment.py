# -*- coding: utf-8 -*-
"""社交情绪 collector（示例骨架，仅美股）。"""
import logging
from typing import Any, Optional

from .base import BaseCollector

logger = logging.getLogger(__name__)


class SentimentCollector(BaseCollector):
    """Reddit / X / Polymarket 等社交情绪数据源骨架。可选，仅美股启用。"""

    priority = 40

    def __init__(self, api_key: str = "", api_url: str = ""):
        self._api_key = api_key
        self._api_url = api_url

    @property
    def name(self) -> str:
        return "sentiment"

    def available(self) -> bool:
        return bool(self._api_key)

    def collect_news(self, symbol: str) -> Optional[Any]:
        # 社交情绪并入 news 通道作为补充信号；非美股可在此判断后跳过。
        logger.debug("SentimentCollector 暂未接入真实数据源: %s", symbol)
        return None
