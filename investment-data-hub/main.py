# -*- coding: utf-8 -*-
"""Investment Data Hub 命令行入口。

串联：搜集 → 标准化 → 存储 → 分析 → 报告 → 通知。
"""
import argparse
import logging

from config import settings
from src.collectors import build_manager
from src.processors import normalize_record
from src.storage import Repository
from src.analysis import analyze
from src.reports import build_report
from src.notify import send

logger = logging.getLogger(__name__)


def collect_one(manager, symbol: str) -> dict:
    """对单个标的搜集各类数据并标准化。"""
    raw = {
        "quotes": manager.quotes(symbol),
        "fundamentals": manager.fundamentals(symbol),
        "news": manager.news(symbol),
    }
    return normalize_record(symbol, raw)


def run(symbols: list[str], *, collect_only: bool, dry_run: bool) -> None:
    manager = build_manager()
    repo = Repository(settings.DATA_DIR)

    results = []
    for symbol in symbols:
        record = collect_one(manager, symbol)
        if not dry_run:
            repo.save(symbol, record)
        if collect_only:
            logger.info("已搜集 %s", symbol)
            continue
        results.append(analyze(symbol, record))

    if collect_only or not results:
        return

    report = build_report(results)
    if dry_run:
        print(report)
    else:
        send(report)


def main() -> None:
    parser = argparse.ArgumentParser(description="Investment Data Hub")
    parser.add_argument("--symbols", default="600519",
                        help="逗号分隔的标的代码，如 600519,AAPL")
    parser.add_argument("--collect", action="store_true", help="仅搜集数据")
    parser.add_argument("--pipeline", action="store_true", help="跑完整流水线")
    parser.add_argument("--dry-run", action="store_true",
                        help="不写存储/不推送，仅验证链路")
    args = parser.parse_args()

    logging.basicConfig(level=settings.LOG_LEVEL,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    run(symbols, collect_only=args.collect and not args.pipeline, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
