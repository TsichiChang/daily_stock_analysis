# -*- coding: utf-8 -*-
"""数据搜集基类与管理器（本项目核心）。

设计：
- BaseCollector: 抽象基类，定义统一的取数接口。
- CollectorManager: 按优先级管理多个 collector，实现自动降级。

约束（见 CLAUDE.md 第 2 节）：
- 单源失败自动切换下一个源，不中断整条流水线。
- 字段标准化在 collector 内部完成，对下游输出统一 schema。
"""
import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)

# 行情数据标准列名
STANDARD_OHLCV_COLUMNS = [
    "date", "open", "high", "low", "close", "volume", "amount", "pct_chg",
]


class BaseCollector(ABC):
    """所有数据源 collector 的统一接口。

    子类至少实现 `name`、`available` 与一个或多个 `collect_*` 方法；
    未支持的数据类型返回 None，由 manager 继续向下降级。
    """

    #: 数字越小越优先
    priority: int = 100

    @property
    @abstractmethod
    def name(self) -> str:
        """数据源名称，用于日志与可观测。"""

    @abstractmethod
    def available(self) -> bool:
        """凭据/依赖是否就绪。不就绪时 manager 会跳过该源。"""

    def collect_quotes(self, symbol: str) -> Optional[Any]:
        """采集行情（OHLCV）。未支持返回 None。"""
        return None

    def collect_fundamentals(self, symbol: str) -> Optional[Any]:
        """采集基本面。未支持返回 None。"""
        return None

    def collect_news(self, symbol: str) -> Optional[Any]:
        """采集相关新闻。未支持返回 None。"""
        return None


class CollectorManager:
    """按优先级编排多个 collector，实现自动降级。"""

    def __init__(self, collectors: list[BaseCollector]):
        # 只保留可用源，并按优先级排序
        self._collectors = sorted(
            [c for c in collectors if c.available()],
            key=lambda c: c.priority,
        )
        logger.info(
            "CollectorManager 就绪，可用数据源: %s",
            [c.name for c in self._collectors] or "(无)",
        )

    def _run(self, method: str, symbol: str) -> Optional[Any]:
        """依次尝试每个源的指定方法，第一个成功的结果即返回。"""
        last_error: Optional[Exception] = None
        for collector in self._collectors:
            fn: Callable = getattr(collector, method)
            try:
                result = fn(symbol)
                if result is not None:
                    logger.debug("%s 命中 %s(%s)", collector.name, method, symbol)
                    return result
            except Exception as exc:  # 单源失败不中断，继续降级
                last_error = exc
                logger.warning("%s.%s(%s) 失败: %s", collector.name, method, symbol, exc)
        if last_error is not None:
            logger.error("%s(%s) 所有数据源均失败", method, symbol)
        return None

    def quotes(self, symbol: str) -> Optional[Any]:
        return self._run("collect_quotes", symbol)

    def fundamentals(self, symbol: str) -> Optional[Any]:
        return self._run("collect_fundamentals", symbol)

    def news(self, symbol: str) -> Optional[Any]:
        return self._run("collect_news", symbol)
