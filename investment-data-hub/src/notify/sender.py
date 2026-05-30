# -*- coding: utf-8 -*-
"""通知推送（示例骨架）。

单一渠道失败不应中断主流程。接入真实渠道时在此扩展。
"""
import logging

logger = logging.getLogger(__name__)


def send(content: str) -> bool:
    """推送报告内容。未配置任何渠道时跳过并返回 False。"""
    logger.info("通知内容（未接入真实渠道，仅打印）:\n%s", content)
    return False
