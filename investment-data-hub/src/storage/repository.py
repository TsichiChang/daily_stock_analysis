# -*- coding: utf-8 -*-
"""存储读写（示例：JSON 文件落盘骨架）。

接入数据库时保持同一接口（save / load），不改变下游调用方。
"""
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class Repository:
    def __init__(self, data_dir: Path):
        self._dir = Path(data_dir)
        self._dir.mkdir(parents=True, exist_ok=True)

    def save(self, symbol: str, record: dict[str, Any]) -> None:
        path = self._dir / f"{symbol}.json"
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("已保存 %s -> %s", symbol, path)

    def load(self, symbol: str) -> dict[str, Any]:
        path = self._dir / f"{symbol}.json"
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))
