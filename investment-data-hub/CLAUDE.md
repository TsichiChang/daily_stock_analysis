# CLAUDE.md — Investment Data Hub

本文件是本仓库的 AI 协作与开发约束的唯一真源，目标是减少重复沟通、减少返工，并让改动与项目结构保持一致。

如果本文件与仓库中的实际脚本、代码、配置不一致，**以实际可执行内容为准**，并在相关改动中顺手修正本文件，避免规则漂移。

## 0. 项目定位

**Investment Data Hub** 是一个以「**搜集各种投资相关数据**」为核心的投研数据中台。

主流程（全链路）：

```
搜集数据 → 清洗/标准化 → 存储 → 分析 → 生成报告 → 通知推送
collect  →  process     → store →  analyze → report → notify
```

- **核心工作是数据搜集（collect）**：多市场（A 股 / 港股 / 美股）、多类型（行情、基本面、新闻、社交情绪、宏观）、多数据源、自动降级。
- 分析、报告、通知是搜集到的数据的下游消费方，保持轻量、可插拔。
- 设计目标：**新增数据源/字段成本低**，**单一数据源失败不拖垮整条流水线**。

## 1. 硬规则

- 遵循现有目录边界（见第 3 节），不新增平行实现，优先复用现有 collector / processor / 配置入口。
- 未经明确确认，不执行 `git commit`、`git tag`、`git push`。
- commit message 使用英文，不添加 `Co-Authored-By`。
- **不写死密钥、Token、账号、绝对路径、模型名、端口**；所有外部凭据走环境变量。
- 新增配置项时，必须同步更新 `.env.example` 和相关文档。
- 默认稳定性优先于「顺手优化」；与当前任务无关的重构、抽象、依赖迁移一律克制。
- 涉及用户可见行为、CLI/接口、数据字段、数据源、通知方式、报告结构变化时，同步更新 `docs/` 与 `docs/CHANGELOG.md`。
- 注释、docstring、日志文案以清晰准确为准，与文件语境保持一致即可，不强制英文。

## 2. 数据搜集硬约束（本项目重点）

新增或修改数据源（`src/collectors/`）时必须遵守：

1. **统一接口**：所有数据源继承 `BaseCollector`，实现其抽象方法；通过 `CollectorManager` 注册并参与降级排序。
2. **字段标准化**：对外输出统一 schema（标准列名 / 标准字段），原始字段的差异在 collector 内部消化，不外溢到下游。
3. **降级与容错**：单源失败 → 自动切换下一个源；瞬时网络错误走超时 + 指数退避重试；任一源失败**不得**抛出未捕获异常中断整条流水线（除非任务明确要求 fail-fast）。
4. **流控防封禁**：对有频率限制的源内置限流；免费源默认可用，付费/限额源仅作增强或兜底。
5. **可观测**：每次取数记录来源、耗时、成功/失败，便于排查降级链路。
6. **不配置也能跑**：缺少某个 Key 时，对应源应自动跳过而非报错；「不配置可运行，配置后增强能力」。

## 3. 目录结构

```
investment-data-hub/
├── CLAUDE.md            # 本文件：协作规则唯一真源
├── README.md            # 项目概览与快速开始
├── .env.example         # 配置项清单（新增配置必须同步）
├── requirements.txt
├── main.py              # 命令行入口
├── config/             # 配置加载（settings）
├── src/
│   ├── collectors/     # 【核心】数据搜集：行情/基本面/新闻/情绪/宏观
│   ├── processors/     # 清洗、去重、标准化
│   ├── storage/        # 持久化与读取
│   ├── analysis/       # 分析逻辑
│   ├── reports/        # 报告生成
│   └── notify/         # 通知推送
├── tests/              # pytest 测试
└── docs/               # 文档与数据源说明
```

边界：
- 数据搜集相关改动 → `src/collectors/`
- 清洗/标准化 → `src/processors/`
- 存储读写 → `src/storage/`
- 分析 / 报告 / 通知 → 对应 `src/analysis|reports|notify/`
- 配置入口 → `config/`、`.env.example`

## 4. 常用命令

```bash
# 安装依赖
pip install -r requirements.txt

# 运行（采集 + 全流程）
python main.py --collect                 # 仅搜集数据
python main.py --symbols 600519,AAPL     # 指定标的
python main.py --pipeline                # 跑完整流水线
python main.py --dry-run                 # 不写存储/不推送，验证链路

# 测试与静态检查
python -m pytest -q
python -m pytest -m "not network"        # 跳过联网用例
python -m py_compile $(git diff --name-only '*.py')
flake8 src tests
```

> 上述命令以实际实现为准；新增 CLI 参数时同步更新本节与 `README.md`。

## 5. 默认工作流

1. 判断任务类型：`feat / fix / refactor / docs / chore / test`。
2. 先读现有 collector / processor / 配置 / 测试，再动手；优先复用，不夹带无关重构。
3. 识别改动边界：搜集 / 处理 / 存储 / 分析 / 报告 / 通知 / 配置 / 文档。
4. 高风险区优先确认：数据源优先级与降级、字段 schema、存储结构、调度、凭据处理。
5. 只做与当前任务直接相关的最小改动。
6. 按第 6 节验证矩阵执行检查。
7. 交付说明默认包含：**改了什么 / 为什么 / 验证情况 / 未验证项 / 风险点 / 回滚方式**。

## 6. 验证矩阵

- 数据搜集 / 处理 / 存储改动（`src/`）：
  - 最低：`python -m py_compile <changed_files>` + 相关 `pytest`
  - 涉及联网数据源时：先跑离线/确定性用例，确认 timeout / retry / fallback / 降级文案仍成立；若未做在线验证，需写明原因。
  - 涉及字段 schema 变化：必须说明对下游（分析/报告/通知）的兼容性，优先追加字段、保留旧字段。
- 文档改动（`docs/`、`README.md`、`CLAUDE.md`）：不强制跑测试，但需核对命令、配置项、文件名与实际仓库一致。
- 配置改动（`.env.example`、`config/`）：确认「不配置也可运行」，并同步文档。

## 7. 稳定性护栏

- **数据源**：改动优先级、降级、字段标准化、缓存、超时策略时要整体评估；单源失败不应中断流水线。
- **字段契约**：改 schema / 报告载荷时，默认追加字段或保留旧字段，避免无提示破坏下游。
- **通知**：单一通知渠道失败不应拖垮主流程（除非明确要求 fail-fast）。
- **凭据**：所有 Key/Token 仅从环境变量读取；日志与报告中不得回显敏感凭据。

## 8. 交付与发布

- 默认交付结构：`改了什么 / 为什么这么改 / 验证情况 / 未验证项 / 风险点 / 回滚方式`。
- 纯文档任务可写：`Docs only, tests not run`，但仍需核对命令与文件名。
- 用户可见变更优先通过 PR 合入，并补齐验证说明。
- 手动打 tag 使用 annotated tag。
