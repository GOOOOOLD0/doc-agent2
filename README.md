# Satellite Landing Permit Regulatory Monitor

这个项目用于整理、监控和分析各国卫星落地许可相关法规来源。正式知识由 Codex 或人工依据官方资料生成和审核，Hermes 读取正式知识库回答问题并执行更新研究。

## 当前内容

- `Report_Spacesail_EN.docx`: 原始巴西落地许可流程报告。
- `regulatory_sources/brazil.md`: 人工可读的巴西法规来源台账。
- `regulatory_sources/thailand.md`: 泰国试点来源台账和访问问题记录。
- `regulatory_sources/mongolia.md`: 蒙古试点来源台账和可监控官方 URL。
- `wiki/raw/landing_rights/brazil/source_inventory.md`: 巴西知识抽取用来源清单。
- `wiki/raw/landing_rights/mongolia/source_inventory.md`: 蒙古知识抽取用来源清单。
- `wiki/raw/landing_rights/<country>/source_notes/`: 从单个官方来源提取的结构化笔记。
- `wiki/raw/landing_rights/<country>/evidence_matrix.md`: 正式案例生成前的证据矩阵。
- `wiki/concepts/landing_rights/cases/<country>/`: 经审核的国家案例文件。
- `regulatory_sources/sources.json`: 机器可读的法规 URL 配置。
- `scripts/check_sources.py`: 法规页面抓取、正文归一化、快照保存和更新比对脚本。
- `tools/landing_rights/`: Evidence Matrix 和正式案例的确定性校验工具。
- `skills/satellite-landing-rights/SKILL.md`: 正式的 Satellite Landing Rights Analysis Skill。
- `AGENT.md`: Hermes 项目入口和角色边界。
- `AGENTS.md`: Codex 项目入口。
- `landing_rights_agent/`: 保留的实验性命令行程序，不作为正式知识写入入口。
- `wiki/raw/landing_rights/brazil/sources/`: 巴西法规来源 baseline 快照和检查日志。
- `wiki/raw/landing_rights/mongolia/sources/`: 蒙古法规来源 baseline 快照和检查日志。

## 运行方式

### 本地运行

创建或更新快照：

```bash
python3 scripts/check_sources.py
```

只检查是否有更新、不写入文件：

```bash
python3 scripts/check_sources.py --dry-run
```

指定日期生成快照：

```bash
python3 scripts/check_sources.py --date 2026-06-23
```

### 正式知识生产

正式国家案例遵循以下流程：

1. 收集目标国官方法规、监管页面、申请指南和附件；
2. 更新 `source_inventory.md`，保存原始资料并逐个生成 source note；
3. 由 Codex 或人工审核 source notes，建立 `evidence_matrix.md`；
4. 依据 Evidence Matrix 和 common 规范生成或更新 `00-09`；
5. 运行确定性校验，并对法律翻译、许可边界、费用和周期进行人工复核；
6. 复核完成前保持 `review_status: draft`。

巴西案例只提供结构样板和检查清单，不得作为其他国家法律结论的依据。详细规则见：

- `AGENT.md`
- `skills/satellite-landing-rights/SKILL.md`
- `wiki/concepts/landing_rights/common/`

校验蒙古 Evidence Matrix：

```bash
python3 tools/landing_rights/validate_evidence_matrix.py --country mongolia
```

校验已经按新矩阵复核的蒙古正式 `08`：

```bash
python3 tools/landing_rights/validate_cases.py --country mongolia --files 08
```

检查整套 `01-09` 并列出尚未吸收的证据：

```bash
python3 tools/landing_rights/validate_cases.py --country mongolia
```

校验通过表示文件结构、证据登记和内部链接符合项目规则，不代表法律结论已经自动获得权威确认。

### Hermes 问答与研究

Hermes 读取正式 Wiki 回答已有国家问题，也可以研究新国家或检查更新，但不得直接覆盖正式 source notes、Evidence Matrix 或 `00-09`。

Hermes 的研究草稿和更新建议统一写入：

```text
.agent_runs/hermes/
```

需要进入正式知识库的内容，由 Codex 或人工复核官方原文后再写入。旧的 `landing_rights_agent/` 保留用于实验和兼容测试，不作为正式知识生产入口。

### GitHub 每月自动运行

仓库已配置 `.github/workflows/monthly-regulatory-check.yml`：

- 每月 1 日北京时间 09:00 自动运行一次。
- 也可以在 GitHub 的 Actions 页面手动触发 `Monthly regulatory source check`。
- 脚本会抓取 `regulatory_sources/sources.json` 里启用监控的 URL。
- 如果网页内容和上一次快照一致，会在对应 `checks.md` 里记录 `no-update`。
- 如果网页内容发生变化，会保存新快照并由 GitHub Actions 自动提交到仓库。

注意：GitHub 的定时任务只有在 workflow 文件合并到仓库默认分支后才会按月自动触发。当前分支可以先手动运行验证。

## 当前状态

巴西已经建立官方来源台账、原始资料、source notes 和正式案例。月度监控可识别网页更新，但监控结果仍需经过正式知识生产流程后才能改变法律结论。

泰国已完成第一轮试点。部分 NBTC 页面和附件存在 Cloudflare / HTTP 403，当前资料尚不足以生成完整正式案例，需要继续补齐可复核的官方原文。

蒙古现有 27 份正式 source notes，覆盖 CRC 许可、无线电频率、设备认证、Legalinfo.mn 法规正文、投资和收费规则。Evidence Matrix 已完成正式审核，共登记 25 条证据；正式 `08_mongolia_regulations.md` 已据此重建。

蒙古其余 `01-07`、`09` 仍需按照已审核 Evidence Matrix 逐文件复核。后续新增国家必须先完成 research、source notes 和 Evidence Matrix，再进入正式 cases。
