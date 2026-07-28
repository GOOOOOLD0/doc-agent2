from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.landing_rights.validation import (
    validate_cases,
    validate_evidence_matrix,
)


VALID_MATRIX = """\
---
country: Testland
topic: landing_rights
doc_type: evidence_matrix
language: zh-CN
review_status: draft
last_reviewed: 2026-07-28
---

# 测试国卫星落地许可证据映射

## 1. 资料概览

- **已读取 Source Notes**：`1`
- **未使用 Source Notes**：`0`
- **已确认结论**：`1`
- **分析推断**：`0`
- **待确认事项**：`0`

## 2. 证据项

### E-001｜许可属于监管机构主管

**状态**

`已确认`

**结论**

测试国法律规定卫星许可由监管机构主管。

**依据**

- [[ts-law]]

**能够支持**

- 确认主管机构。

**不能支持**

- 不能确认费用。

**边界与风险**

- 仍需核对实施细则。

**目标文件**

- `08_testland_regulations.md`

**待确认**

- 无

## 3. 冲突、版本与翻译问题

本轮未发现。

## 4. 案例覆盖状态

### `08` 法规依据

- **主要证据**：`E-001`

## 5. 关键证据缺口

本轮未发现。

## 6. 生成前检查

- [x] 已完成检查。
"""

VALID_CASE_08 = """\
---
country: Testland
topic: regulations
case_type: structured_case
source_document: testland_evidence_matrix_and_official_source_notes
language: zh-CN
review_status: draft
last_reviewed: 2026-07-28
---

# 测试国法规依据

## 1. 文件用途

本文件梳理法规依据。

## 2. 结论摘要

### 2.1 已确认信息

主管机构已经确认。

### 2.2 分析推断

本轮没有分析推断。

### 2.3 待确认事项

费用仍需确认。

## 3. 核心法律和规则

| 来源 | 作用 |
| --- | --- |
| [[ts-law]] | 确认主管机构 |

## 4. 监管机构申请和说明页面

| 来源 | 状态 |
| --- | --- |
| [[ts-law]] | 已确认 |

## 5. 法规层级和主题映射

法律提供上位依据。

## 6. 版本、翻译和修订风险

需复核最新版本。

## 7. 仍需补充的官方文件

需补充收费文件。

## 8. 相关文件

- [[evidence_matrix]]
"""


class LandingRightsValidationToolsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "AGENT.md").write_text("# Agent\n", encoding="utf-8")

        self.raw = (
            self.root / "wiki" / "raw" / "landing_rights" / "testland"
        )
        self.notes = self.raw / "source_notes"
        self.cases = (
            self.root
            / "wiki"
            / "concepts"
            / "landing_rights"
            / "cases"
            / "testland"
        )
        self.notes.mkdir(parents=True)
        self.cases.mkdir(parents=True)

        (self.notes / "ts-law.md").write_text(
            "---\nsource_id: ts-law\n---\n# Test law\n", encoding="utf-8"
        )
        (self.notes / "source_notes_index.md").write_text(
            "# Source Notes Index\n", encoding="utf-8"
        )
        (self.raw / "source_inventory.md").write_text(
            "| 1 | Test law | https://example.gov/law | Authority | HTML | 是 | "
            "法规 | 可访问 | 可提取 | 否 | source_id: `ts-law`。 |\n",
            encoding="utf-8",
        )
        (self.raw / "evidence_matrix.md").write_text(
            VALID_MATRIX, encoding="utf-8"
        )
        (self.cases / "08_testland_regulations.md").write_text(
            VALID_CASE_08, encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_valid_matrix_passes(self) -> None:
        report = validate_evidence_matrix(self.root, "testland")
        self.assertTrue(report.ok, report.errors)
        self.assertEqual(report.metrics["evidence_items"], 1)

    def test_matrix_rejects_missing_required_field(self) -> None:
        matrix_path = self.raw / "evidence_matrix.md"
        matrix_path.write_text(
            VALID_MATRIX.replace("**不能支持**", "**其他说明**"),
            encoding="utf-8",
        )
        report = validate_evidence_matrix(self.root, "testland")
        self.assertFalse(report.ok)
        self.assertTrue(
            any("字段 不能支持" in error for error in report.errors)
        )

    def test_matrix_rejects_unaccounted_source_note(self) -> None:
        (self.notes / "ts-unused.md").write_text(
            "---\nsource_id: ts-unused\n---\n# Unused\n", encoding="utf-8"
        )
        inventory_path = self.raw / "source_inventory.md"
        inventory_path.write_text(
            inventory_path.read_text(encoding="utf-8")
            + "| 2 | Unused | https://example.gov/unused | Authority | HTML | 是 | "
            "法规 | 可访问 | 可提取 | 否 | source_id: `ts-unused`。 |\n",
            encoding="utf-8",
        )
        matrix_path = self.raw / "evidence_matrix.md"
        matrix_path.write_text(
            VALID_MATRIX.replace(
                "**已读取 Source Notes**：`1`",
                "**已读取 Source Notes**：`2`",
            ),
            encoding="utf-8",
        )
        report = validate_evidence_matrix(self.root, "testland")
        self.assertFalse(report.ok)
        self.assertTrue(
            any("未被证据使用" in error for error in report.errors)
        )

    def test_valid_regulations_case_passes(self) -> None:
        report = validate_cases(self.root, "testland", ["08"])
        self.assertTrue(report.ok, report.errors)
        self.assertEqual(report.metrics["traced_evidence_items"], 1)

    def test_case_rejects_broken_wikilink(self) -> None:
        case_path = self.cases / "08_testland_regulations.md"
        case_path.write_text(
            VALID_CASE_08 + "\n- [[missing-note]]\n", encoding="utf-8"
        )
        report = validate_cases(self.root, "testland", ["08"])
        self.assertFalse(report.ok)
        self.assertTrue(
            any("链接目标不存在" in error for error in report.errors)
        )

    def test_case_rejects_missing_required_section(self) -> None:
        case_path = self.cases / "08_testland_regulations.md"
        case_path.write_text(
            VALID_CASE_08.replace(
                "## 7. 仍需补充的官方文件",
                "## 7. 后续事项",
            ),
            encoding="utf-8",
        )
        report = validate_cases(self.root, "testland", ["08"])
        self.assertFalse(report.ok)
        self.assertTrue(
            any("仍需补充的官方文件" in error for error in report.errors)
        )


if __name__ == "__main__":
    unittest.main()
