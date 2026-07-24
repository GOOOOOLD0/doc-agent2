---

scope: common
topic: landing_rights
doc_type: source_note_template
language: zh-CN
review_status: draft
---

# Source Note 摘要模板

## 1. 文件用途

Source note 用于记录单个网页、PDF、法规、通知、指南或附件的主要原始信息。

Agent 生成 source note 时，只需要忠实提取来源中的主要内容。

---

## 2. 保存位置


每个国家生成的 source note 保存到：

`wiki/raw/landing_rights/<country>/source_notes/`

单个 source note 文件命名为：

`<source_id>.md`

示例：

`wiki/raw/landing_rights/mongolia/source_notes/mn-crc-satellite-network-license.md`

对应的原始来源文件通常保存到：

`wiki/raw/landing_rights/<country>/sources/`

---

## 3. Source Note 文件格式

每个 source note 文件应包含 YAML front matter。

推荐格式：

```yaml
---
country: Mongolia
topic: landing_rights
doc_type: source_note
source_id: mn-crc-satellite-network-license
source_name: Satellite communications network establishment, operation and service license page
source_url: https://example.com
source_agency: CRC
source_type: HTML
local_source_path: wiki/raw/landing_rights/mongolia/sources/html/example.html
language: mn
review_status: draft
last_extracted: 2026-07-07
---
```

---

# Source Note: <source_name>

## 1. 来源信息

| 项目     | 内容                            |
| ------ | ----------------------------- |
| 来源名称   |                               |
| 发布机构   |                               |
| 来源类型   | HTML / PDF / DOCX / XLSX / 其他 |
| 原始链接   |                               |
| 本地来源路径 |                               |
| 来源语言   |                               |
| 抽取日期   |                               |

---

## 2. 主要内容摘要

用 3-8 条概括该来源主要讲了什么。

要求：

1. 只总结来源中明确出现的信息；
2. 不扩展推测；
3. 不判断该来源属于哪个 cases 文件；
4. 如果只是入口页、目录页或背景页，应直接说明。

---

## 3. 主要原始信息

提取来源中最重要的原始信息。

可包括：

* 页面标题；
* 主要小节；
* 许可名称；
* 机构名称；
* 申请条件；
* 申请材料；
* 费用；
* 有效期；
* 审批流程；
* 附件名称；
* 法规名称；
* 其他重要信息。

没有出现的信息不用写。

---

## 4. 关键原文依据

记录最关键的原文依据。

| 位置                        | 原文要点 |
| ------------------------- | ---- |
| 页面标题 / 小节名 / 表格名 / PDF 页码 |      |

要求：

1. 不要大段复制原文；
2. 网页记录标题、小节名或表格名；
3. PDF 记录页码；
4. 只记录最关键的信息。

---

## 5. 信息不足或需人工复核

记录该来源中不清楚、无法提取或需要人工确认的地方。

示例：

* 页面可以访问，但附件未下载；
* 页面为目录页，需要继续打开子链接；
* 原文为外文，需要人工复核翻译；
* 页面未说明费用；
* 页面未说明审批周期；
* 页面未说明是否适用于外国卫星运营商。

---

## 6. 生成规则

Agent 生成 source note 时必须遵守：

1. 只提取来源本身的信息；
2. 不生成大量空字段；
3. 来源未提及的信息直接省略；
4. 不得编造法规、机构、费用、材料或流程；
5. 如果来源内容很少，应明确说明“该来源信息有限”。
