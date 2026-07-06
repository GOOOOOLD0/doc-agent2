# Satellite Landing Permit Regulatory Monitor

这个项目用于整理和监控各国卫星落地许可相关法规来源。当前已完成巴西的第一版最小闭环。

## 当前内容

- `Report_Spacesail_EN.docx`: 原始巴西落地许可流程报告。
- `regulatory_sources/brazil.md`: 人工可读的巴西法规来源台账。
- `regulatory_sources/thailand.md`: 泰国试点来源台账和访问问题记录。
- `regulatory_sources/mongolia.md`: 蒙古试点来源台账和可监控官方 URL。
- `wiki/raw/articles/landing_rights/brazil/source_inventory.md`: 巴西知识抽取用来源清单。
- `wiki/concepts/landing_rights/cases/brazil/10_brazil_answer_template.md`: 巴西落地许可 Agent 回答模板。
- `regulatory_sources/sources.json`: 机器可读的法规 URL 配置。
- `scripts/check_sources.py`: 法规页面抓取、正文归一化、快照保存和更新比对脚本。
- `sources/brazil/`: 巴西法规来源 baseline 快照和检查日志。
- `sources/mongolia/`: 蒙古试点来源 baseline 快照和检查日志。

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

蒙古已完成第一轮试点：CRC 官方许可、无线电频率、设备认证、法律目录页面可抓取；已启用 7 个蒙古来源进入每月监控。三部较大的 legalinfo.mn 法律正文已记录 URL，但暂不启用，待确定快照体积策略后再加入。

下一步可以继续为泰国定位具体官方文件直链，并把蒙古监控源映射成“落地许可流程回答模板”。
