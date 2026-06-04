# Wiki 结构规范 / Wiki Schema

## 领域范围 / Domain

本 Wiki 用于整理卫星通信监管、频谱管理、政策文件、技术报告和分析结论。重点覆盖 ITU、FCC、NGSO/GSO、EPFD rules、spectrum regulation 和 technical document analysis。

## 写作约定 / Conventions

- 文件名使用小写字母和连字符，不使用空格，例如 `epfd-rules.md`。
- 除非用户明确要求使用其他语言，Wiki 页面正文默认使用简体中文；专业名称、机构名称、法规名称和技术术语可以保留英文原文。
- 每个 Wiki 页面都应以 YAML frontmatter 开头。
- 页面之间使用 `[[wikilinks]]` 互相链接；建议每页至少包含 2 个出站链接。
- 更新页面时，必须同步更新 `updated` 日期。
- 每个新增页面都应添加到 `index.md` 的对应章节下。
- 每次重要操作都应追加记录到 `log.md`。
- **Provenance markers / 来源标记：** 如果某个页面综合了 3 个以上来源，并且某段内容来自特定来源，应在该段末尾添加 `^[raw/articles/source-file.md]`。

## 页面元数据 / Frontmatter

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: source | entity | concept | comparison | report | query | summary
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]
confidence: high | medium | low
contested: true
contradictions: [other-page-slug]
---
```

`confidence` 和 `contested` 是可选字段，但对于观点较多、变化较快或存在争议的主题，建议填写。

## 标签分类 / Tag Taxonomy

- epfd
- itu
- fcc
- ngso
- gso
- satellite
- spectrum
- regulation
- analysis
- documents
- policy
- coordination
- interference
- rule-making
- public-comment

## 页面创建标准 / Page Thresholds

- **Create a page / 创建页面：** 当某个实体或概念出现在 2 个以上来源中，或它是单个来源的核心主题时，创建独立页面。
- **Add to existing page / 补充现有页面：** 当新来源提到的内容已经被已有页面覆盖时，更新现有页面。
- **Don't create a page / 不创建页面：** 对于顺带提及、细枝末节或领域范围之外的内容，不创建独立页面。
- **Split a page / 拆分页面：** 当页面过长或主题混杂时，拆分为多个页面。
- **Archive a page / 归档页面：** 当页面内容已被新内容完全取代时，将其移动到 `_archive/`，并从 `index.md` 中移除。

## 原始文档页面 / Source Page

Source Page 用于记录单篇原始文档。

必须包含：
- 文档标题
- 来源机构
- 发布时间
- 文件类型
- 原始路径或来源链接
- 一句话总结
- 核心内容
- 关键条款或关键观点
- 涉及概念
- 涉及机构
- 可能影响
- 待核查问题

## 实体页面 / Entity Page

Entity Page 用于记录组织、监管机构、卫星运营商、频段、标准文件等实体。

## 概念页面 / Concept Page

Concept Page 用于解释长期概念。

必须包含：
- 概念定义
- 背景说明
- 相关规则
- 相关文档
- 争议或待核查问题

## 比较页面 / Comparison Page

Comparison Page 用于并列比较分析，例如 ITU 与 FCC 的监管路径比较、NGSO 与 GSO 框架比较。

## 专题报告页面 / Report Page

Report Page 用于生成专题分析报告。

必须包含：
- 问题背景
- 主要发现
- 证据来源
- 影响分析
- 结论
- 待进一步核查的问题

## 更新策略 / Update Policy

当新信息与已有内容冲突时：
1. 先检查日期；通常较新的来源优先于较旧来源。
2. 如果确实存在矛盾，应同时记录双方观点，并标明日期和来源。
3. 在 frontmatter 中标记：`contradictions: [page-name]`。
4. 在 lint 或人工检查阶段提示用户复核。

## 基本原则 / Core Principles

- 不允许编造原文没有的信息。
- 重要结论必须能追溯到原始文档。
- 不确定内容必须标注“待核查”。
- 必须区分“文档事实”和“模型推断”。
