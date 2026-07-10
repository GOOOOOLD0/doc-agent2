# Parse Notes — Radio Regulations 2020

**File:** `wiki/raw/regulations/radio_regulations_2020/parse_notes.md`

---

## 1. Text Extraction Status

| Method | Status | Quality |
|--------|--------|---------|
| PDF Bookmarks (TOC) | ✅ Success | Full chapter/article tree with page numbers |
| pdftotext (xpdf 4.00 -layout) | ⚠️ Partial | 18,891 lines extracted but Chinese characters garbled (font encoding issue) |
| PyMuPDF (fitz 1.27.2) | ⚠️ Partial | Font `SimSun-GBK-EUC-H` / `SimHei-GBK-EUC-H` not mapped — garbled Unicode output |
| pdfminer.six | ⚠️ Partial | Outputs CID codes `(cid:xxxx)` — CMap `UniGB-UTF16-H` missing |
| EasyOCR (CPU, DPI 200) | ✅ Good | ~2.3s/page, accurate Chinese recognition on test pages |

## 2. Font Encoding Issue

**Root cause:** The PDF uses legacy GBK-EUC-H encoded fonts:
- `SimSun-GBK-EUC-H`
- `SimHei-GBK-EUC-H`

The CMap file `UniGB-UTF16-H` that maps GBK-EUC font encoding to Unicode UTF-16 is missing from the system. Neither xpdf 4.00, poppler, nor MuPDF can decode the Chinese text without this mapping. pdfminer.six also lacks the CJK CMap resource.

**Data loss:** pdftotext extracted ~18,891 lines but with garbled characters. The structural layout (line breaks, paragraphs) is preserved, but the Chinese text content itself is unreadable programmatically.

## 3. Resolution

**EasyOCR** was successfully tested on the Table of Contents page (~2.3s, accurate recognition). OCR approach is feasible but requires:

- Page-by-page rendering via PyMuPDF at DPI 200
- ~2–3 seconds per page on CPU (total ~15–20 min for 442 pages)
- GPU would reduce this significantly

**Plan for full text extraction:**
1. Render each page as PNG via PyMuPDF at 200 DPI
2. OCR with EasyOCR `['ch_sim', 'en']` mode
3. Save per-page OCR text
4. Assemble into article-level text chunks guided by structure.md

## 4. OCR Verification

| Test Page | OCR Lines | Quality |
|-----------|-----------|---------|
| Page 7 (Table of Contents) | 53 lines | ✅ All chapter/article titles correctly recognized |
| Page 14 (Preface) | 2 lines | ⚠️ Near-blank/transition page |

## 5. Known Issues

1. **OCR failure modes:** Tables, diagrams, footnotes, and small-print annotations may have reduced accuracy
2. **Frequency allocation table (第5条):** Pages 45–196 contain detailed frequency allocation tables — these will require post-OCR validation
3. **Bookmarks source:** All bookmark titles were manually verified against the Table of Contents page (OCR-confirmed)
4. **Article 10:** Marked as "（此号未使用）" (this number not used) — confirmed by both bookmarks and TOC
5. **Blank/transition pages:** Some transition pages between chapters appear blank — these are retained in the page count but contain no substantive content

## 6. Recommendations

- Run full OCR batch to extract all 442 pages into per-article text files
- Validate frequency allocation tables (第5条) against the ITU original English edition
- Consider manual spot-check of ~20 random pages to verify OCR accuracy
- Install GPU acceleration for future batch OCR work
