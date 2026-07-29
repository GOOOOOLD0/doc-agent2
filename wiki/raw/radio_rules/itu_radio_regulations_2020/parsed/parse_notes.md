# itu_radio_regulations_2020 解析记录

- 共识别到 10 个章、62 个条、0 个节、0 个子条款。（来源文件类型: .pdf，位置单位: 页）
- 使用 profile: itu_radio_regulations，层级体系: chapter > article > section > clause
- 需要保留的元数据: pdf_page, page_label, article_number, clause_number, tables, footnotes, cross_references, wrc_revision
- 以下 preserve 标记依赖 LLM 精修阶段处理: article_number, clause_number, tables, footnotes, wrc_revision


## split_book.py 追加记录

- 特殊条款 article_1: 在 '第I节 – 一般术语' 处切分，规则: split_by=['section']
- 特殊条款 article_1: 在 '第II节 – 有关频率管理的专用名词' 处切分，规则: split_by=['section']
- 特殊条款 article_1: 在 '第III节 – 无线电业务' 处切分，规则: split_by=['section']
- 特殊条款 article_1: 在 '第IV节 – 各种无线电台与系统' 处切分，规则: split_by=['section']
- 特殊条款 article_1: 在 '第V节 – 操作术语' 处切分，规则: split_by=['section']
- 特殊条款 article_1: 在 '第VI节 – 发射与无线电设备的特性' 处切分，规则: split_by=['section']
- 特殊条款 article_1: 在 '第VII节 – 频率共用' 处切分，规则: split_by=['section']
- 特殊条款 article_1: 在 '第VIII节 – 空间技术术语' 处切分，规则: split_by=['section']
-   特殊条款 article_01: 写入节文件 section_00.md (217 字符)
-   特殊条款 article_01: 写入节文件 section_01.md (790 字符)
-   特殊条款 article_01: 写入节文件 section_02.md (279 字符)
-   特殊条款 article_01: 写入节文件 section_03.md (3112 字符)
-   特殊条款 article_01: 写入节文件 section_04.md (3515 字符)
-   特殊条款 article_01: 写入节文件 section_05.md (1569 字符)
-   特殊条款 article_01: 写入节文件 section_06.md (3059 字符)
-   特殊条款 article_01: 写入节文件 section_07.md (1060 字符)
-   特殊条款 article_01: 写入节文件 section_08.md (886 字符)
-   特殊条款 article_01: 同时写入全文 article.md (14495 字符)
- 特殊条款 article_1: 按 ['section'] 切分为 9 个子块。


## build_source_notes.py 追加记录

- 共生成 11 个 Source Note
- 输出目录: C:\Users\ld\Desktop\yx\doc-agent2\wiki\raw\radio_rules\itu_radio_regulations_2020\source_notes
- 来源文档: 无线电规则：2020年第1卷——条款 (version: 2020)


## compile_wiki.py 追加记录

- 共生成 11 个 Wiki 概念页面
- 输出目录: C:\Users\ld\Desktop\yx\doc-agent2\wiki\concepts\radio_rules
- 已更新 wiki/index.md 和 wiki/log.md
- 来源文档: 无线电规则：2020年第1卷——条款 (version: 2020)

## optimize_wiki_pages.py — Python 机械层

- 去重: 0 行
- 垃圾行: 0 行
- OCR 错字: 是
- 行末垃圾: 0 处
- 交叉引用: 100 个链接

### 待 LLM 精修

Python 机械层已完成清洗（去重、垃圾行、OCR修正、条款合并、交叉引用）。
**所有表格识别与重建由 LLM 全权负责：**
1. **条款→定义表格**：将条款号+定义文本转为 `| 条款 | 定义 |` 表格（包括单条款）
2. **内联表格重建**：检测合一条款中的内联结构化数据，重建为 Markdown 表格
   - 频段划分表（频段序号+符号+频率范围+米制细分）
   - 多语种术语对照表（中文+法文+英文+西班牙文+阿拉伯文+俄文）
   - 任何其他 PDF 压平的结构化数据
3. **残行修正**、**交叉引用审查**、**脚注归属**、**页码格式化**、**一致性检查**

preserve 标记参考: tables, footnotes, wrc_revision, article_number, clause_number, cross_references
