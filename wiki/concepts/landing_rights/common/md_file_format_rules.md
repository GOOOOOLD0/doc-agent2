---
scope: common
topic: landing_rights
doc_type: format_rules
language: zh-CN
review_status: draft
--------------------

# 卫星落地许可 Markdown 文件格式规则

## 1. 文件用途

本文件规定 Agent 在生成卫星落地许可相关 Markdown 文件时应遵守的统一格式。

本文件用于约束：

1. 文件命名；
2. 文件编号；
3. YAML 元数据；
4. 正文结构；
5. 已确认信息和待确认信息的写法；
6. 来源记录；
7. Obsidian 链接；
8. 新国家特殊流程的扩展方式。

本文件只规定 Markdown 结构化知识文件的格式，暂不规定原始网页、PDF、法规文件的下载和保存流程。

Agent 在生成新国家案例文件前，必须先读取本文件。

---

## 2. 文件类型和保存路径

卫星落地许可相关 Markdown 文件主要分为三类。

### 2.1 common 文件

用于保存通用规则、模板、检查清单和方法论。

路径：

`wiki/concepts/landing_rights/common/`

示例：

* `country_landing_rights_sop.md`
* `license_type_overview.md`
* `information_extraction_checklist.md`
* `source_priority_rules.md`
* `open_questions_template.md`
* `md_file_format_rules.md`

### 2.2 cases 文件

用于保存某个国家的结构化案例分析。

路径：

`wiki/concepts/landing_rights/cases/<country>/`

示例：

* `wiki/concepts/landing_rights/cases/brazil/`
* `wiki/concepts/landing_rights/cases/thailand/`

### 2.3 comparisons 文件

用于保存不同国家之间的系统对比分析。

路径：

`wiki/comparisons/landing_rights/<country>/`

示例：

* `wiki/comparisons/landing_rights/thailand/thailand_vs_brazil.md`

---

## 3. 国家案例文件命名规则

国家案例文件统一使用英文小写文件名。

格式：

`<序号>_<country>_<topic>.md`

规则：

1. `<序号>` 使用两位数字；
2. `<country>` 使用英文小写国家名；
3. `<topic>` 使用英文小写和下划线；
4. 文件名不使用中文；
5. 文件名不使用空格；
6. 不得占用已有标准编号。

---

## 4. 标准 00-09 文件结构

每个国家案例应尽量保留以下标准文件。

| 编号 | 文件名                                        | 用途                         |
| -- | ------------------------------------------ | -------------------------- |
| 00 | `00_<country>_case_index.md`               | 国家案例入口和文件索引                |
| 01 | `01_<country>_landing_overview.md`         | 国家落地许可整体流程总览               |
| 02 | `02_<country>_foreign_satellite_rights.md` | 外国卫星落地权、市场准入或外国卫星容量使用许可    |
| 03 | `03_<country>_service_authorization.md`    | 电信业务许可或服务授权                |
| 04 | `04_<country>_frequency_coordination.md`   | 频率使用、频率协调、ITU filing 或干扰协调 |
| 05 | `05_<country>_equipment_certification.md`  | 用户终端、网关设备、网络设备等认证要求        |
| 06 | `06_<country>_station_licensing.md`        | 地面站、网关站、空间站、TT&C 站或无线电台站许可 |
| 07 | `07_<country>_fee_list.md`                 | 申请费、频率费、站点费、年费、续期费等        |
| 08 | `08_<country>_regulations.md`              | 法律、法规、通知、指南和官方依据           |
| 09 | `09_<country>_reusable_experience.md`      | 可复用经验和后续分析启发               |

注意：

1. `02_` 固定用于 foreign satellite rights，不得用于 regulators。
2. `08_` 固定用于 regulations，不得用于 regulators。
3. 监管机构文件应作为补充文件，从 `10_` 开始编号。

推荐命名：

`10_<country>_regulatory_authorities.md`

---

## 5. 国家特殊流程扩展规则

00-09 是基础结构，不代表所有国家都必须与巴西流程完全相同。

Agent 必须识别目标国家自己的真实监管体系，不得机械套用巴西流程。

如果发现目标国家存在巴西案例中没有的特殊许可、特殊机构、特殊流程或特殊限制，应按以下规则处理：

1. 优先判断是否可以写入 00-09 标准文件；
2. 如果可以归入标准文件，不要新建文件；
3. 如果无法合理归入标准文件，可以创建 `10_` 及以后的补充专题文件；
4. 新增补充文件时，必须说明新增原因、确认状态和相关来源；
5. 新增补充文件后，应更新 `00_<country>_case_index.md`。

补充文件示例：

* `10_thailand_regulatory_authorities.md`
* `11_thailand_local_entity_requirement.md`
* `12_thailand_space_policy_institutions.md`

---

## 6. YAML front matter 规则

每个 Markdown 文件开头必须包含 YAML front matter。

cases 文件推荐格式：

---

country: Thailand
topic: regulatory_authorities
case_type: structured_case
source_document: public_sources
language: zh-CN
review_status: draft
--------------------

字段说明：

| 字段              | 含义            | 示例                     |
| --------------- | ------------- | ---------------------- |
| country         | 国家名称，英文首字母大写  | Thailand               |
| topic           | 文件主题，英文小写和下划线 | regulatory_authorities |
| case_type       | 文件类型          | structured_case        |
| source_document | 资料来源说明        | public_sources         |
| language        | 正文语言          | zh-CN                  |
| review_status   | 审核状态          | draft                  |

`review_status` 规则：

1. Agent 自动生成的新文件应写 `draft`；
2. 如果需要强调机器生成，可写 `machine_generated`；
3. 只有用户人工确认后，才能写 `human_reviewed`；
4. 内容可能过期或需要复核时，写 `needs_update`。

Agent 不得在自动生成的新国家文件中直接写：

`review_status: human_reviewed`

---

## 7. 标题和正文结构规则

每个 Markdown 文件必须有一个中文一级标题。

格式：

`# <中文标题>`

正文不得直接从 bullet list 开始。

### 7.1 cases 文件推荐结构

每个新生成的 cases 文件应尽量包含以下部分：

1. 文件用途；
2. 结论摘要；
3. 已确认信息；
4. 相关信息或待确认信息；
5. 与巴西案例的关系；
6. 官方来源或资料来源；
7. 待确认问题；
8. 下一步工作；
9. 相关文件。

不同主题可以适当调整章节名称，但不得缺少以下核心内容：

1. YAML front matter；
2. 中文一级标题；
3. 文件用途；
4. 结论摘要；
5. 已确认信息；
6. 待确认信息或待确认问题；
7. 来源记录；
8. Obsidian 相关文件链接。

---

## 8. 已确认信息和待确认信息规则

Agent 必须区分三类信息：

1. 已确认信息；
2. 相关但未确认信息；
3. 待确认问题。

### 8.1 已确认信息

已确认信息应优先来自：

1. 官方监管机构网站；
2. 官方法律法规；
3. 官方通知、指南、申请表或公告；
4. 政府门户网站；
5. 正式监管文件。

### 8.2 相关但未确认信息

如果某机构、许可或流程可能相关，但尚未确认其是否直接参与审批，应明确写为“需进一步确认”。

推荐写法：

“该机构可能与空间政策或产业协调有关，但其是否直接参与通信卫星落地许可审批，仍需进一步确认。”

### 8.3 待确认问题

待确认内容应以问题形式列出。

示例：

1. 申请主体是否必须为本地公司？
2. 外国卫星运营商是否可以直接申请？
3. 是否需要提交 ITU filing？
4. 是否需要单独办理网关站许可？
5. 用户终端是否需要设备认证？

---

## 9. 不确定信息写法

对于尚未确认的信息，Agent 应使用谨慎表达。

推荐表达：

* “需进一步确认”；
* “未在公开官方资料中确认”；
* “当前只能作为相关机构保留”；
* “不能直接认定为审批机构”；
* “目前可初步判断为相关要求，但仍需官方复核”。

不推荐表达：

* “一定需要”；
* “必然由该机构负责”；
* “已确认要求”；
* “完全等同于巴西流程”；
* “该国流程与巴西相同”。

除非有明确官方来源支持，否则不得使用绝对化表述。

---

## 10. 来源记录规则

每个 cases 文件必须包含“官方来源”或“资料来源”部分。

官方来源示例：

## 官方来源

1. NBTC 官方主页：`https://www.nbtc.go.th`
2. NBTC 官方通知：`https://www.nbtc.go.th/...`

如果使用律所、咨询机构、新闻、博客或行业报告，应单独标注为“非官方补充来源”。

非官方来源写法：

## 非官方补充来源

1. 某律所文章：`URL`

说明：

该来源为非官方来源，仅作为补充参考。关键结论仍需以官方文件为准。

来源使用要求：

1. 关键结论优先基于官方来源；
2. 非官方来源只能作为补充；
3. 如果官方来源无法确认，应标记为待确认；
4. 不得将第三方解释直接作为最终法律结论；
5. 涉及费用、有效期、审批周期、法规编号时，应提醒进行最新官方复核。

---

## 11. 与巴西案例的关系

巴西案例是参考样板，不是目标国家的法律依据。

每个新国家 cases 文件可以简要说明其与巴西案例的关系，但不要求逐条说明“与巴西一致”或“与巴西不一致”。

推荐写法：

1. 说明该文件对应巴西案例中的哪个模块；
2. 如果目标国家制度与巴西明显不同，应简要指出；
3. 如果无法确认是否一致，不得强行判断，应写为“需进一步确认”；
4. 详细国家对比应写入 comparisons 文件，而不是在每个 cases 文件中重复展开。

示例：

“该部分对应巴西案例中的 `02_brazil_foreign_satellite_rights.md`。但泰国制度不应直接等同于巴西的 Right to Exploit Foreign Satellite，仍需根据 NBTC 官方文件确认其具体许可名称、申请主体和审批流程。”

---

## 12. Obsidian 链接规则

每个 Markdown 文件末尾必须包含“相关文件”部分。

Obsidian 链接格式：

`[[文件名|显示名称]]`

通常不写 `.md` 后缀。

### 12.1 新国家文件至少链接

每个新国家 cases 文件至少应链接：

1. 本国 case index；
2. 本国 landing overview；
3. 巴西案例索引；
4. 巴西案例可复用经验；
5. common SOP；
6. source priority rules；
7. information extraction checklist。

示例：

## 相关文件

* [[00_thailand_case_index|泰国案例索引]]
* [[01_thailand_landing_overview|泰国落地许可总览]]
* [[00_brazil_case_index|巴西案例索引]]
* [[09_brazil_reusable_experience|巴西案例可复用经验]]
* [[country_landing_rights_sop|国家落地许可分析 SOP]]
* [[source_priority_rules|落地许可资料来源优先级规则]]
* [[information_extraction_checklist|国家落地许可信息抽取清单]]

如果 common 文件带有数字编号，应使用实际文件名。

---

## 13. 表格使用规则

当内容涉及多个机构、多个许可、多个费用、多个法规或多个对比维度时，Agent 应优先使用 Markdown 表格。

示例：

| 机构     | 当前判断     | 与落地许可的关系                    | 确认状态   |
| ------ | -------- | --------------------------- | ------ |
| NBTC   | 核心监管机构   | 可能负责外国卫星容量使用、电信业务许可、频率和设备认证 | 已初步确认  |
| MDES   | 政策相关机构   | 可能涉及数字经济和通信政策               | 需进一步确认 |
| GISTDA | 空间事务相关机构 | 可能涉及空间政策或空间活动协调             | 需进一步确认 |

---

## 14. case index 更新规则

如果 Agent 为某个国家新增文件，必须检查是否需要更新该国家的 case index 文件。

case index 文件路径：

`wiki/concepts/landing_rights/cases/<country>/00_<country>_case_index.md`

如果 case index 不存在，Agent 应创建该文件。

case index 至少应包括：

1. 案例名称；
2. 案例用途；
3. 文件结构；
4. 已完成文件；
5. 待补充文件；
6. 相关 common 文件链接。

如果新增文件为：

`10_thailand_regulatory_authorities.md`

则应在 `00_thailand_case_index.md` 中加入：

* [[10_thailand_regulatory_authorities|泰国监管机构]]

---

## 15. 文件主题映射规则

Agent 可参考以下规则选择文件位置。

| 发现的信息类型               | 推荐写入文件                                      |
| --------------------- | ------------------------------------------- |
| 整体许可流程                | `01_<country>_landing_overview.md`          |
| 监管机构                  | `10_<country>_regulatory_authorities.md`    |
| 外国卫星落地权、市场准入、外国卫星容量使用 | `02_<country>_foreign_satellite_rights.md`  |
| 电信业务许可、服务授权           | `03_<country>_service_authorization.md`     |
| 频率使用、ITU filing、频率协调  | `04_<country>_frequency_coordination.md`    |
| 用户终端、网关设备认证           | `05_<country>_equipment_certification.md`   |
| 地面站、网关站、空间站、TT&C 站许可  | `06_<country>_station_licensing.md`         |
| 费用、年费、续期费             | `07_<country>_fee_list.md`                  |
| 法律、法规、通知、指南、官方依据      | `08_<country>_regulations.md`               |
| 可复用经验                 | `09_<country>_reusable_experience.md`       |
| 本地公司、本地代表、本地运营商要求     | `11_<country>_local_entity_requirement.md`  |
| 空间政策机构或空间事务协调机构       | `12_<country>_space_policy_institutions.md` |
| 其他无法归入标准文件的重要特殊流程     | `13_` 及以后补充文件                               |

---

## 16. 文件生成检查清单

Agent 生成新文件前后，应检查以下事项：

1. 是否读取了 `AGENT.md`；
2. 是否读取了本格式规则文件；
3. 是否读取了 common SOP、source priority rules 和 information extraction checklist；
4. 是否读取了巴西案例索引；
5. 目标文件名是否与 00-09 标准编号冲突；
6. 目标文件是否已经存在；
7. 是否需要使用 `10_` 及以后的补充编号；
8. 是否包含 YAML front matter；
9. `review_status` 是否为 `draft` 或 `machine_generated`；
10. 是否有中文一级标题；
11. 是否区分已确认信息和待确认信息；
12. 是否记录官方来源或资料来源；
13. 是否包含待确认问题；
14. 是否包含 Obsidian 相关文件链接；
15. 是否需要更新 `00_<country>_case_index.md`。

如果目标文件已经存在，Agent 不得直接覆盖，除非用户明确要求。

---

## 17. 禁止事项

Agent 不得执行以下行为：

1. 不得只生成简单 bullet notes；
2. 不得使用错误编号；
3. 不得将监管机构文件命名为 `02_<country>_regulators.md`；
4. 不得将法规依据文件和监管机构文件混淆；
5. 不得把巴西流程直接套用到目标国家；
6. 不得把未确认信息写成最终结论；
7. 不得把非官方来源作为最终法律依据；
8. 不得自动写 `review_status: human_reviewed`；
9. 不得忽略目标国家特有流程；
10. 不得省略 Obsidian 相关文件链接；
11. 不得在用户未要求覆盖时覆盖已有文件。

---

## 18. 最终目标

本格式规则的目标不是让所有国家案例内容完全相同，而是让所有国家案例具有统一的知识库格式。

Agent 应做到：

1. 格式统一；
2. 编号清楚；
3. 来源清楚；
4. 已确认和待确认分离；
5. 巴西案例仅作为参考；
6. 目标国家特殊流程不被忽略；
7. Obsidian 链接完整；
8. 后续人工复核方便；
9. LLM Wiki 可以长期维护和扩展。
