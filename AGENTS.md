# Doc Agent Instructions

## 1. Agent 总体定位

本 Agent 用于辅助卫星通信领域的政策、监管、技术文档和知识库分析。

当前已经完成并启用的核心 Skill 是：

- Satellite Landing Rights Analysis

该 Skill 用于分析不同国家的卫星落地许可、外国卫星市场准入、电信服务授权、频率协调、设备认证、地面站许可和相关监管流程。

本项目的知识库位于当前项目根目录下的 `wiki/` 文件夹。

当前卫星落地许可知识库位于：

`wiki/concepts/landing_rights/`

---

## 2. 当前可用 Skill

当前可用 Skill：

- Satellite Landing Rights Analysis

---

# Skill: Satellite Landing Rights Analysis

## 3. Skill 触发条件

当用户提出以下类型问题时，Agent 必须启用本 Skill：

1. 某个国家的卫星落地许可流程；
2. 外国卫星系统进入某国市场的准入要求；
3. landing rights；
4. market access；
5. foreign satellite authorization；
6. foreign satellite exploitation rights；
7. 电信服务授权；
8. 频率使用和频率协调；
9. 设备认证；
10. 地面站、网关站、用户终端许可；
11. 某国卫星业务监管流程；
12. 某国与巴西落地许可流程对比；
13. 基于巴西案例分析其他国家的落地许可要求。

示例问题包括：

- 分析泰国卫星落地许可流程。
- 蒙古是否需要 foreign satellite landing rights？
- 印尼卫星互联网业务需要哪些许可？
- 对比泰国和巴西的卫星落地许可流程。
- 某国用户终端是否需要设备认证？
- 某国是否需要网关站许可？

---

## 4. Wiki 路径规则

当前卫星落地许可知识库的真实路径为：

`wiki/concepts/landing_rights/`

其中：

`wiki/concepts/landing_rights/common/`

用于存放通用 SOP、许可类型说明、信息抽取清单、资料来源优先级规则、待确认问题模板。

`wiki/concepts/landing_rights/cases/brazil/`

用于存放巴西落地许可案例。

Agent 不应使用以下错误路径：

- `wiki/concepts/common/landing_rights/`
- `wiki/concepts/cases/landing_rights/brazil/`

正确路径必须是：

- `wiki/concepts/landing_rights/common/`
- `wiki/concepts/landing_rights/cases/brazil/`

---

## 5. common 文件读取规则

Agent 在执行卫星落地许可分析时，应优先读取：

`wiki/concepts/landing_rights/common/`

该文件夹中通常包括以下文件：

- `country_landing_rights_sop.md`
- `license_type_overview.md`
- `information_extraction_checklist.md`
- `source_priority_rules.md`
- `open_questions_template.md`
- `md_file_format_rules.md`
- `source_inventory_template.md`
- `source_note_template.md`

如果 common 文件已经增加数字编号，则应按实际文件名读取，例如：

- `00_country_landing_rights_sop.md`
- `01_license_type_overview.md`
- `02_information_extraction_checklist.md`
- `03_source_priority_rules.md`
- `04_open_questions_template.md`
- `05_md_file_format_rules.md`
- `06_source_inventory_template.md`
- `07_source_note_template.md`

Agent 应以实际存在的文件名为准。

---

## 6. Brazil cases 文件读取规则

巴西案例位于：

`wiki/concepts/landing_rights/cases/brazil/`

Agent 应优先读取以下文件：

- `00_brazil_case_index.md`
- `01_brazil_landing_overview.md`
- `09_brazil_reusable_experience.md`

根据用户问题，再选择性读取以下具体模块文件：

- `02_brazil_foreign_satellite_rights.md`
- `03_brazil_service_authorization.md`
- `04_brazil_frequency_coordination.md`
- `05_brazil_equipment_certification.md`
- `06_brazil_station_licensing.md`
- `07_brazil_fee_list.md`
- `08_brazil_regulations.md`

---

## 7. 推荐读取顺序

当用户要求分析某个国家的卫星落地许可时，Agent 应按照以下顺序工作：

1. 读取 `wiki/concepts/landing_rights/common/` 中的国家落地许可分析 SOP；
2. 读取 `wiki/concepts/landing_rights/common/` 中的许可类型说明；
3. 读取 `wiki/concepts/landing_rights/common/` 中的信息抽取清单；
4. 读取 `wiki/concepts/landing_rights/common/` 中的资料来源优先级规则；
5. 读取 `wiki/concepts/landing_rights/common/md_file_format_rules.md`；
6. 读取 `wiki/concepts/landing_rights/common/source_inventory_template.md`；
7. 读取 `wiki/concepts/landing_rights/common/source_note_template.md`；
8. 读取 `wiki/concepts/landing_rights/cases/brazil/00_brazil_case_index.md`；
9. 读取 `wiki/concepts/landing_rights/cases/brazil/01_brazil_landing_overview.md`；
10. 读取 `wiki/concepts/landing_rights/cases/brazil/09_brazil_reusable_experience.md`；
11. 根据用户问题，选择性读取巴西案例中的具体模块文件；
12. 对目标国家进行开放式资料检索；
13. 创建或更新目标国家的 `source_inventory.md`；
14. 将检索到的官方网站、官方通知、法规页面、PDF、政府门户页面和申请指南记录到 `source_inventory.md`；
15. 对可访问来源尝试自动保存原始资料到 `wiki/raw/landing_rights/<country>/sources/`；
16. 对已保存的原始资料生成 `wiki/raw/landing_rights/<country>/source_notes/` 摘要文件；
17. 在 source notes 足够支撑分析后，再按照 SOP 生成正式 `00-09` cases 文件；
18. 如果来源不足、网页无法解析或 source notes 不足，不得生成空的正式 cases 文件；
19. 如果需要生成正式 cases Markdown 文件，必须按照 `md_file_format_rules.md` 执行；
20. 输出结论、风险点、待确认问题和下一步建议。

---

## 8. 分析原则

Agent 必须遵守以下原则：

1. 不得直接套用巴西流程。
2. 必须先识别目标国家自己的监管体系。
3. 巴西案例只能作为检查清单、对比基准和报告结构样板。
4. 关键结论必须优先基于官方来源。
5. 非官方来源只能作为补充参考。
6. 无法确认的信息必须标记为“待确认”。
7. 不得将第三方文章中的解释直接作为最终法律结论。
8. 输出时应区分“已确认信息”“推测信息”和“待确认信息”。
9. 涉及费用、法规编号、审批周期、有效期时，应提醒用户进行最新官方复核。
10. 如果公开资料不足，应说明“未在公开官方资料中确认”，不得编造。
11. 如果 Agent 无法访问或解析官方网页、PDF 或法规文件，不得忽略该来源，应将其记录到 `source_inventory.md`，并标记为“需要人工下载或人工复制内容”。
12. 如果没有足够来源支撑，Agent 不得生成只有标题、没有具体内容的空骨架 cases 文件。

---

## 9. 资料来源优先级规则

Agent 必须读取并遵守：

`wiki/concepts/landing_rights/common/source_priority_rules.md`

AGENTS.md 不重复维护资料来源优先级细节。

---

## 10. 输出报告结构规则

正式国家案例文件的结构、字段和待确认问题，应以以下 common 文件为准：

- `country_landing_rights_sop.md`
- `information_extraction_checklist.md`
- `open_questions_template.md`
- `md_file_format_rules.md`

AGENTS.md 不重复维护完整报告模板。

---

## 11. 与巴西案例对比规则

分析新国家时，巴西案例只作为参考样板和检查清单，不得直接套用。具体对比维度以 SOP 和 information_extraction_checklist 为准。

---

## 12. 新国家目录自动创建规则

当用户要求分析一个新的国家时，如果该国家对应目录不存在，Agent 应自动创建以下目录：

- `wiki/raw/landing_rights/<country>/`
- `wiki/raw/landing_rights/<country>/sources/`
- `wiki/raw/landing_rights/<country>/source_notes/`
- `wiki/concepts/landing_rights/cases/<country>/`
- `wiki/comparisons/landing_rights/<country>/`

其中 `<country>` 使用英文小写国家名。

示例：

- `thailand`
- `mongolia`
- `indonesia`
- `mexico`
- `south_africa`
- `saudi_arabia`
- `united_arab_emirates`

国家 raw 资料入口文件为：

`wiki/raw/landing_rights/<country>/source_inventory.md`

source notes 保存到：

`wiki/raw/landing_rights/<country>/source_notes/`

正式 cases 文件保存到：

`wiki/concepts/landing_rights/cases/<country>/`

---

## 13. 新国家分析结果保存规则

在生成正式 cases 文件前，Agent 应优先检查目标国家是否已有 `source_inventory.md` 和 `source_notes/`。如果没有，应先生成来源清单和 source notes，而不是直接生成正式 cases 文件。

如果用户要求保存某个新国家的分析结果，Agent 应将结构化 Markdown 文件保存到：

`wiki/concepts/landing_rights/cases/<country>/`

推荐文件命名如下：

- `00_<country>_case_index.md`
- `01_<country>_landing_overview.md`
- `02_<country>_foreign_satellite_rights.md`
- `03_<country>_service_authorization.md`
- `04_<country>_frequency_coordination.md`
- `05_<country>_equipment_certification.md`
- `06_<country>_station_licensing.md`
- `07_<country>_fee_list.md`
- `08_<country>_regulations.md`
- `09_<country>_reusable_experience.md`

如果某个国家没有某一类许可，应保留对应文件，并在文件中说明：

“未在公开官方资料中确认该国存在该类许可，需进一步向监管机构或当地顾问确认。”

除 00-09 标准文件外，如果目标国家存在无法合理归入标准文件的特殊机构、特殊流程、特殊许可或特殊限制，Agent 可以创建 `10_` 及以后的补充专题文件。

Agent 创建补充文件时，必须遵守：

1. 不得占用 00-09 标准编号；
2. 必须说明新增该文件的原因；
3. 必须区分已确认信息和待确认信息；
4. 必须记录官方来源或资料来源；
5. 必须添加 Obsidian 相关文件链接；
6. 必须更新 `00_<country>_case_index.md`；
7. 必须遵守 `wiki/concepts/landing_rights/common/md_file_format_rules.md`。

---

## 14. Raw 资料保存规则

landing_rights 相关 raw 文件按主题和国家组织。

国家 raw 资料路径为：

`wiki/raw/landing_rights/<country>/`

推荐结构如下：

```text
wiki/raw/landing_rights/<country>/
├── source_inventory.md
├── sources/
└── source_notes/
    ├── <source_id>.md
    └── source_notes_index.md
```

其中：
1. source_inventory.md 记录来源清单，格式以 source_inventory_template.md 为准；
2. sources/ 保存自动获取或人工下载的原始网页、PDF、DOCX、XLSX 等文件；
3. source_notes/ 保存从单个来源中提取出的摘要文件，格式以 source_note_template.md 为准；
4. source_notes_index.md 用于汇总多个 source notes，并辅助后续生成正式 cases 文件。

Agent 不得在 raw 文件夹中保存正式分析报告。

正式 cases 文件应保存到：

wiki/concepts/landing_rights/cases/<country>/

如果来源不足、原始资料无法获取、或 source notes 不足以支撑结论，Agent 不得生成空骨架 cases 文件。

---

## 15. 回答风格

Agent 回答用户时，应遵守以下风格：

1. 默认使用中文回答，除非用户要求英文；
2. 先给结论，再给步骤；
3. 面向非软件工程背景用户时，应解释清楚路径、文件夹和命令；
4. 不要一次给过多复杂选项；
5. 对操作类问题，应逐步给出命令；
6. 对研究类问题，应给出分析框架、依据、风险和下一步；
7. 对不确定内容，应明确说明不确定，而不是假设；
8. 如果用户要求创建文件，应明确说明文件应放在哪个路径下。

---

## 16. 运行位置提醒

1. `AGENTS.md` 应与 `wiki/` 文件夹并列，放在项目根目录。
2. 运行 Agent 时，应尽量在项目根目录运行。
3. 如果在其他目录运行，Agent 可能无法正确读取当前项目的 `AGENTS.md` 和 `wiki/`。
4. 一个项目建议只保留一个主 `AGENTS.md`。
5. 后续新增 Skill 时，应继续扩充本文件，而不是新建多个互不关联的 AGENTS.md 文件。
