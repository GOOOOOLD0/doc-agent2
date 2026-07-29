---
name: book-ingestion
description: 将书籍、法规、技术标准或长文档解析并整理为 Wiki。chunk 即做清洗，source note = LLM 摘要。
status: active
---

# Book Ingestion

## 核心理念

- **chunk 即做清洗**：PDF 垃圾（页眉/页码/RR1-2）在 chunk 阶段就清理干净，不留到后面。
- **source note = LLM 摘要**：不再是 chunk 的复制品，而是基于清洗后 chunk 灵活生成的提炼——提取概念、观点、机构分类、一句话总结等。
- **frontmatter 精简统一**：所有阶段文件都有精简 YAML frontmatter（仅必要字段），正文不重复元信息。
- **交叉引用后移**：chunk 保持纯文本引用（第N条、WRC-NN），wikilink 注入在 compile_wiki 阶段统一完成。
- **chunk 排版规范**：定义类条款表格化，多段条款行距统一。

## 处理流程

```
1. parse_book.py            PDF TOC 提取 → structure.json
2. split_book.py            按条款切分 → chunks/（精简 frontmatter，清除元标记）
3. chunk 清洗               垃圾清除 + 排版格式化 → 干净的 chunks/
4. build_source_notes.py    生成 Source Note 壳子 → source_notes/
5. LLM 摘要生成              基于清洗后 chunk 灵活生成摘要 → source_notes/
6. compile_wiki.py          生成 Wiki 概念页面（含交叉引用注入）→ wiki/concepts/
7. optimize --rebuild-core  从 chunks 合并全文 → 概念页完整文本
```

## 各步骤详解

### Step 1: parse_book.py — 结构提取

- 从 PDF TOC（get_toc）或 DOCX 标题段落提取文档结构树
- 输出 `parsed/structure.json`, `structure.md`, `parse_notes.md`
- 配置驱动：`profile.patterns` 决定节点分类

### Step 2: split_book.py — chunk 生成

- 按 `preferred_level`（通常是 article）提取每个节点的页范围
- PDF 文字层若损坏（CJK 占比 < 5%）自动切换 OCR（EasyOCR）
- 超出 `max_chunk_tokens` 的节点按 `fallback_chunk_tokens` 兜底切分
- 特殊条款（`profile.special_articles`）支持 `section`/`table` 等策略

**精简 frontmatter（仅 9 个必要字段）：**

```yaml
title: 第1条 — 第1节
type: chunk
tags: [regulation, radio_rules]
source_doc: 无线电规则：2020年第1卷——条款
source_version: 2020
source_location: 第15页 至 第32页
node_id: 1
chunk_id: article_01_section_01
```

**已删除的冗余字段**：`created`, `updated`, `source_doc_id`, `source_type`, `source_file`, `source_language`

**正文规则**：
- 清除 `--- page N ---` 元标记（页码范围已在 frontmatter.source_location）
- 其他 PDF 原生活圾（印刷页码、页眉、RR1-2）由 Step 3 清洗

### Step 3: chunk 清洗

**3a. mechanical-clean + 排版格式化**（Python 确定性）：

1. **垃圾行删除**：`--- page N ---`、`RR*-*`、孤立数字行、OCR 乱码、章节页眉、印刷页码
2. **OCR 错字修正**：GH2→GHz、困际→国际、第工节→第I节
3. **残行合并**：OCR 切碎的同一句子合并（以句号/分号为边界）
4. **节级裁剪**：每个 section 文件只保留对应节的条款（从 article.md 全文按节标题切分）
5. **排版格式化**：
   - **定义类条款**（单段、≤300字、≥3条）→ 转为 Markdown 表格 `| 条款 | 定义 |`
   - **多段条款**（含注释、子段落）→ 款号独占一行，正文紧跟，条款间一个空行
   - 条款内不得有空行（多段合并）
   - 章节标题前后各一个空行
6. **注意**：此阶段**不做交叉引用 wikilink 注入**——chunk 保持纯文本（第N条、WRC-NN）

**3b. LLM 精修**（代理执行）：

1. **内嵌子表格检测与重构**（最高优先级——先于其他所有步骤）：
   当 `| 条款 | 定义 |` 表格中某条款的定义文本引用了内嵌表格（特征：条款文本含"按照下表"/"如下表所示"/"按以下划分"/"列示"等，且该条款行后紧跟另一个表头），必须重构：
   - **关闭外层表格**：在该条款行后插入空行
   - **独立渲染子表格**：内嵌表格独立成表，保留其原有列结构
   - **重启外层表格**：子表格 + 注释结束后，插入 `| 条款 | 定义 |` + `|------|------|` 重新开始外层表格
   - **示例**（条款 2.1 含频段表）：
     ```
     | 条款 | 定义 |
     |------|------|
     | 2.1 | ...定义文本，按下表列示... |

     | 频段序号 | 符号 | 频率范围 | 米制细分 |
     |----------|------|---------|---------|
     | 4 | VLF | 3-30 kHz | 万米波 |
     ...

     注1：...

     | 条款 | 定义 |
     |------|------|
     | 2.2 | ... |
     ```
   - **关键**：重启外层表格时必须带表头和分隔行，否则 2.2 行会被 markdown 解析为内嵌表格的列（若列数不同则渲染错乱）

2. **表格重建**：OCR 压缩的结构化数据重建为 Markdown 表格（如频段表）
3. **残行修正**：检查 Python 合并的边缘情况
4. **脚注归属**：确保脚注紧跟相关条款
5. **WRC 修订标记保留**：`（WRC-03）` 等必须保留
6. **最终一致性**：条款号连续、款号完整

I/O: `chunks/` → `chunks/`（原地清洗覆盖）

### Step 4: build_source_notes.py — Source Note 壳子

- **元信息来源**：从 chunk 文件的 YAML frontmatter 读取（精简字段）
- **生成内容**：frontmatter + chunk 路径引用 + 所有语义字段占位符
- **不再包含**：属性表格、chunk 原文复制

Source Note 模板：
```markdown
---
title: 第1条 — 第1节
type: source
source_doc: ...
source_location: ...
node_id: article_01_section_01
---

## 一句话总结
(待LLM生成)

## 源文件
原始内容参见: `chunks/article_01/section_01.md`

## 关键条款 / 关键观点
(待LLM生成)
...
```

### Step 5: LLM 摘要生成

代理遍历所有 Source Note，读取对应 chunk 原文，灵活生成摘要填入各字段：
- **一句话总结**：核心主题
- **关键条款/关键观点**：重要定义、规则、限值
- **涉及概念**：关键术语和概念
- **涉及机构**：组织、部门、委员会
- **可能影响**：实际应用中的影响
- **待核查问题**：需进一步核实的内容

要求：中文、详实、基于原文不编造。

### Step 6: compile_wiki.py — Wiki 概念页面

- **核心内容**：从 cleaned chunks 拉全文
- **摘要**：从 source_notes 拉 LLM 生成的摘要
- **交叉引用注入**（本阶段唯一做 wikilink 的地方）：
  - `第N条` → `[[concepts/<topic>/article_N|第N条]]`
  - `附录N` → `[[concepts/<topic>/appendix_N|附录N]]`
  - `WRC-NN` → `[[concepts/<topic>/wrc-NN|WRC-NN]]`
- 更新 wiki/index.md, wiki/log.md, toc_index.md

### Step 7: optimize --rebuild-core

- 仅做 chunk 合并（将同一条款的多 chunk 文件合并为完整文本）
- `--mechanical-clean` 和 LLM 精修在此阶段不再需要

## Chapter-Scoped Runs

```
uv run python tools/book_ingestion/parse_book.py <document.yaml>
uv run python tools/book_ingestion/split_book.py <document.yaml> --nodes 1,2,3
# Step 3: chunk 清洗（代理执行 mechanical-clean + LLM 精修，作用于 chunks/）
uv run python tools/book_ingestion/build_source_notes.py <document.yaml> --nodes 1,2,3
# Step 5: LLM 摘要生成（代理执行）
uv run python tools/book_ingestion/compile_wiki.py <document.yaml> --nodes 1,2,3
uv run python tools/book_ingestion/optimize_wiki_pages.py <document.yaml> --nodes 1,2,3 --rebuild-core
```

## Pitfalls

- **清洗必须先于 source note**：PDF 垃圾在 chunk 阶段清完，source note 只接收干净 chunk。
- **source note ≠ chunk 复制**：source note 是摘要，只放 LLM 提炼的内容 + chunk 路径索引。
- **交叉引用只在 wiki 阶段注入**：chunk 保持纯文本引用，wikilink 由 compile_wiki.py 统一注入。
- **frontmatter 精简**：chunk 只含 9 个必要字段，source note / concept page 同理不冗余。
- **内嵌子表格必须显式断表重启**：当条款定义中包含子表格（如 2.1 含频段表），外层 `| 条款 | 定义 |` 表格必须在子表格前关闭（空行），子表格 + 注释独立渲染，然后在后续条款前用 `| 条款 | 定义 |` + `|------|------|` 重启外层表格。仅靠空行分离不够——若无重启表头，后续条款行会被 markdown 解析为子表格的列，列数不同时渲染彻底错乱。
- **所有步骤必须走完**：Step 1→2→3→4→5→6→7，少一步就是未完成。
- **每次全流程从干净状态重跑**：运行前清理旧输出目录。
- **项目本地 skill 优先**：本项目 skills/book-ingestion/SKILL.md 是权威版本。
