# -*- coding: utf-8 -*-
"""新闻 / 资讯 collector（示例骨架）。

接入真实搜索引擎（Tavily / Bocha / Brave / SerpAPI）时，
复用多 Key 负载均衡与超时重试，结果统一为 {title, url, published_at, summary}。
"""
import logging
from typing import Any, Optional

from .base import BaseCollector

logger = logging.getLogger(__name__)


class NewsCollector(BaseCollector):
    """新闻搜索数据源骨架，支持多 Key。"""

    priority = 30

    def __init__(self, api_keys: Optional[list[str]] = None, max_age_days: int = 3):
        self._api_keys = api_keys or []
        self._max_age_days = max_age_days

    @property
    def name(self) -> str:
        return "news"

    def available(self) -> bool:
        # 配置了至少一个 Key 才启用
        return bool(self._api_keys)

    def collect_news(self, symbol: str) -> Optional[Any]:
        logger.debug("NewsCollector 暂未接入真实搜索引擎: %s", symbol)
        return None
