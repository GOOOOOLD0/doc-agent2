---
name: book-ingestion
description: 将书籍、法规、技术标准或长文档解析并整理为 Wiki。
status: draft
---

# Book Ingestion

## 使用场景

当用户要求执行以下任务时使用本 Skill：

- 将一本书加入 Wiki；
- 解析 PDF、DOCX 等长文档；
- 按章节、条款或小节拆分文档；
- 根据书籍内容生成 Source Notes；
- 根据 Source Notes 生成主题 Wiki 页面。

## 输入

每本书应具有独立文档目录：

`wiki/raw/<topic>/<doc_id>/`

目录中至少包括：

- `document.yaml`
- `source/`

文档处理规则由 `document.yaml` 中指定的 profile 决定。

配置文件位于：

`config/book_ingestion/`

## 处理流程

书籍处理按照以下顺序执行：

1. 读取 `document.yaml`；
2. 读取对应的 profile 配置；
3. 解析原始书籍；
4. 按文档结构切分；
5. 生成 Source Notes；
6. 生成主题 Wiki 页面；
7. 更新相关索引。

计划使用的工具：

- `tools/book_ingestion/parse_book.py`
- `tools/book_ingestion/split_book.py`
- `tools/book_ingestion/build_source_notes.py`
- `tools/book_ingestion/compile_wiki.py`

## 输出位置

解析结果：

`wiki/raw/<topic>/<doc_id>/parsed/`

切分结果：

`wiki/raw/<topic>/<doc_id>/chunks/`

Source Notes：

`wiki/raw/<topic>/<doc_id>/source_notes/`

最终 Wiki 页面：

`wiki/concepts/<topic>/`

## 基本规则

- 不得修改或覆盖 `source/` 中的原始文件；
- 优先按照章节、条款、小节等原始结构切分；
- 只有无法按照结构切分时，才按 token 长度兜底；
- 表格、脚注和正文之间的关联应尽量保留；
- Source Note 和 Wiki 页面必须保留原文位置；
- 解析质量不足时，应记录问题，不得直接生成确定性结论。

## 当前状态

本 Skill 当前为流程草案。

具体命令参数、失败处理和重跑规则，应在相关 Python 工具完成后补充。