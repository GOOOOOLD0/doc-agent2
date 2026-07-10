#!/c/Users/ld/.venv/Scripts/python
"""OCR chapter 1 of Radio Regulations 2020 to extract article text."""
import fitz
import easyocr
import os
import re
import time

PDF_PATH = r"wiki/raw/regulations/无线电规则-2020/source.pdf"
OUT_DIR = r"wiki/concepts/regulations/radio_regulations_2020/articles"

# Article definitions for Chapter 1 (from structure.md)
CHAPTER1_ARTICLES = [
    ("art_01", "第1条", 17, 34),   # pages 17-34
    ("art_02", "第2条", 35, 36),   # pages 35-36
    ("art_03", "第3条", 37, 38),   # pages 37-38
]

# Also extract articles from other key chapters for completeness
# Chapter 4 (Interference) - small, quick
CHAPTER4_ARTICLES = [
    ("art_15", "第15条", 247, 252),
    ("art_16", "第16条", 253, 254),
]

# Chapter 5 (Administrative) - small, relevant to landing rights
CHAPTER5_ARTICLES = [
    ("art_17", "第17条", 257, 258),
    ("art_18", "第18条", 259, 260),
    ("art_19", "第19条", 261, 272),
    ("art_20", "第20条", 273, 274),
]

ALL_ARTICLES = CHAPTER1_ARTICLES + CHAPTER4_ARTICLES + CHAPTER5_ARTICLES

doc = fitz.open(PDF_PATH)
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)

for art_id, art_title, start_p, end_p in ALL_ARTICLES:
    print(f"\n{'='*60}")
    print(f"Processing {art_id} ({art_title}) — pages {start_p}–{end_p}")
    print(f"{'='*60}")
    
    all_text = []
    page_count = end_p - start_p + 1
    
    for pgnum in range(start_p - 1, end_p):  # 0-indexed
        page = doc[pgnum]
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        
        # Save temp image for OCR
        temp_path = f"_temp_ocr_{art_id}.png"
        with open(temp_path, "wb") as f:
            f.write(img_bytes)
        
        t0 = time.time()
        result = reader.readtext(temp_path, detail=0)
        elapsed = time.time() - t0
        
        page_text = "\n".join(result)
        all_text.append(f"--- Page {pgnum+1} ---\n{page_text}")
        
        print(f"  Page {pgnum+1}/{end_p}: {len(page_text)} chars, {elapsed:.1f}s")
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    full_text = "\n\n".join(all_text)
    
    # Generate article page
    article_page = f"""---
article_id: {art_id}
chapter: {"1" if art_id in [a[0] for a in CHAPTER1_ARTICLES] else ("4" if art_id in [a[0] for a in CHAPTER4_ARTICLES] else "5")}
title_zh: {art_title}
pages: {start_p}–{end_p}
keywords: []
---

# {art_title}

## 原文

{full_text}

---

*Source: Radio Regulations 2020 (Chinese edition), ITU*
*Extraction method: OCR (EasyOCR, CPU, DPI 200)*
"""
    
    out_path = os.path.join(OUT_DIR, f"{art_id}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(article_page)
    print(f"  ✅ Saved to {out_path}")

doc.close()
print(f"\n✅ Chapter extraction complete!")
