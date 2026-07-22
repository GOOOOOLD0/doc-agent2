from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from landing_rights_agent.client import ResponsesClient, extract_output_text
from landing_rights_agent.knowledge import (
    KnowledgeBaseError,
    require_source_notes,
    render_context,
    validate_country_slug,
)
from landing_rights_agent.validation import (
    strip_markdown_fence,
    validate_case_markdown,
)
from landing_rights_agent.workflows import build_country_cases


class ClientTests(unittest.TestCase):
    def test_extract_output_text_from_response_items(self) -> None:
        response = {
            "output": [
                {
                    "type": "message",
                    "content": [{"type": "output_text", "text": "结论"}],
                }
            ]
        }
        self.assertEqual(extract_output_text(response), "结论")

    def test_web_search_payload(self) -> None:
        client = ResponsesClient(api_key="test", model="test-model")
        payload = client.build_payload(
            instructions="rules", input_text="question", web_search=True
        )
        self.assertEqual(payload["model"], "test-model")
        self.assertEqual(payload["tools"][0]["type"], "web_search")
        self.assertEqual(len(payload["tools"]), 1)
        self.assertEqual(payload["tool_choice"], "required")
        self.assertEqual(payload["reasoning"]["effort"], "none")
        self.assertFalse(payload["store"])

    def test_openai_web_search_payload(self) -> None:
        client = ResponsesClient(
            api_key="test",
            provider="openai",
            model="test-model",
            base_url="https://api.openai.com/v1",
        )
        payload = client.build_payload(
            instructions="rules", input_text="question", web_search=True
        )
        self.assertEqual(len(payload["tools"]), 1)
        self.assertEqual(payload["tools"][0]["search_context_size"], "high")
        self.assertIn("text", payload)

    def test_extract_output_text_appends_web_sources(self) -> None:
        response = {
            "output_text": (
                "研究结论：[监管机构](https://regulator.example.gov/)"
            ),
            "x_tools": {"web_search": {"count": 1}},
            "output": [
                {
                    "type": "web_search_call",
                    "action": {
                        "sources": [
                            {
                                "title": "Official regulator",
                                "url": "https://regulator.example.gov/",
                            }
                        ]
                    },
                }
            ],
        }
        result = extract_output_text(response)
        self.assertIn("研究结论", result)
        self.assertIn("https://regulator.example.gov/", result)
        self.assertIn("正文实际引用的 API 搜索来源", result)
        self.assertIn("API 搜索调用次数：1", result)
        self.assertIn("正文实际引用其中：1 个", result)

    def test_search_appendix_excludes_uncited_results(self) -> None:
        response = {
            "output_text": "研究结论",
            "output": [
                {
                    "type": "web_search_call",
                    "action": {
                        "sources": [
                            {
                                "title": "Unrelated result",
                                "url": "https://unrelated.example/",
                            }
                        ]
                    },
                }
            ],
        }
        result = extract_output_text(response)
        self.assertNotIn("Unrelated result", result)
        self.assertIn("搜索返回 URL：1 个", result)
        self.assertIn("正文实际引用其中：0 个", result)


class KnowledgeTests(unittest.TestCase):
    def test_country_slug_normalization(self) -> None:
        self.assertEqual(validate_country_slug("South Africa"), "south_africa")

    def test_country_slug_rejects_paths(self) -> None:
        with self.assertRaises(KnowledgeBaseError):
            validate_country_slug("../../etc")

    def test_empty_context_is_explicit(self) -> None:
        self.assertIn("没有找到", render_context([]))

    def test_build_requires_evidence_layer(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(KnowledgeBaseError):
                require_source_notes(Path(temporary), "test")


class ValidationTests(unittest.TestCase):
    def test_strip_markdown_fence(self) -> None:
        self.assertEqual(strip_markdown_fence("```markdown\n# 标题\n```"), "# 标题")

    def test_valid_case_markdown(self) -> None:
        content = """---
country: Test
topic: overview
case_type: structured_case
source_document: official_sources
language: zh-CN
review_status: draft
---

# 测试落地许可

## 1. 文件用途

本文件用于测试完整的国家案例生成和校验流程，正文必须达到足够长度。

## 2. 结论摘要

### 2.1 已确认信息

这是已确认信息。""" + ("内容" * 260) + """

## 3. 官方来源

- [官方来源](https://example.gov/)

## 4. 相关文件

- [[00_test_case_index|案例索引]]
"""
        self.assertEqual(validate_case_markdown(content, number="01"), [])


class FakeClient:
    def create(
        self,
        *,
        instructions: str,
        input_text: str,
        web_search: bool = False,
    ) -> str:
        return """---
country: Test
topic: overview
case_type: structured_case
source_document: official_sources
language: zh-CN
review_status: draft
---

# 测试落地许可总览

## 1. 文件用途

本文件用于验证 Agent 从 source notes 生成案例预览的完整执行路径。

## 2. 结论摘要

### 2.1 已确认信息

这是基于官方来源形成的测试信息。""" + ("测试内容" * 180) + """

## 3. 官方来源

- [测试监管机构](https://regulator.example.gov/)

## 4. 相关文件

- [[00_test_case_index|案例索引]]
"""


class WorkflowTests(unittest.TestCase):
    def test_build_country_preview_and_apply(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
            common = root / "wiki/concepts/landing_rights/common"
            common.mkdir(parents=True)
            (common / "md_file_format_rules.md").write_text(
                "# Format\n", encoding="utf-8"
            )
            raw = root / "wiki/raw/landing_rights/test"
            notes = raw / "source_notes"
            notes.mkdir(parents=True)
            (raw / "source_inventory.md").write_text(
                "# Sources\n", encoding="utf-8"
            )
            for index in range(3):
                (notes / f"source-{index}.md").write_text(
                    f"# Official source {index}\n", encoding="utf-8"
                )

            preview_root = root / "preview"
            preview_dir, generated = build_country_cases(
                FakeClient(),
                root=root,
                country="test",
                numbers=["01"],
                preview_root=preview_root,
            )
            self.assertEqual(len(generated), 1)
            self.assertTrue((preview_dir / "01_test_landing_overview.md").exists())
            target = root / "wiki/concepts/landing_rights/cases/test"
            self.assertFalse(target.exists())

            build_country_cases(
                FakeClient(),
                root=root,
                country="test",
                numbers=["01"],
                apply=True,
                preview_root=root / "preview-apply",
            )
            self.assertTrue((target / "01_test_landing_overview.md").exists())


if __name__ == "__main__":
    unittest.main()
