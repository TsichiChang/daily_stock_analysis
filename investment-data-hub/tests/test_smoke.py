# -*- coding: utf-8 -*-
"""冒烟测试：验证装配与降级链路在无外部依赖时能跑通。"""
from src.collectors import build_manager
from src.processors import normalize_record
from src.analysis import analyze
from src.reports import build_report


def test_manager_builds():
    manager = build_manager()
    # 无凭据时所有取数应安全返回 None，而不是抛异常
    assert manager.quotes("600519") is None
    assert manager.fundamentals("600519") is None
    assert manager.news("600519") is None


def test_normalize_sets_symbol():
    record = normalize_record("AAPL", {"quotes": None})
    assert record["symbol"] == "AAPL"


def test_pipeline_report():
    record = normalize_record("AAPL", {"quotes": None, "fundamentals": None, "news": None})
    result = analyze("AAPL", record)
    report = build_report([result])
    assert "AAPL" in report
