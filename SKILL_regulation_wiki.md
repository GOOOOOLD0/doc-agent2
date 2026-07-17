# Skill: Long Regulation Document Wiki-ization（超长法规文档 Wiki 化）

> 本文件独立存放于**项目根目录**，与 `AGENT.md`、`wiki/`、`scripts/` 平级：
>
> ```
> project_root/
> ├── AGENT.md
> ├── SKILL_regulation_wiki.md        <-- 本文件
> ├── scripts/
> │   └── regulation_wiki/            <-- 本Skill的可执行脚本
> │       ├── extract_structure.py
> │       ├── chunk_articles.py
> │       ├── clean_ocr_text.py
> │       ├── generate_wiki_pages.py
> │       └── build_index.py
> └── wiki/
>     ├── raw/regulations/<reg_name>/
>     └── concepts/regulations/<reg_name>/
> ```
>
> 完整规则维护于本文件，不并入 AGENT.md 正文；AGENT.md 中仅保留
> 触发条件判断和指向本文件的调用说明（见文末"AGENT.md 插入片段"）。
> 数据存放在 `wiki/raw/regulations/` 和 `wiki/concepts/regulations/`
> 下，与 landing_rights 使用的子文件夹并列、不嵌套、不共享内容。

---

## 0. 核心原则（先于所有细节）

1. **结构先行，语义在后**：先用规则从 PDF 书签/目录里抽出"章-条"结构，
   不让 LLM 猜层级；结构确定之后，LLM 只负责在确定的切片内做摘要、
   关键词、引用候选，不负责决定切片边界。
2. **原文必须完整保留**：任何页面的"原文正文"区块都是完整原文，
   摘要只是附加字段，不能用摘要取代原文，也不能用"看起来更通顺"
   的复述悄悄替换原文。
3. **交叉引用只做规则定位，不臆造**：能在结构表里查到目标就链接，
   查不到就标 `[待链接]`，禁止为了"完整"而编一个目标。
4. **不确定的东西必须标注，不允许沉默处理**：文字提取失败、OCR
   噪声、书签缺失、条款过长等情况，都要写进 `parse_notes.md` 或页面
   的"备注/待确认项"，不能悄悄跳过或悄悄修正。
5. **规则 + LLM 混合，而不是"LLM 通读全书"**：LLM 不直接处理整本书，
   只处理规则已经切好的、语义完整的最小单元（一条，或超长条款拆出
   的一个脚注）。

---

## 1. Skill 定位

用于将**单份超长、结构复杂的法规/标准原文**（如《无线电规则》《ITU-R
建议书》等，通常几十到几百页，带章/条款层级）转化为四层结构：

| 层 | 内容 | 存放位置 |
|---|---|---|
| 原始层 | 原始 PDF、逐条原文文本 | `wiki/raw/regulations/<reg_name>/` |
| 结构层 | 章-条-页码树 | `wiki/raw/regulations/<reg_name>/structure.json` `.md` |
| 语义层 | 逐条 wiki 页面（摘要/关键词/引用/原文） | `wiki/concepts/regulations/<reg_name>/articles/` |
| 检索层 | 目录索引、主题索引 | `wiki/concepts/regulations/<reg_name>/index/` |

本 Skill 只处理"单份长文档本身的结构化转化"，不涉及国家案例分析，
不与 landing_rights 相关文件互相引用。

---

## 2. 触发条件

当用户满足以下情况之一时，Agent 应启用本 Skill：

1. 上传或指定了一份长篇法规、标准、规则类 PDF/文档，并要求"建wiki""整理成知识库""方便以后查"；
2. 要求对某部法规按章节/条款做结构化整理；
3. 要求对某部法规做交叉引用梳理或主题索引；
4. 要求基于某部法规原文做条款级问答准备（RAG）。

不适用于 landing_rights 相关的零散短篇资料摘要收集，那属于另一 Skill。

---

## 3. 知识库路径规则

```
wiki/raw/regulations/<reg_name>/
├── source.pdf / source.docx 或指向原文件的说明   # 支持 .pdf 和 .docx
├── structure.json                # 机器可读的章-条-位置树(position_type: page/paragraph_index)
├── structure.md                  # 人可读版本
├── parse_notes.md                # 解析过程中的异常、待确认项(持续追加,不覆盖)
├── raw_chunks/
│   ├── <article_id>.txt              # 逐条原文(text_layer / ocr / vision_llm_transcribe / docx_text)
│   └── <article_id>.structured.json  # 按款号重排后的结构化记录(clean_ocr_text.py产出)
└── semantic/
    └── <article_id>.json         # LLM按提示词模板产出的加工字段(清洗结果+摘要+引用候选,可选,存在才用)

wiki/concepts/regulations/<reg_name>/
├── common/
│   ├── chunking_rules.md
│   ├── article_page_template.md
│   ├── cross_reference_rules.md
│   └── semantic_enrichment_prompt.md
├── articles/
│   └── <article_id>.md           # 正式 wiki 页面(原文正文为按款表格)
└── index/
    ├── toc_index.md
    └── topic_index.md
```

### 3.1 `<reg_name>` 命名规则

必须带版本号，格式：英文小写+下划线+版本标识（优先用原文标注年份）。
示例：`radio_regulations_2020`。不同版本各自独立目录，不自动合并。

---

## 4. common 文件读取规则

执行本 Skill 时，应优先读取 `wiki/concepts/regulations/<reg_name>/common/`
下的四个文件。若该法规首次处理，先创建这四个文件的初始版本
（可直接复用本 Skill 自带的通用版本，按具体法规调整），再开始切分。

---

## 5. 推荐处理流程

### 5.1 结构层（`extract_structure.py`）

1. 统一用 fitz（PyMuPDF）读取：PDF 走 `get_toc()` 拿书签，DOCX
   走段落文字扫描（用同一套"章/条"正则规则判断标题，不依赖 Word
   的 Heading 样式，因为很多文档标题只是加粗的普通段落）；
2. 用"下一个节点的起始位置 - 1"推算每个节点的结束位置（PDF 单位
   是页码，DOCX 单位是段落序号，统一记在 `structure.json` 的
   `position_type` 字段里，下游脚本按这个字段判断怎么取内容区间）；
3. 若 PDF 没有书签、或 DOCX 里规则扫描不到任何标题段落，如实记录到
   `parse_notes.md`，标注"需人工核对目录后手动补 structure.json"，
   不得让 LLM 凭空编一份目录出来；
4. 产出 `structure.json`（供后续脚本用）和 `structure.md`（人读）。

支持的文件类型：`.pdf`、`.docx`。其他格式暂不支持，需先转换。

### 5.2 原始层文字抽取（`chunk_articles.py`）

部分 PDF 存在字体编码表（ToUnicode CMap）损坏的情况：直接抽取文字层
时中文会变成乱码，英文数字正常。这种问题不会自己消失，必须在流程里
加检测，判断文字层是否可靠，不可靠时才降级到 OCR。

判断逻辑（顺序不能颠倒）：

1. 先去掉所有空白字符再统计中文占比。fitz 抽取中文时经常在字符间
   插入空格（字体字宽导致，不代表原文真的有空格），若直接用"中文
   字符数 ÷ 文本总长度"计算比例，会被这些空格拉低分母之外的比例，
   造成误判，所以必须先去空白再算；
2. 有效字符数太少（默认 < 20）时，不基于比例做判断，直接采用抽取
   结果——内容本来就少的页面（扉页、空白页）没有强行 OCR 的必要，
   小样本下比例本身也不稳定；
3. 只有"有效字符量足够、去空白后中文占比仍然很低"，才判定文字层
   确实损坏，记录到 `parse_notes.md`，改用页面转图片 + OCR。

抽取到的文字统一做"字符间空格归一化"：只删除两个中文字符之间的
空格，不动其他任何空格（英文单词间、数字单位间的空格照常保留）。
这一步处理的是提取过程本身产生的排版 artifact，不是修改原文内容——
原文本来就没有这些空格。

OCR 是最后一道防线，尽量少用：

- 优先用 fitz 原生文字层，只有真正判定损坏才降级到 OCR；
- OCR 优先用 Tesseract，但对复杂版式页面（旋转页眉、多栏交错、
  频率划分表这类大表格）识别噪声较大，这类页面更稳妥的做法是改用
  具备视觉能力的 LLM 直接读页面图片做转录（模板见
  `semantic_enrichment_prompt.md`）；
- DOCX 是原生文字格式，永远不需要 OCR，`method` 统一记为
  `docx_text`；
- 无论哪种方式抽取，"原文来源"（text_layer / ocr /
  vision_llm_transcribe / docx_text）都必须写进最终页面的元信息
  字段，不允许隐藏抽取方式。

### 5.3 切分粒度（详见 `chunking_rules.md`）

- 默认一条 = 一个块；
- 跨页数超过阈值（默认15页）的"超长条款"，不得只生成一个整块摘要，
  必须做二次切分。本法规的第5条（频率划分，跨152页）是典型案例，
  应按其内部的脚注编号（如 `5.150`）二次切分成独立页面，因为全文
  的交叉引用真正指向的就是这些脚注编号，而不是整条第5条。

### 5.3.1 格式重排层（`clean_ocr_text.py`，纯结构性，零内容改动）

OCR/文字层产出的原文经常"内容对，换行乱"——一句话被切成三四行。
这一步在语义加工之前插入，按款号（单独一行的 `3.1`）把零散换行
重新组织成款级结构化记录 `.structured.json`（每款独立的编号、
页码、文字），只调整换行位置，不增删改任何字符。

**异常符号/错字清洗不在这一步做**：字符是否识别错误，本质上要靠
上下文语义判断，规则脚本判断不了，也无法用一份固定字典穷举所有
可能的错误模式。这部分工作放在语义层的 LLM（见 5.4），
`clean_ocr_text.py` 只负责结构性重排，不承担语义判断的职责。

### 5.4 语义层（`generate_wiki_pages.py` + LLM）

1. LLM 读取 `.structured.json` 里的款级原文，一次性完成两项任务
   （提示词见 `semantic_enrichment_prompt.md`）：
   - **任务A：逐款异常符号/错字清洗**——只处理明显的 OCR 识别噪声
     （形近字、字母缺失、孤立乱码符号），不改写句式、不做"表达优化"，
     每处改动都要记录 `{from, to, reason}` 三元组，原文和清洗结果
     都要保留，不能只留清洗后的版本；
   - **任务B：全条摘要、关键词、原始引用候选**（`raw_cross_references`），
     LLM 只负责列出候选原文，**不负责**判断引用具体指向哪个条款——
     这一步交给规则脚本（见 5.5）；
2. 产出存成 `semantic/<article_id>.json`；
3. `generate_wiki_pages.py` 把 `.structured.json`（权威原文）+
   `semantic.json`（清洗结果/摘要/引用）按 `article_page_template.md`
   组装成正式页面——"原文正文"渲染成按款号的表格，原文列和清洗列
   分开展示，不合并成一大段文字，也不用原文回填冒充"已清洗"；
   没有语义 JSON 时，页面仍然生成（保留完整原文表格），只是摘要/
   关键词/清洗列标"待生成"/"待清洗"，不生成空骨架页面（原文永远
   是有内容的）。

### 5.5 交叉引用定位（详见 `cross_reference_rules.md`，含接地检查）

语义加工阶段的 LLM 产出的引用候选，不能默认它一定真实存在于原文——
有可能是凭空生成的。所以定位目标之前必须先做接地检查：

1. 先验证 LLM 给出的每条 `raw_cross_reference` 是否能在原文里逐字
   找到；找不到 → 标记 `[疑似幻觉，原文未找到该引用文字]`，不进入
   目标定位（这种情况需要回头检查语义加工这一步是不是出了问题）；
2. 接地检查通过后，再用正则在原文里匹配条款号/脚注号，对照
   `structure.json` 里已知的合法条款集合做定位；
3. 定位成功才生成链接，定位失败标 `[待链接]`（这种情况引用文字
   本身是真实的，只是暂时找不到目标，和"疑似幻觉"性质不同）。

### 5.6 检索层（`build_index.py`）

- `toc_index.md`：按结构层的章节顺序列出所有条款，已生成页面的
  给链接，未处理的如实标注"未处理"，不能让索引看起来"全部完成"
  而实际只处理了一部分；
- `topic_index.md`：汇总所有已生成页面的关键词做主题聚合，没有
  关键词（即还没做语义加工）的条款不出现在主题索引里。

---

## 6. 分析原则

1. 原文条款正文必须完整保留，不得用摘要替代原文；
2. 摘要、关键词、交叉引用属于"加工信息"，必须与原文分区展示；
3. 无法确认的目录层级、交叉引用目标、OCR 疑似错字，必须标记
   "待确认"，不得臆造或悄悄修正原文；
4. 条款编号、频段等关键数字信息，不得在加工过程中改写；
5. 若原文本身存在勘误、修订版本差异，应在对应条款页注明版本来源；
6. 不得因为某条款内容冗长而跳过处理或仅做部分摘要，超长条款按
   5.3 的规则拆分处理；
7. 本 Skill 产出的所有文件仅存放于 `wiki/raw/regulations/` 和
   `wiki/concepts/regulations/` 之下，不得写入 landing_rights 相关路径。

---

## 7. 回答风格

沿用 AGENT.md 第15节的总体回答风格（先结论后步骤、面向非工程背景
解释路径和命令、不确定内容明确标注），本 Skill 不单独定义新的风格规则。

