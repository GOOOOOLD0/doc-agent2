---
name: satellite-landing-rights
description: 检索、分析和生成国家卫星落地许可知识，支持独立 CLI Agent。
status: active
---

# Satellite Landing Rights Analysis

## 使用场景

当用户询问以下内容时使用本 Skill：

- 某国卫星落地许可或 landing rights；
- 外国卫星市场准入；
- 卫星、电信或频率许可；
- 地球站、网关、用户终端和设备认证；
- 根据官方来源生成国家 `00-10` 案例；
- 比较不同国家和巴西的监管流程。

## 独立 Agent 入口

在项目根目录运行：

```bash
python3 -m landing_rights_agent doctor
python3 -m landing_rights_agent answer --country mongolia --question "蒙古卫星宽带落地需要哪些许可？"
python3 -m landing_rights_agent research --country indonesia --output indonesia-research.md
python3 -m landing_rights_agent build-country --country mongolia
```

`build-country` 默认只写入 `.agent_runs/` 预览目录。只有用户明确要求更新 Wiki 时，才使用 `--apply`。

## 强制读取顺序

1. 根目录 `AGENTS.md`；
2. `wiki/concepts/landing_rights/common/`；
3. 目标国家 `wiki/raw/landing_rights/<country>/source_inventory.md`；
4. 目标国家 `wiki/raw/landing_rights/<country>/source_notes/`；
5. 目标国家已有 cases；
6. 巴西案例仅作为结构和问题清单参考。

## 证据和写入边界

1. 目标国家官方来源才可支撑关键法律结论；
2. 必须区分已确认信息、分析推断和待确认事项；
3. 来源不足时不得生成正式 cases 空骨架；
4. `research` 结果只是第一阶段研究报告，不自动等同于 source note；
5. `build-country` 至少需要 source inventory 和三个 source notes；
6. 自动生成文件必须保持 `review_status: draft`；
7. 费用、期限、法规版本和主体资格必须标记最新复核要求；
8. 不得自动提交 GitHub、发送外部信息或覆盖人工确认状态。

## 输出

- 问答结果：终端或 `--output` 指定文件；
- 研究报告：终端或 `--output` 指定文件；
- cases 预览：`.agent_runs/<timestamp>/<country>/cases/`；
- 正式 cases：仅在 `--apply` 时写入 `wiki/concepts/landing_rights/cases/<country>/`。
