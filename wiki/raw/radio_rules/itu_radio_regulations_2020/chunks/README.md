# Chunks

本目录用于保存书籍经过结构化切分后生成的原文块。

切分结果由 `tools/book_ingestion/split_book.py` 自动生成，
不建议手工编辑。每个 chunk 应尽量保留：

- 文档 ID；
- 章节、条款或小节编号；
- PDF 页码和印刷页码；
- 原始标题；
- 原始正文；
- 表格、脚注及交叉引用关系。

示例文件名：

- `article_03.md`
- `article_01_section_02.md`
- `article_22_table_01a.md`

