# -*- coding: utf-8 -*-
"""数据搜集层（本项目核心）。

build_manager() 依据配置装配可用的 collector 并交给 CollectorManager 编排。
"""
from config import settings

from .base import BaseCollector, CollectorManager, STANDARD_OHLCV_COLUMNS
from .market_data import MarketDataCollector
from .fundamentals import FundamentalsCollector
from .news import NewsCollector
from .sentiment import SentimentCollector

__all__ = [
    "BaseCollector",
    "CollectorManager",
    "STANDARD_OHLCV_COLUMNS",
    "MarketDataCollector",
    "FundamentalsCollector",
    "NewsCollector",
    "SentimentCollector",
    "build_manager",
]


def build_manager() -> CollectorManager:
    """根据配置装配所有数据源。新增数据源时在此注册。"""
    collectors: list[BaseCollector] = [
        MarketDataCollector(token=settings.TUSHARE_TOKEN),
        FundamentalsCollector(),
        NewsCollector(
            api_keys=settings.TAVILY_API_KEYS + settings.BOCHA_API_KEYS,
            max_age_days=settings.NEWS_MAX_AGE_DAYS,
        ),
        SentimentCollector(
            api_key=settings.SOCIAL_SENTIMENT_API_KEY,
            api_url=settings.SOCIAL_SENTIMENT_API_URL,
        ),
    ]
    return CollectorManager(collectors)
