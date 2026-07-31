"""Step 3a: Apply mechanical_clean to all chunk files for articles 1-5."""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.book_ingestion.optimize_wiki_pages import mechanical_clean

chunks_dir = project_root / 'wiki' / 'raw' / 'radio_rules' / 'itu_radio_regulations_2020' / 'chunks'

preserve = {
    "pdf_page": True,
    "page_label": True,
    "article_number": True,
    "clause_number": True,
    "tables": True,
    "footnotes": True,
    "cross_references": True,
    "wrc_revision": True,
}

# Collect chunk files for articles 1-5 only
chunk_files = []
for article_dir in sorted(chunks_dir.iterdir()):
    if not article_dir.is_dir():
        continue
    name = article_dir.name
    if not name.startswith('article_'):
        continue
    # Extract article number
    suffix = name.replace('article_', '')
    try:
        num = int(suffix)
    except ValueError:
        continue
    if num > 5:
        continue
    for f in sorted(article_dir.rglob('*.md')):
        chunk_files.append((f, name))

total_files = len(chunk_files)
total_stats = {"dedup": 0, "garbage": 0, "ocr_fix": 0, "xref": 0, "junk": 0}

print(f"Processing {total_files} chunk files...")

for i, (fpath, dirname) in enumerate(chunk_files):
    content = fpath.read_text(encoding='utf-8')

    # Separate frontmatter from body
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        print(f"  SKIP {fpath.name}: no frontmatter")
        continue

    frontmatter = parts[1]
    body = parts[2] if len(parts) > 2 else ''

    article_id = dirname.replace('article_', '')

    cleaned_body, stats = mechanical_clean(
        body, article_id, 'radio_rules', set(),
        inject_wikilinks=False, preserve=preserve
    )

    for k in total_stats:
        total_stats[k] += stats.get(k, 0)

    new_content = f'---\n{frontmatter}---\n\n{cleaned_body}\n'
    fpath.write_text(new_content, encoding='utf-8')

    if (i + 1) % 20 == 0 or (i + 1) == total_files:
        print(f"  [{i+1}/{total_files}] {fpath.relative_to(chunks_dir)}")

print(f"\nDone! Processed {total_files} files.")
print(f"Stats: {total_stats}")
