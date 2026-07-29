"""Final cleanup: inject section headers + clean trailing junk + cross-refs."""
import re, sys

TOPIC = "radio_rules"

def clean_page(aid, related_ids):
    path = f"wiki/concepts/radio_rules/{aid}.md"
    with open(path, encoding='utf-8') as f:
        text = f.read()

    # Locate core content
    core_start = text.find("## 核心内容")
    key_start = text.find("## 关键条款 / 关键观点")
    if core_start < 0:
        return
    before = text[:core_start]
    after = text[key_start:] if key_start >= 0 else ""

    # Read raw chunks
    raw_path = f"wiki/raw/radio_rules/itu_radio_regulations_2020/chunks/{aid}.txt"
    with open(raw_path, encoding='utf-8') as f:
        raw = f.read()

    # Normalize
    raw = raw.replace('\r\n', '\n').replace('\r', '\n')
    lines = raw.split('\n')

    # Filter and clean
    gset = {'人','米','米米','卜','eSt','豆','•','●','○','◎','※','~','…','"',"'",'C','G','('}
    ok = []
    for l in lines:
        s = l.strip()
        if not s: continue
        if s in gset: continue
        if re.match(r'^(---\s*page\s*\d+\s*---|RRI\d*|RR\d+[-–]\d+|RR\d+\s+\d+|RRI[Ll]|第[一二三四五六七八九十]+章[-–—])$', s): continue
        if re.match(r'^\d{1,3}$', s): continue
        if '阆' in s or re.match(r'^\d+@', s): continue
        ok.append(s)

    for old, new in [('笫','第'),('GH2','GHz'),('GHZ','GHz'),('MHZ','MHz'),('MIZ','MHz'),
                      ('KZ','kHz'),('kr','kHz'),('O00','000'),('O0O','000'),
                      ('WRC-IS','WRC-15'),('WRC-I9','WRC-19'),
                      ('困际','国际'),('太会','大会'),('己下定义','已下定义'),
                      ('第工节','第I节'),('第皿节','第IV节'),('三织法','组织法'),
                      ('IU-尽','ITU-R'),('ITU-尽','ITU-R')]:
        ok = [s.replace(old, new) for s in ok]
    ok = [re.sub(r'\s+', ' ', s.replace('\u3000', ' ')).strip() for s in ok]
    ok = [s for s in ok if s]

    # Dedup
    cpat = re.compile(r'^(\d+\.?\d*[A-Za-z]?)(?:\s+(.*))?$')
    dedup = []
    seen = {}
    for l in ok:
        m = cpat.match(l)
        if m:
            num = m.group(1)
            rest = (m.group(2) or '').strip()
            if num in seen and rest[:60] in seen[num]:
                continue
            seen[num] = rest
        dedup.append(l)

    # Clause grouping with section headers as standalone
    section_pat = re.compile(r'^第([IVXLCDM]+)节\s*[-–—]\s*(.*)')
    out = []
    cur = None
    buf = []

    def flush():
        nonlocal cur, buf, out
        if cur is not None:
            t = ' '.join(buf).strip()
            t = re.sub(r'\s+', ' ', t)
            # Clean trailing junk
            t = re.sub(r'\s+\d{1,3}\s+第[一二三四五六七八九十]+章\S*$', '', t)
            t = re.sub(r'_{4,}', '', t)
            t = re.sub(r'[\uf000-\uf8ff\u2000-\u2fff\ufff0-\uffff]', '', t)
            t = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', t)
            t = t.strip()
            if t:
                out.append(f"{cur} {t}")
            cur = None
            buf = []

    for l in dedup:
        sm = section_pat.match(l)
        if sm:
            flush()
            roman = sm.group(1)
            rest2 = sm.group(2).strip()
            out.append(f"第{roman}节 - {rest2}")
            continue
        m = cpat.match(l)
        if m:
            flush()
            cur = m.group(1)
            r2 = (m.group(2) or '').strip()
            if r2:
                buf.append(r2)
        else:
            if cur is not None:
                buf.append(l)
            else:
                out.append(l)
    flush()

    core = '\n'.join(out)

    # Cross-refs
    core = re.sub(r'(?<!\[\[)(?<!\|)第(\d+[A-Za-z]?)条(?!\])',
                  lambda m: m.group(0) if m.group(1) == aid
                  else f"[[concepts/{TOPIC}/{m.group(1)}|第{m.group(1)}条]]", core)
    core = re.sub(r'(?<!\[\[)(?<!\|)附录(\d+)(?!\])',
                  lambda m: f"[[concepts/{TOPIC}/appendix-{m.group(1)}|附录{m.group(1)}]]", core)
    core = re.sub(r'(?<!\[\[)(?<!\|)WRC[-–](\d+)(?!\])',
                  lambda m: f"[[concepts/{TOPIC}/wrc-{m.group(1)}|WRC-{m.group(1)}]]", core)

    # Spacing
    cs = re.compile(r'^\d+\.?\d*[A-Za-z]?\s')
    result = []
    prev = False
    for l in core.split('\n'):
        is_c = bool(cs.match(l))
        if is_c and prev:
            result.append('')
        result.append(l)
        prev = is_c
    core = '\n'.join(result)

    # Related docs
    related = '\n'.join(f"- [[concepts/{TOPIC}/{n}|第{n}条]]" for n in related_ids if str(n) != aid)
    after2 = after
    issues_idx = after2.find("## 争议")
    after2 = after2[issues_idx:] if issues_idx >= 0 else after2
    after2 = f"## 相关文档\n\n### 本文档内的其他条款\n\n{related}\n\n" + after2

    page = before + "## 核心内容\n\n" + core + "\n\n" + after2
    page = page.replace('\r\n', '\n')
    page = re.sub(r'(\^\[raw/[^\]]+\])\s*\n\s*\^\[raw/[^\]]+\]', r'\1', page)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(page)

    clauses = len(re.findall(r'^\d+\.\d+[A-Za-z]?\s', core, re.MULTILINE))
    sections = len(re.findall(r'^第[IVXLCDM]+节\s*[-–—]', core, re.MULTILINE))
    return clauses, sections

# Process all
for aid, rel in [("1",["2","3"]),("2",["1","3"]),("3",["1","2","16"])]:
    c, s = clean_page(aid, rel)
    print(f"第{aid}条: {c} clauses, {s} sections")

# Re-inject Article 2 table
with open("wiki/concepts/radio_rules/2.md", encoding='utf-8') as f:
    p2 = f.read()

table = """| 频段序号 | 符号 | 频率范围（下限除外，上限包括在内） | 相当于米制的细分 |
|----------|------|-----------------------------------|-----------------|
| 4 | VLF | 3至30 kHz | 万米波 |
| 5 | LF | 30至300 kHz | 千米波 |
| 6 | MF | 300至3 000 kHz | 百米波 |
| 7 | HF | 3至30 MHz | 十米波 |
| 8 | VHF | 30至300 MHz | 米波 |
| 9 | UHF | 300至3 000 MHz | 分米波 |
| 10 | SHF | 3至30 GHz | 厘米波 |
| 11 | EHF | 30至300 GHz | 毫米波 |
| 12 | — | 300至3 000 GHz | 丝米波 |"""

p2 = p2.replace(
    "以吉赫（GHz）表示。\n但是，如果遵守这些规定会导致严重困难，例如在进行频率通知及登记、频率表或有关事项时，则可做适当变通1。（[[concepts/radio_rules/wrc-15|WRC-15]]）\n\n注1",
    "以吉赫（GHz）表示。\n但是，如果遵守这些规定会导致严重困难，例如在进行频率通知及登记、频率表或有关事项时，则可做适当变通1。（[[concepts/radio_rules/wrc-15|WRC-15]]）\n\n" + table + "\n\n注1"
)

with open("wiki/concepts/radio_rules/2.md", 'w', encoding='utf-8') as f:
    f.write(p2)

print("第2条: table re-injected")
