# Skill: Long Regulation Document Wiki-ization（超长法规文档 Wiki 化）

> 本文件独立存放于**项目根目录**，与 `AGENT.md`、`wiki/` 平级：
>
> ```
> project_root/
> ├── AGENT.md
> ├── SKILL_LONG_DOC.md   <-- 本文件
> └── wiki/
>     ├── raw/
>     └── concepts/
> ```
>
> 完整规则维护于本文件，不并入 AGENT.md 正文；AGENT.md 中仅保留
> 触发条件判断和指向本文件的调用说明（见文末"AGENT.md 插入片段"）。
>
> 本 Skill 产出的数据存放在 `wiki/raw/` 和 `wiki/concepts/` 下**新增的
> 独立子文件夹**中，与 landing_rights 使用的子文件夹并列、不嵌套、
> 不共享内容、不做交叉引用，仅仅是共用 `wiki/` 这一层父目录。

---

## 1. Skill 定位

用于将**单份超长、结构复杂的法规/标准原文**（如《无线电规则》《ITU-R 建议书》
《频率划分表》等，通常几十到几百页，带章/条款层级）转化为：

1. 保留条款级细节、可逐条查阅的 wiki 页面；
2. 带交叉引用跳转和主题索引的知识库；
3. 可选：供后续语义检索/问答使用的向量索引来源。

本 Skill 只处理"单份长文档本身的结构化转化"，不涉及任何国家案例分析、
不引用、不被 landing_rights 相关文件引用。

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

本 Skill 复用项目已有的 `wiki/raw/` 和 `wiki/concepts/` 两个顶层目录，
在其下**各自新增一个独立子文件夹** `regulations/`，与 landing_rights
现有的子文件夹（`landing_rights/`）并列，互不嵌套、互不引用：

```
wiki/raw/regulations/
└── <reg_name>/
    ├── source.pdf                    # 原始文件（或引用路径）
    ├── structure.md                  # 解析出的目录/条款树
    └── parse_notes.md                # 解析异常、待确认项

wiki/concepts/regulations/
└── <reg_name>/
    ├── common/
    │   ├── chunking_rules.md             # 切分粒度规则
    │   ├── article_page_template.md      # 单条wiki页模板
    │   └── cross_reference_rules.md      # 交叉引用识别与链接规则
    ├── articles/
    │   ├── <article_id>.md               # 逐条wiki页，如 5.150.md
    │   └── ...
    └── index/
        ├── toc_index.md                   # 按原文目录结构的索引页
        └── topic_index.md                 # 按主题聚合的索引页
```

即：

- 原始文件 → `wiki/raw/regulations/<reg_name>/`
- 加工后的 wiki 页面/索引 → `wiki/concepts/regulations/<reg_name>/`

与 landing_rights 现有路径（`wiki/raw/landing_rights/...`、
`wiki/concepts/landing_rights/...`）保持同级但完全独立的结构，
不产生路径混淆，也不共享任何具体文件。

### 3.1 `<reg_name>` 命名规则

`<reg_name>` 必须带版本号，格式为：英文小写+下划线+版本标识，
版本标识优先使用原文标注的年份或版本号。

示例：

- `radio_regulations_2020`（《无线电规则》2020年版）
- `radio_regulations_2024`（若未来出现修订版，作为独立 `<reg_name>`，不覆盖旧版）

不同版本之间不自动关联、不自动合并，如需比较版本差异，属于后续单独任务，
不在本 Skill 默认流程内处理。

---

## 4. common 文件读取规则

执行本 Skill 时，应优先读取：

`wiki/concepts/regulations/<reg_name>/common/`

若该目录尚不存在（首次处理该法规该版本），应先创建并生成上述三个 common
文件的初始版本，再开始正式切分处理；不得跳过 common 文件直接生成 articles。

---

## 5. 推荐处理流程

1. 读取原文 PDF，提取书签/目录，生成 `wiki/raw/regulations/<reg_name>/structure.md`（章-条款树）；
2. 若书签缺失或不完整，记录到 `wiki/raw/regulations/<reg_name>/parse_notes.md`，标注"需人工核对目录结构"，不得臆造层级；
3. 按 `structure.md` 中的条款单元切分原文，每个切片对应一条最小语义完整单元；
4. 对每个切片生成 `wiki/concepts/regulations/<reg_name>/articles/<article_id>.md`，字段包括：
   - 条款号、标题
   - 一句话摘要
   - 关键词（涉及频段、业务类型等，视具体法规内容而定）
   - 交叉引用（原文中"见第X条"类表述，转为内部链接）
   - 原文全文（完整保留，不得因摘要而删减或改写原文本身）
5. 交叉引用暂时无法定位目标条款时，保留原始引用文字并标记"待链接"，不得编造目标；
6. 全部条款处理完成后，生成 `wiki/concepts/regulations/<reg_name>/index/toc_index.md`（按原文结构）；
7. 根据条款关键词聚合生成 `wiki/concepts/regulations/<reg_name>/index/topic_index.md`（按主题）；
8. 如需支持问答/语义检索，对 `articles/` 下全部条款生成向量索引（存储位置另行确定，不在本文件内维护）；
9. 输出处理总结：已处理条款数、未能定位的交叉引用数量、待人工核对项。

---

## 6. 分析原则

1. 原文条款正文必须完整保留，不得用摘要替代原文；
2. 摘要、关键词、交叉引用属于"加工信息"，必须与原文分区展示，不得混淆；
3. 无法确认的目录层级、交叉引用目标，必须标记"待确认"，不得臆造；
4. 条款编号、频段等关键数字信息，不得在加工过程中改写或四舍五入；
5. 若原文本身存在勘误、修订版本差异，应在对应条款页注明版本来源；
6. 不得因为某条款内容冗长而跳过处理或仅做部分摘要；
7. 本 Skill 产出的所有文件仅存放于 `wiki/raw/regulations/` 和
   `wiki/concepts/regulations/` 之下，不得写入 `wiki/raw/landing_rights/`、
   `wiki/concepts/landing_rights/` 等 landing_rights 相关路径。

---

## 7. 回答风格

沿用 AGENT.md 第15节的总体回答风格（先结论后步骤、面向非工程背景解释路径和命令、
不确定内容明确标注），本 Skill 不单独定义新的风格规则。

