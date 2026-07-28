from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from landing_rights_agent.case_data import (
    constrain_machine_case_data,
    parse_case_data,
    validate_case_data,
)
from landing_rights_agent.client import AgentAPIError, ResponsesClient, extract_output_text
from landing_rights_agent.knowledge import (
    ContextDocument,
    KnowledgeBaseError,
    build_file_documents,
    require_source_notes,
    render_context,
    validate_country_slug,
)
from landing_rights_agent.validation import (
    GeneratedFileError,
    strip_markdown_fence,
    validate_case_markdown,
)
from landing_rights_agent.workflows import build_country_cases


class ClientTests(unittest.TestCase):
    def test_ollama_from_env_does_not_require_api_key(self) -> None:
        with patch.dict(
            "os.environ",
            {"LANDING_RIGHTS_PROVIDER": "ollama"},
            clear=True,
        ):
            client = ResponsesClient.from_env()
        self.assertEqual(client.provider, "ollama")
        self.assertEqual(client.api_key, "ollama")
        self.assertEqual(client.model, "landing-rights-qwen3.5:9b")
        self.assertEqual(client.base_url, "http://127.0.0.1:11434/v1")

    def test_ollama_payload_uses_supported_response_fields(self) -> None:
        client = ResponsesClient(
            api_key="ollama",
            provider="ollama",
            model="qwen3:8b",
            base_url="http://127.0.0.1:11434/v1",
        )
        payload = client.build_payload(
            instructions="rules",
            input_text="question",
        )
        self.assertEqual(
            payload,
            {
                "model": "qwen3:8b",
                "instructions": "rules",
                "input": "question",
            },
        )

    def test_ollama_rejects_web_search(self) -> None:
        client = ResponsesClient(api_key="ollama", provider="ollama")
        with self.assertRaises(AgentAPIError):
            client.build_payload(
                instructions="rules",
                input_text="question",
                web_search=True,
            )

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

    def test_extract_output_text_from_function_arguments(self) -> None:
        response = {
            "output": [
                {
                    "type": "function_call",
                    "name": "submit_case_data",
                    "arguments": '{"title":"测试"}',
                }
            ]
        }
        self.assertEqual(extract_output_text(response), '{"title":"测试"}')

    def test_qwen_structured_payload_uses_required_function(self) -> None:
        client = ResponsesClient(api_key="secret", provider="qwen")
        schema = {
            "type": "object",
            "properties": {"title": {"type": "string"}},
            "required": ["title"],
        }
        payload = client.build_payload(
            instructions="rules",
            input_text="data",
            output_schema=schema,
        )
        self.assertEqual(payload["tool_choice"], "required")
        self.assertEqual(payload["tools"][0]["type"], "function")
        self.assertEqual(payload["tools"][0]["parameters"], schema)
        self.assertEqual(payload["reasoning"], {"effort": "none"})
        self.assertEqual(payload["temperature"], 0)

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

    def test_build_file_documents_use_minimal_relevant_context(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            common = root / "wiki/concepts/landing_rights/common"
            common.mkdir(parents=True)
            for name in (
                "country_landing_rights_sop.md",
                "source_priority_rules.md",
                "open_questions_template.md",
                "md_file_format_rules.md",
            ):
                (common / name).write_text(f"# {name}\n", encoding="utf-8")

            raw = root / "wiki/raw/landing_rights/test"
            notes = raw / "source_notes"
            notes.mkdir(parents=True)
            (raw / "source_inventory.md").write_text("# Inventory\n", encoding="utf-8")
            (notes / "source_notes_index.md").write_text("# Index\n", encoding="utf-8")
            (notes / "equipment.md").write_text(
                "设备 合格证 认证 EMC RF 测试报告\n", encoding="utf-8"
            )
            (notes / "investment.md").write_text(
                "外国 投资 本地主体 市场准入\n", encoding="utf-8"
            )
            (notes / "frequency.md").write_text(
                "无线电频率 频段 ITU 干扰协调\n", encoding="utf-8"
            )

            brazil = root / "wiki/concepts/landing_rights/cases/brazil"
            brazil.mkdir(parents=True)
            (brazil / "04_brazil_frequency_coordination.md").write_text(
                "# Brazil frequency structure\n", encoding="utf-8"
            )
            (brazil / "05_brazil_equipment_certification.md").write_text(
                "# Brazil equipment structure\n", encoding="utf-8"
            )
            old_cases = root / "wiki/concepts/landing_rights/cases/test"
            old_cases.mkdir(parents=True)
            (old_cases / "05_test_equipment_certification.md").write_text(
                "# Old generated case\n", encoding="utf-8"
            )
            (root / "AGENTS.md").write_text("# Private project rules\n", encoding="utf-8")

            documents = build_file_documents(root, "test", number="05")
            paths = {document.path.as_posix() for document in documents}
            self.assertIn("wiki/raw/landing_rights/test/source_notes/equipment.md", paths)
            self.assertNotIn("wiki/raw/landing_rights/test/source_notes/investment.md", paths)
            self.assertNotIn("wiki/raw/landing_rights/test/source_notes/frequency.md", paths)
            self.assertIn(
                "wiki/concepts/landing_rights/cases/brazil/05_brazil_equipment_certification.md",
                paths,
            )
            self.assertNotIn(
                "wiki/concepts/landing_rights/cases/brazil/04_brazil_frequency_coordination.md",
                paths,
            )
            self.assertNotIn("AGENTS.md", paths)
            self.assertFalse(any("cases/test" in path for path in paths))

    def test_build_file_documents_keep_multiple_required_notes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            common = root / "wiki/concepts/landing_rights/common"
            common.mkdir(parents=True)
            for name in (
                "country_landing_rights_sop.md",
                "source_priority_rules.md",
                "open_questions_template.md",
            ):
                (common / name).write_text(f"# {name}\n", encoding="utf-8")

            notes = root / "wiki/raw/landing_rights/test/source_notes"
            notes.mkdir(parents=True)
            for stem in (
                "br-anatel-collective-services",
                "br-res-720-2020",
                "br-res-777-2025",
            ):
                (notes / f"{stem}.md").write_text(
                    "服务授权 集体利益服务 服务通知\n",
                    encoding="utf-8",
                )

            brazil = root / "wiki/concepts/landing_rights/cases/brazil"
            brazil.mkdir(parents=True)
            (brazil / "03_brazil_service_authorization.md").write_text(
                "# Brazil service structure\n",
                encoding="utf-8",
            )

            documents = build_file_documents(root, "test", number="03")
            paths = {document.path.as_posix() for document in documents}
            for stem in (
                "br-anatel-collective-services",
                "br-res-720-2020",
                "br-res-777-2025",
            ):
                self.assertIn(
                    f"wiki/raw/landing_rights/test/source_notes/{stem}.md",
                    paths,
                )

    def test_brazil_fee_context_keeps_each_required_official_note(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            common = root / "wiki/concepts/landing_rights/common"
            common.mkdir(parents=True)
            for name in (
                "country_landing_rights_sop.md",
                "source_priority_rules.md",
                "open_questions_template.md",
            ):
                (common / name).write_text(f"# {name}\n", encoding="utf-8")

            notes = root / "wiki/raw/landing_rights/brazil/source_notes"
            notes.mkdir(parents=True)
            required = (
                "br-res-748-2021",
                "br-anatel-satellite-rights-page",
                "br-anatel-collective-services",
                "br-law-5070-1966",
            )
            for stem in required:
                (notes / f"{stem}.md").write_text(
                    "费用 收费 费率 权利费 服务费\n",
                    encoding="utf-8",
                )
            (notes / "decoy-fee-note.md").write_text(
                ("费用 收费 费率 " * 20) + "\n",
                encoding="utf-8",
            )

            brazil = root / "wiki/concepts/landing_rights/cases/brazil"
            brazil.mkdir(parents=True)
            (brazil / "07_brazil_fee_list.md").write_text(
                "# Brazil fee structure\n",
                encoding="utf-8",
            )

            documents = build_file_documents(root, "brazil", number="07")
            paths = {document.path.as_posix() for document in documents}
            for stem in required:
                self.assertIn(
                    f"wiki/raw/landing_rights/brazil/source_notes/{stem}.md",
                    paths,
                )


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

- 这是已确认信息（依据：source-0）。""" + ("内容" * 260) + """

### 2.2 分析推断

- 这是审慎的分析推断（推断依据：source-0）。

### 2.3 待确认事项

- 这是待确认事项。

## 3. 许可框架

- 已确认的许可框架（依据：source-0）。

## 4. 申请主体

- 申请主体仍有事项待确认。

## 5. 申请材料

- 已确认的申请材料（依据：source-0）。

## 6. 审批流程

- 审批流程仍有事项待确认。

## 7. 风险与下一步

- 待确认：实际执行口径。

## 8. 官方来源

- [官方来源](https://example.gov/)

## 9. 相关文件

- [[00_test_case_index|案例索引]]
"""
        self.assertEqual(validate_case_markdown(content, number="01"), [])

    def test_missing_numbered_sections_are_rejected(self) -> None:
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

内容。

## 2. 结论摘要

### 2.1 已确认信息

- 已确认（依据：source-0）。

### 2.2 分析推断

- 可能需要进一步核查（推断依据：source-0）。

### 2.3 待确认事项

- 待确认。

## 8. 官方来源

- https://example.gov/

## 9. 相关文件

- [[00_test_case_index]]
""" + ("内容" * 260)
        errors = validate_case_markdown(content, number="01")
        self.assertTrue(any("连续编号章节" in error for error in errors))

    def test_missing_evidence_marker_is_rejected(self) -> None:
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

内容。

## 2. 结论摘要

### 2.1 已确认信息

- 没有证据标记的结论。

### 2.2 分析推断

- 没有推断依据的分析。

### 2.3 待确认事项

- 待确认。

## 3. 许可框架

- 已确认的许可框架（依据：source-0）。

## 4. 申请主体

- 申请主体仍有事项待确认。

## 5. 申请材料

- 已确认的申请材料（依据：source-0）。

## 6. 审批流程

- 审批流程仍有事项待确认。

## 7. 风险与下一步

- 待确认：实际执行口径。

## 8. 官方来源

- https://example.gov/

## 9. 相关文件

- [[00_test_case_index]]
""" + ("内容" * 260)
        errors = validate_case_markdown(content, number="01")
        self.assertTrue(any("每条“已确认信息”" in error for error in errors))
        self.assertTrue(any("每条“分析推断”" in error for error in errors))

    def test_unclosed_front_matter_is_rejected(self) -> None:
        content = """---
country: Test
topic: overview
case_type: structured_case
source_document: official_sources
language: zh-CN
review_status: draft

# 测试标题

## 1. 文件用途

## 2. 结论摘要

## 3. 官方来源

## 4. 相关文件
""" + ("内容" * 300)
        errors = validate_case_markdown(content, number="01")
        self.assertTrue(any("未正确闭合" in error for error in errors))


class CaseDataTests(unittest.TestCase):
    def _data(self, quote: str = "卫星通信网络 许可组合") -> str:
        value = {
            "title": "测试案例",
            "purpose": "测试结构化案例。",
            "confirmed": [
                {
                    "text": "官方资料记录了卫星通信网络许可组合。",
                    "source_id": "source-0",
                    "evidence_quote": quote,
                }
            ],
            "inferences": [],
            "pending": ["执行口径待确认。"],
            "sections": [
                {
                    "number": number,
                    "heading": "测试章节",
                    "items": [
                        {
                            "status": "confirmed",
                            "text": "官方资料记录了许可组合。",
                            "source_id": "source-0",
                            "evidence_quote": quote,
                        }
                    ],
                }
                for number in range(3, 8)
            ],
            "sources": [
                {
                    "label": "监管机构",
                    "url": "https://regulator.example.gov/",
                }
            ],
            "related_files": ["00_test_case_index.md"],
        }
        return json.dumps(value, ensure_ascii=False)

    def test_exact_evidence_quote_is_required(self) -> None:
        data = parse_case_data(self._data("来源中不存在的摘录"))
        documents = [
            ContextDocument(
                path=Path(
                    "wiki/raw/landing_rights/test/source_notes/source-0.md"
                ),
                content=(
                    "source_id: source-0\n"
                    "卫星通信网络 许可组合\n"
                    "https://regulator.example.gov/\n"
                ),
            )
        ]
        with self.assertRaises(GeneratedFileError):
            validate_case_data(
                data,
                documents=documents,
                allowed_related_files=["00_test_case_index.md"],
            )

    def test_markdown_table_separator_is_ignored_for_evidence(self) -> None:
        quote = "第 6.1 至 6.3 条：CRC 负责 ITU 登记与干扰协调"
        data = parse_case_data(self._data(quote))
        documents = [
            ContextDocument(
                path=Path(
                    "wiki/raw/landing_rights/test/source_notes/source-0.md"
                ),
                content=(
                    "source_id: source-0\n"
                    "| 条款 | 内容 |\n"
                    "| 第 6.1 至 6.3 条 | CRC 负责 ITU 登记与干扰协调 |\n"
                    "https://regulator.example.gov/\n"
                ),
            )
        ]
        validate_case_data(
            data,
            documents=documents,
            allowed_related_files=["00_test_case_index.md"],
        )

    def test_two_adjacent_source_lines_can_form_one_evidence_quote(self) -> None:
        quote = "第 9.8 项：频率许可。第 9.10 项：卫星网络许可。"
        data = parse_case_data(self._data(quote))
        documents = [
            ContextDocument(
                path=Path(
                    "wiki/raw/landing_rights/test/source_notes/source-0.md"
                ),
                content=(
                    "source_id: source-0\n"
                    "| 第 9.8 项 | 频率许可。 |\n"
                    "| 第 9.10 项 | 卫星网络许可。 |\n"
                    "https://regulator.example.gov/\n"
                ),
            )
        ]
        validate_case_data(
            data,
            documents=documents,
            allowed_related_files=["00_test_case_index.md"],
        )

    def test_structured_schema_requires_five_sections(self) -> None:
        from landing_rights_agent.case_data import CASE_DATA_SCHEMA

        sections_schema = CASE_DATA_SCHEMA["properties"]["sections"]
        self.assertEqual(sections_schema["minItems"], 5)
        self.assertEqual(sections_schema["maxItems"], 5)
        self.assertEqual(
            CASE_DATA_SCHEMA["properties"]["inferences"]["maxItems"],
            0,
        )
        status_schema = sections_schema["items"]["properties"]["items"][
            "items"
        ]["properties"]["status"]
        self.assertEqual(status_schema["enum"], ["confirmed", "pending"])

    def test_machine_constraint_removes_free_inferences(self) -> None:
        value = json.loads(self._data())
        value["inferences"] = [
            {
                "text": "初步判断来源未确认的结论。",
                "source_id": "source-0",
                "evidence_quote": "卫星通信网络 许可组合",
            }
        ]
        value["sections"][0]["items"] = [
            {
                "status": "inference",
                "text": "可能存在来源未确认的程序。",
                "source_id": "source-0",
                "evidence_quote": "卫星通信网络 许可组合",
            }
        ]
        constrained = constrain_machine_case_data(
            parse_case_data(json.dumps(value, ensure_ascii=False))
        )
        self.assertEqual(constrained.inferences, ())
        self.assertEqual(constrained.sections[0].items[0].status, "pending")
        self.assertIn("人工复核", constrained.sections[0].items[0].text)

    def test_machine_constraint_filters_unknown_pending_tokens(self) -> None:
        value = json.loads(self._data())
        value["pending"].append("SMSS 第 99 条是否适用？")
        documents = [
            ContextDocument(
                path=Path(
                    "wiki/raw/landing_rights/test/source_notes/source-0.md"
                ),
                content="卫星通信网络 许可组合\n",
            )
        ]
        constrained = constrain_machine_case_data(
            parse_case_data(json.dumps(value, ensure_ascii=False)),
            documents=documents,
        )
        self.assertEqual(constrained.pending, ("执行口径待确认。",))

    def test_empty_section_pending_text_gets_safe_fallback(self) -> None:
        value = json.loads(self._data())
        value["sections"][0]["items"] = [
            {
                "status": "pending",
                "text": "",
                "source_id": "",
                "evidence_quote": "",
            }
        ]
        parsed = parse_case_data(json.dumps(value, ensure_ascii=False))
        item = parsed.sections[0].items[0]
        self.assertEqual(item.status, "pending")
        self.assertIn("人工复核", item.text)

    def test_empty_confirmed_text_falls_back_to_evidence_quote(self) -> None:
        value = json.loads(self._data())
        value["confirmed"][0]["text"] = ""
        parsed = parse_case_data(json.dumps(value, ensure_ascii=False))
        self.assertEqual(
            parsed.confirmed[0].text,
            parsed.confirmed[0].evidence_quote,
        )


class FakeClient:
    def create(
        self,
        *,
        instructions: str,
        input_text: str,
        web_search: bool = False,
        output_schema: dict | None = None,
    ) -> str:
        self.assert_is_structured(output_schema)
        data = {
            "title": "测试落地许可总览",
            "purpose": "本文件用于验证 Agent 从 source notes 生成案例预览的完整执行路径。",
            "confirmed": [
                {
                    "text": "测试来源确认卫星通信网络许可组合。",
                    "source_id": "source-0",
                    "evidence_quote": "卫星通信网络 许可组合",
                }
            ],
            "inferences": [],
            "pending": ["实际申请口径仍需向监管机构确认。"],
            "sections": [
                {
                    "number": number,
                    "heading": heading,
                    "items": [
                        {
                            "status": "confirmed",
                            "text": "测试来源支持本节结论。",
                            "source_id": "source-0",
                            "evidence_quote": "卫星通信网络 许可组合",
                        }
                    ],
                }
                for number, heading in (
                    (3, "许可框架"),
                    (4, "申请主体"),
                    (5, "申请材料"),
                    (6, "审批流程"),
                    (7, "风险与下一步"),
                )
            ],
            "sources": [
                {
                    "label": "测试监管机构",
                    "url": "https://regulator.example.gov/",
                }
            ],
            "related_files": ["00_test_case_index.md"],
        }
        return json.dumps(data, ensure_ascii=False)

    def assert_is_structured(self, output_schema: dict | None) -> None:
        if output_schema is None:
            raise AssertionError("workflow did not request structured output")


class RetryingFakeClient(FakeClient):
    def __init__(self) -> None:
        self.calls = 0

    def create(
        self,
        *,
        instructions: str,
        input_text: str,
        web_search: bool = False,
        output_schema: dict | None = None,
    ) -> str:
        self.calls += 1
        raw = super().create(
            instructions=instructions,
            input_text=input_text,
            web_search=web_search,
            output_schema=output_schema,
        )
        if self.calls == 1:
            value = json.loads(raw)
            value["confirmed"][0]["evidence_quote"] = "来源中不存在的摘录"
            return json.dumps(value, ensure_ascii=False)
        return raw


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
                    f"# Official source {index}\n"
                    "卫星通信网络 许可组合\n"
                    "https://regulator.example.gov/\n",
                    encoding="utf-8",
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
            rendered = (
                preview_dir / "01_test_landing_overview.md"
            ).read_text(encoding="utf-8")
            self.assertIn("卫星通信网络 许可组合", rendered)
            self.assertNotIn("测试来源确认卫星通信网络许可组合", rendered)
            self.assertIn("review_status: machine_generated", rendered)
            self.assertTrue(
                (preview_dir / "01_test_landing_overview.case-data.json").exists()
            )
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

    def test_build_retries_once_after_evidence_failure(self) -> None:
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
                    f"# Official source {index}\n"
                    "卫星通信网络 许可组合\n"
                    "https://regulator.example.gov/\n",
                    encoding="utf-8",
                )

            client = RetryingFakeClient()
            preview_dir, generated = build_country_cases(
                client,
                root=root,
                country="test",
                numbers=["01"],
                preview_root=root / "preview-retry",
            )
            self.assertEqual(client.calls, 2)
            self.assertEqual(len(generated), 1)
            self.assertTrue(
                (
                    preview_dir
                    / "01_test_landing_overview.case-data.attempt-1.json"
                ).exists()
            )
            self.assertTrue(
                (
                    preview_dir
                    / "01_test_landing_overview.case-data.attempt-2.json"
                ).exists()
            )


if __name__ == "__main__":
    unittest.main()
