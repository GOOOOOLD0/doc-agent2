# Landing Rights Validators

本目录提供不调用模型 API 的确定性校验工具。校验通过只表示文件结构、证据登记和内部链接符合项目规则，不表示法律结论已经获得监管机构确认。

## Evidence Matrix

```bash
python3 tools/landing_rights/validate_evidence_matrix.py --country mongolia
```

检查内容包括：

- frontmatter、一级标题和占位符；
- `E-xxx`、`C-xxx` 连续编号；
- 每个证据项的八个必填字段和三类状态；
- Source Inventory、Source Notes 和未使用说明是否闭合；
- 资料概览中的计数是否与实际文件一致；
- 证据到 `01-09` 的目标文件映射；
- Obsidian 内部链接是否存在。

## 正式案例

校验全部正式 `01-09`：

```bash
python3 tools/landing_rights/validate_cases.py --country mongolia
```

只校验指定文件：

```bash
python3 tools/landing_rights/validate_cases.py \
  --country mongolia \
  --files 04,08
```

检查内容包括：

- 文件名、frontmatter、标题和必需章节；
- 已确认、分析推断和待确认三类结论分区；
- `08` 法规文件专用结构；
- 空章节、占位符和行尾空白；
- Obsidian 内部链接；
- Evidence Matrix 映射项是否能通过 Evidence ID、Source Note 或官方 URL 回溯。

当前案例未在正文显式记录 Evidence ID 时，工具会使用 Source Note 或 Source Inventory URL 进行近似检查并给出警告。法律语义、翻译和适用边界仍需人工审核。
