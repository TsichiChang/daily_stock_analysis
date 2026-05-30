# -*- coding: utf-8 -*-
"""集中式配置加载。

所有外部凭据与运行参数从环境变量读取（配合 .env），
不在代码中写死密钥、Token、路径。
"""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv 未安装时不阻断
    pass


def _keys(name: str) -> list[str]:
    """读取逗号分隔的多 Key 配置，去空白后返回列表。"""
    raw = os.getenv(name, "")
    return [k.strip() for k in raw.split(",") if k.strip()]


# 运行
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))

# 行情 / 基本面数据源
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN", "")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", "")

# 新闻 / 搜索数据源（多 Key）
TAVILY_API_KEYS = _keys("TAVILY_API_KEYS")
BOCHA_API_KEYS = _keys("BOCHA_API_KEYS")
BRAVE_API_KEYS = _keys("BRAVE_API_KEYS")
SERPAPI_API_KEYS = _keys("SERPAPI_API_KEYS")
NEWS_MAX_AGE_DAYS = int(os.getenv("NEWS_MAX_AGE_DAYS", "3"))

# 社交情绪
SOCIAL_SENTIMENT_API_KEY = os.getenv("SOCIAL_SENTIMENT_API_KEY", "")
SOCIAL_SENTIMENT_API_URL = os.getenv("SOCIAL_SENTIMENT_API_URL", "")

# 通知
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL", "")
WECOM_WEBHOOK_URL = os.getenv("WECOM_WEBHOOK_URL", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
