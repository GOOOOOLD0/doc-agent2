# Satellite Landing Permit Regulatory Monitor

这个项目用于整理、监控和分析各国卫星落地许可相关法规来源。当前已完成巴西和蒙古知识库，并提供可独立运行的命令行 Agent。

## 当前内容

- `Report_Spacesail_EN.docx`: 原始巴西落地许可流程报告。
- `regulatory_sources/brazil.md`: 人工可读的巴西法规来源台账。
- `regulatory_sources/thailand.md`: 泰国试点来源台账和访问问题记录。
- `regulatory_sources/mongolia.md`: 蒙古试点来源台账和可监控官方 URL。
- `wiki/raw/landing_rights/brazil/source_inventory.md`: 巴西知识抽取用来源清单。
- `wiki/concepts/landing_rights/cases/brazil/10_brazil_answer_template.md`: 巴西落地许可 Agent 回答模板。
- `wiki/raw/landing_rights/mongolia/source_inventory.md`: 蒙古知识抽取用来源清单。
- `wiki/concepts/landing_rights/cases/mongolia/10_mongolia_answer_template.md`: 蒙古落地许可 Agent 回答模板。
- `regulatory_sources/sources.json`: 机器可读的法规 URL 配置。
- `scripts/check_sources.py`: 法规页面抓取、正文归一化、快照保存和更新比对脚本。
- `landing_rights_agent/`: 独立运行的卫星落地许可 Agent 程序。
- `skills/satellite-landing-rights/SKILL.md`: 正式的 Satellite Landing Rights Analysis Skill。
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

### 独立 Agent

首次使用时创建本地环境文件：

```bash
cp .env.example .env
```

在 `.env` 中填写 `DASHSCOPE_API_KEY`。该文件已加入 `.gitignore`，不得提交到 GitHub，也不要把密钥发送到聊天中。

默认配置使用阿里云百炼的 `qwen3.6-flash` 和 OpenAI 兼容 Responses API。低成本批量摘要可以临时将 `LANDING_RIGHTS_MODEL` 改为 `qwen3.5-flash`。

检查环境：

```bash
python3 -m landing_rights_agent doctor
```

回答已有国家问题：

```bash
python3 -m landing_rights_agent answer \
  --country mongolia \
  --question "蒙古卫星宽带落地需要哪些许可？"
```

同时检索最新官方网页：

```bash
python3 -m landing_rights_agent answer \
  --country mongolia \
  --question "蒙古卫星宽带落地需要哪些许可？" \
  --web
```

研究新国家并保存报告：

```bash
python3 -m landing_rights_agent research \
  --country indonesia \
  --output indonesia-research.md
```

根据已经核验的 source notes 生成 `00-10` 预览：

```bash
python3 -m landing_rights_agent build-country --country mongolia
```

默认预览保存在 `.agent_runs/`，不会修改 Wiki。人工确认任务范围后，使用 `--apply` 写入正式 cases 目录；生成文件仍保持 `review_status: draft`。

### GitHub 每月自动运行

仓库已配置 `.github/workflows/monthly-regulatory-check.yml`：

- 每月 1 日北京时间 09:00 自动运行一次。
- 也可以在 GitHub 的 Actions 页面手动触发 `Monthly regulatory source check`。
- 脚本会抓取 `regulatory_sources/sources.json` 里启用监控的 URL。
- 如果网页内容和上一次快照一致，会在对应 `checks.md` 里记录 `no-update`。
- 如果网页内容发生变化，会保存新快照并由 GitHub Actions 自动提交到仓库。

注意：GitHub 的定时任务只有在 workflow 文件合并到仓库默认分支后才会按月自动触发。当前分支可以先手动运行验证。

## 当前状态

已监控 10 个巴西法规来源，重复运行验证结果为 `no-update`。`Act No. 9,526/2021` 尚未确认到官方 URL，暂未加入监控队列。

泰国已完成第一轮试点：NBTC 与 Royal Gazette 官方入口在脚本环境中返回 Cloudflare / HTTP 403，暂不加入每月监控；MDES 法规目录可抓取，但尚未确认属于卫星落地许可核心来源。

蒙古已完成扩展试点：CRC 官方许可、无线电频率、设备认证、法律目录页面和 Legalinfo.mn 法规正文均可抓取；13 个蒙古官方来源已进入每月监控，其中包括第 37/2022 号决议附件、三部基础法律、《投资法》和频率收费规则。

蒙古正式 `00-10` cases 已完成。下一步可使用独立 Agent 对新的试点国家执行 `research`，经人工核验并形成 source notes 后，再运行 `build-country`。
