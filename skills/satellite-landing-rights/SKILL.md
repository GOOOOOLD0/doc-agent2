---
name: satellite-landing-rights
description: >
  当用户要求查询、研究、核实、比较、生成或更新某个国家的卫星落地许可、
  外国卫星市场准入、服务授权、频谱、设备、地面站、网关、用户终端、
  费用或监管程序时，使用本 Skill。
status: active
---

# Satellite Landing Rights

## 1. 目标与职责

基于可追溯的官方资料，完成国家卫星落地许可的问答、研究、更新、建档和比较。

Hermes 是唯一顶层 Agent。本 Skill 负责流程编排和阶段检查；通用模板负责格式；仓库工具负责抓取、解析和校验。不得调用其他独立 Agent 或二次 LLM。

## 2. 项目根目录与固定路径

执行任务前：

1. 运行 `git rev-parse --show-toplevel`；
2. 验证根目录中存在 `AGENT.md`、`wiki/` 和 `skills/`；
3. 以下路径均相对于项目根目录解析。

固定路径：

- 通用规则：`wiki/concepts/landing_rights/common/`
- 国家原始资料：`wiki/raw/landing_rights/<country>/`
- 国家案例：`wiki/concepts/landing_rights/cases/<country>/`
- 国家比较：`wiki/comparisons/landing_rights/<country>/`

`<country>` 使用英文小写和下划线，例如 `mongolia`、`south_africa`。

不得将国家资料或案例写入：

- `~/.hermes/skills/`
- `skills/satellite-landing-rights/`
- `wiki/concepts/landing_rights/common/`

## 3. 任务模式

根据用户意图选择：

- **answer**：读取已有资料回答，不写文件；
- **research**：搜索、登记、抓取并生成 Source Notes；
- **build**：根据已有 Source Notes 生成 Evidence Matrix 和国家案例；
- **update**：更新新增或变化的来源、Evidence Matrix 和受影响案例；
- **compare**：比较多个国家；
- **full**：依次执行 research、build 和 validate。

意图解析：

- “查询、解释、是否需要”默认 `answer`；
- “研究、收集资料、建立台账”默认 `research`；
- “生成案例、生成00-09”默认 `build`；
- “更新、重新核实”默认 `update`；
- “完整研究并建立案例”默认 `full`；
- 显式加载本 Skill 后仅提供国家名时，默认 `full`。

用户只要求回答时，不得自动进入写入模式。

## 4. 通用规则

执行写入任务前，根据阶段读取：

- `case_spec.md`：`00-09` 案例的唯一结构与质量规范；
- `evidence_matrix_template.md`：Evidence Matrix 的唯一格式；
- `source_priority_rules.md`：来源优先级和使用规则；
- `source_inventory_template.md`：来源台账格式；
- `source_note_template.md`：Source Note 格式。

完整路径均位于：

`wiki/concepts/landing_rights/common/`

必要文件不存在或无法读取时，停止相应阶段并报告，不得自行设计替代格式。

## 5. 标准流程

### 5.1 检查现有资料

对目标国家依次检查：

1. `source_inventory.md`；
2. `sources/`；
3. `source_notes/`；
4. `source_notes/source_notes_index.md`；
5. `evidence_matrix.md`；
6. 已有 `cases/<country>/00-09` 及其审核状态。

若 `source_notes_index.md` 不存在，必须枚举并读取 `source_notes/` 中实际存在的 `.md` 文件。

在完成目录检查前，不得声称 Source Notes 不存在，也不得要求用户重新提供路径。

### 5.2 Research：搜索、登记、抓取和 Source Notes

现有证据不足或模式为 `research`、`update`、`full` 时：

1. 优先检索目标国家法律法规、监管机构、政府门户、正式决议、申请指南、收费规则和官方附件；
2. 将有效来源登记到 `source_inventory.md`；
3. 将可获取的网页、PDF、DOCX、XLSX 等保存到 `sources/`；
4. 每个来源生成一份独立 Source Note；
5. 更新 `source_notes_index.md`；
6. 无法访问的来源仍登记台账，并标记需人工获取。

不得使用新闻、咨询报告或其他国家案例单独支撑关键法律结论。

### 5.3 Build 第一步：生成 Evidence Matrix

执行 `build`、`update` 或 `full` 时，必须先生成或更新：

`wiki/raw/landing_rights/<country>/evidence_matrix.md`

严格使用：

`wiki/concepts/landing_rights/common/evidence_matrix_template.md`

输入仅包括目标国家的 Source Inventory 和 Source Notes。

强制要求：

1. 必须逐份读取实际存在的 Source Notes；
2. 每个重要结论使用独立的 `### E-XXX｜主题` 小节；
3. 一个证据项只表达一个主要结论；
4. 同一 Source Note 可以支持多个证据项；
5. 不得使用宽表格保存全部证据项；
6. 不得按“一份 Source Note 一行”组织；
7. 不得重复搬运 Source Inventory 的访问状态、发布者等台账字段；
8. 核心法律和规则应尽量记录具体条款、章节或页面位置；
9. 未使用的 Source Notes 必须说明原因；
10. 不得保留模板占位符。

生成后必须确认：

- 存在 `### E-001｜`；
- 每个证据项包含模板规定的全部字段；
- 不存在以 `| source_id |` 开头的宽表格；
- 阶段时限、收费规则、法规正文和附件的边界得到保留。

Evidence Matrix 未通过检查时，必须自动修正；不得进入案例生成阶段。

### 5.4 Build 第二步：生成 `01-09`

Evidence Matrix 通过后，严格按照 `case_spec.md` 逐个生成：

`01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09`

输出目录固定为：

`wiki/concepts/landing_rights/cases/<country>/`

生成单个文件时：

1. 读取 Evidence Matrix 中所有映射到该文件的证据项；
2. 读取这些证据项引用的相关 Source Notes；
3. 每个证据项必须被正文采用，或明确说明未采用原因；
4. 保留具体条款、支持范围、禁止扩大解释的范围和版本风险；
5. 证据不足时写“未在现有官方资料中确认”；
6. 使用 `review_status: draft`；
7. 不生成只有标题的空文件；
8. 不读取已有目标国家 cases 作为新的事实来源。

不得只根据 Evidence Matrix 的“资料概览”或“覆盖状态”生成案例。

### 5.5 Build 第三步：生成 `00`

`01-09` 完成并通过检查后，最后生成或更新：

`00_<country>_case_index.md`

索引必须与实际存在的文件、状态和链接一致。

### 5.6 Compare

比较多个国家时：

- 只使用各国已确认的资料；
- 使用相同维度；
- 缺失项标记为“未确认”；
- 不得用一个国家的制度填补另一个国家的证据缺口。

## 6. 证据规则

1. 关键法律和许可结论优先使用目标国家官方来源；
2. 明确区分已确认信息、分析推断和待确认事项；
3. 不得补充来源中没有的许可证、材料、费用、期限或主体资格；
4. 多个来源冲突时保留差异，不得静默选择；
5. 一般程序或阶段时限不得写成完整项目周期；
6. 收费原则或公式不得写成具体项目金额；
7. 法规主页、法规附件、申请页面和下载表格应区分证据作用；
8. 费用、期限、版本、翻译和主体资格应记录复核日期及适用边界；
9. 巴西等已有案例只能用于结构参考和比较，不能作为目标国家事实依据。

## 7. 写入前检查

写入前必须报告：

- 项目根目录；
- 任务模式；
- 目标国家及 `<country>`；
- 输入台账和 Source Notes 目录；
- Evidence Matrix 输出路径；
- 国家案例输出目录；
- 计划创建或更新的文件。

若案例输出目录不是：

`wiki/concepts/landing_rights/cases/<country>/`

必须停止，不得写入。

## 8. 写入后校验

至少检查：

- 文件路径和文件名正确；
- frontmatter、一级标题和 `review_status` 合规；
- Source Note 和内部链接真实存在；
- Evidence Matrix 不使用宽表格；
- 案例逐项消费了对应 Evidence 项；
- 条款归属、适用范围、版本和翻译风险未被错误修改；
- 无空文件、重复文件和模板占位符；
- `00` 索引与实际文件一致。

无法完成校验时，不得宣称任务已完成。

## 9. 安全与恢复

- `answer` 不修改 Wiki；
- `research` 只写入目标国家 `raw/` 目录；
- `build` 只写入 Evidence Matrix 和目标国家 `cases/` 目录；
- 不覆盖已人工确认内容，除非用户明确要求；
- 不自动执行 Git commit、push、删除文件或发送外部信息；
- 中途失败时保留已完成文件，并从未完成阶段继续，不进行破坏性重跑。

## 10. 输出要求

默认使用中文。

回答任务优先给出：

1. 直接结论；
2. 监管机构和主要许可；
3. 流程、条件及适用边界；
4. 来源依据；
5. 风险和待确认事项。

写入任务完成后说明：

- 执行的模式和阶段；
- 创建或更新的文件；
- 实际使用的主要来源；
- 校验结果；
- 仍需人工复核的事项。
