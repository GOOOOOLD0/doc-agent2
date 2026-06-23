# Satellite Landing Permit Regulatory Monitor

这个项目用于整理和监控各国卫星落地许可相关法规来源。当前已完成巴西的第一版最小闭环。

## 当前内容

- `Report_Spacesail_EN.docx`: 原始巴西落地许可流程报告。
- `regulatory_sources/brazil.md`: 人工可读的巴西法规来源台账。
- `regulatory_sources/sources.json`: 机器可读的法规 URL 配置。
- `scripts/check_sources.py`: 法规页面抓取、正文归一化、快照保存和更新比对脚本。
- `sources/brazil/`: 2026-06-23 生成的第一版 baseline 快照和检查日志。

## 运行方式

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

## 当前状态

已监控 10 个巴西法规来源，重复运行验证结果为 `no-update`。`Act No. 9,526/2021` 尚未确认到官方 URL，暂未加入监控队列。

下一步可以把脚本接入每月定时任务，并按同样结构补充泰国、蒙古等国家的法规来源。
