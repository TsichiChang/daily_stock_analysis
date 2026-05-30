# Investment Data Hub

以「**搜集各种投资相关数据**」为核心的投研数据中台，覆盖 A 股 / 港股 / 美股，串联从数据采集到分析、报告、通知的完整链路。

```
搜集数据 → 清洗/标准化 → 存储 → 分析 → 生成报告 → 通知推送
```

数据搜集是本项目的核心：多市场、多类型（行情 / 基本面 / 新闻 / 社交情绪 / 宏观）、多数据源、自动降级。

## 核心能力

- **多源采集**：每类数据接入多个数据源，统一接口 + 自动故障切换。
- **标准化**：原始字段在采集层消化，对下游输出统一 schema。
- **容错优先**：单源失败不拖垮流水线；缺少某个 Key 时对应源自动跳过。
- **可插拔下游**：分析 / 报告 / 通知作为采集结果的消费方，保持轻量。

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 准备配置（按需填写数据源 Key，不填也能用免费源跑通）
cp .env.example .env

# 3. 运行
python main.py --collect                 # 仅搜集数据
python main.py --symbols 600519,AAPL     # 指定标的
python main.py --pipeline                # 跑完整流水线
python main.py --dry-run                 # 不写存储/不推送，验证链路
```

## 目录结构

| 路径 | 职责 |
| --- | --- |
| `src/collectors/` | 【核心】数据搜集：行情 / 基本面 / 新闻 / 社交情绪 |
| `src/processors/` | 清洗、去重、标准化 |
| `src/storage/` | 持久化与读取 |
| `src/analysis/` | 分析逻辑 |
| `src/reports/` | 报告生成 |
| `src/notify/` | 通知推送 |
| `config/` | 配置加载 |
| `docs/` | 文档与数据源说明 |

## 文档

- 协作与开发规则：[`CLAUDE.md`](CLAUDE.md)
- 数据源说明：[`docs/data-sources.md`](docs/data-sources.md)
- 更新日志：[`docs/CHANGELOG.md`](docs/CHANGELOG.md)

## 配置

所有外部凭据通过环境变量提供，清单见 [`.env.example`](.env.example)。原则：**不配置也可运行，配置后增强能力**。
