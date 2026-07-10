# Article Page Template — Radio Regulations 2020

Each article page follows this template.

## Template

```markdown
---
article_id: <article_id>
chapter: <chapter_number>
title_zh: <中文标题>
title_en: <English title>
pages: <start_page>–<end_page>
wrc_sources: [<WRC-XX>, ...]
keywords: [<keyword1>, <keyword2>, ...]
---

# 第<N>条 — <标题>

## 一句话摘要

<1–2 sentence summary of the article's purpose and main provisions>

## 关键词

- <keyword1>
- <keyword2>
- ...

## 交叉引用

| 引用来源 | 目标条款 | 状态 |
|----------|----------|------|
| 第N条第X款 | [[art_MM]] | ✅ 已链接 / ⚠️ 待确认 |

## 原文

<Full OCR-extracted text of the article, verbatim>

---

*Source: Radio Regulations 2020 (Chinese edition), ITU*
*Last updated: <date>*
*Extraction method: OCR (EasyOCR)*
```

## Field Definitions

| Field | Required | Description |
|-------|----------|-------------|
| `article_id` | ✅ | e.g., `art_01`, `art_29A` |
| `chapter` | ✅ | Chapter number (1–10) |
| `title_zh` | ✅ | Chinese title from the official text |
| `title_en` | ⚠️ | English title if available (from ITU English edition) |
| `pages` | ✅ | Page range in the source PDF |
| `wrc_sources` | ⚠️ | WRC conferences that adopted/amended this article |
| `keywords` | ✅ | Relevant keywords for topic indexing |
| 一句话摘要 | ✅ | Mandatory — max 2 sentences |
| 关键词 | ✅ | At least 3 keywords |
| 交叉引用 | ⚠️ | May be empty if no cross-references found |
| 原文 | ✅ | Full verbatim text — never summarize or paraphrase |

## Notes

- The **原文** section MUST contain the FULL text of the article, not a summary
- OCR extraction errors should be noted with `[OCR: unclear]` markers where confidence is low
- WRC source notes (出现在条款开头的方括号文字，如 [WRC-19]）should be preserved verbatim
- Line breaks within the original text should be preserved where they aid readability
