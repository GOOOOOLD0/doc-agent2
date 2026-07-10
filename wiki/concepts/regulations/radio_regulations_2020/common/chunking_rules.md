# Chunking Rules — Radio Regulations 2020

## 1. Granularity

Each chunk (article page) corresponds to **one Article** (条) in the Radio Regulations.

## 2. Chunk Boundaries

### Primary boundary: Article number
- Each article starts at a clear `第N条` or `第NA条` heading
- An article ends at the next article heading, or at the chapter end

### Exception: 第5条 (Frequency Allocation Table)
- 第5条 spans pages 45–196 (152 pages), including the complete Frequency Allocation Table
- Sub-chunks: Section 5.1 (general provisions), followed by the allocation table itself
- The allocation table is treated as a single continuous chunk

### Exception: 第10条
- Marked as "（此号未使用）" — no content to chunk

## 3. Internal Structure Within an Article

Each article may contain:

1. **Preamble/WRC source notes** — paragraphs listing which WRC conference modified this article
2. **Main paragraphs** — numbered or lettered (e.g., §1, §2, §3 or A, B, C)
3. **Sub-paragraphs** — indented provisions (e.g., §1.1, §1.2)
4. **Tables** — may appear inline
5. **Footnotes** — appended at the end of the article or page bottom

## 4. OCR Chunking Strategy

Since text is extracted via OCR:

1. Process pages sequentially through the PDF
2. For each page, detect whether it contains an article heading (`第N条`)
3. When a new article heading is detected, finalize the previous article chunk
4. Accumulate OCR text into article buffers
5. Post-process: merge consecutive page chunks for the same article

## 5. Article Page File Naming

Format: `art_NN.md` where NN is the two-digit article number

| Article | Filename |
|---------|----------|
| 第1条 | `art_01.md` |
| 第2条 | `art_02.md` |
| ... | ... |
| 第29A条 | `art_29A.md` |
| 第59条 | `art_59.md` |

## 6. Cross-Article References

- References to other articles within the text (e.g., "见第9条") should be converted to internal wiki links: `[[art_09]]`
- Cannot resolve → mark as `[待链接: 原文引用文字]`
