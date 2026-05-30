# 数据源说明

本页记录 Investment Data Hub 各类数据的来源、配置与降级策略。新增数据源时同步更新本页。

## 数据面与采集层

| 数据面 | Collector | 配置项 | 说明 |
| --- | --- | --- | --- |
| 行情（OHLCV） | `MarketDataCollector` | `TUSHARE_TOKEN`（可选） | 输出标准列名 `date/open/high/low/close/volume/amount/pct_chg` |
| 基本面 | `FundamentalsCollector` | — | PE / PB / 市值等 |
| 新闻 / 资讯 | `NewsCollector` | `TAVILY_API_KEYS` / `BOCHA_API_KEYS`（多 Key 逗号分隔） | 配置至少一个 Key 才启用 |
| 社交情绪 | `SentimentCollector` | `SOCIAL_SENTIMENT_API_KEY` | 可选，仅美股 |

## 降级与容错

- 所有 collector 继承 `BaseCollector`，由 `CollectorManager` 按 `priority` 排序。
- 取数时依次尝试每个可用源，第一个返回非 None 即采纳。
- 单源失败（异常或返回 None）自动切到下一个源，不中断流水线。
- 缺少凭据的源在 `available()` 返回 False，被 manager 直接跳过。

## 接入真实数据源步骤

1. 在 `src/collectors/` 新建或扩展 collector，继承 `BaseCollector`。
2. 实现 `name`、`available` 和需要的 `collect_*` 方法；在内部完成限流与字段标准化。
3. 在 `src/collectors/__init__.py` 的 `build_manager()` 注册，并设置合适的 `priority`。
4. 如需新凭据，更新 `.env.example`、`config/settings.py` 与本页。
5. 补充对应测试，离线场景下应能安全降级。
