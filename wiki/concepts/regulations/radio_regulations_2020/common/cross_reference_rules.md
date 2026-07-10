# Cross-Reference Rules — Radio Regulations 2020

## 1. Reference Patterns to Detect

The Radio Regulations use several standard cross-reference patterns in Chinese:

| Pattern | Example | Internal Link |
|---------|---------|---------------|
| `第N条` | `按第9条的规定` | `[[art_09]]` |
| `第N条第M款` | `第11条第2款` | `[[art_11#§2]]` |
| `第N章` | `依照第五章的规定` | (link to chapter index) |
| `附件N` | `见附件1` | (external annex reference) |
| `附录N` | `按照附录15` | (appendix reference) |
| `Resolution N` / `第N号决议` | `按第49号决议` | (resolution reference) |
| `WRC-XX` | `WRC-19修改` | (conference source note) |
| `《无线电规则》` | `根据《无线电规则》` | (self-reference) |
| `RR N.N` | `RR 5.150` | (ITU standard notation) |

## 2. Mapping Rules

| Source Text | Target Article ID | Notes |
|-------------|-------------------|-------|
| 第1条 | `art_01` | |
| 第2条 | `art_02` | |
| ... | ... | |
| 第29A条 | `art_29A` | Note: no space between 29 and A |
| 第59条 | `art_59` | |

## 3. Unresolvable References

If a reference cannot be mapped to a known article (e.g., references to:
- Appendices not included in this PDF
- Resolutions (not articles)
- ITU-R Recommendations
- Other ITU documents

→ preserve the original reference text and mark with `[待链接: <original text>]`

## 4. Implementation

During article text processing:

1. Scan OCR text for all known reference patterns
2. For each match, resolve to the target article ID using the mapping table
3. If resolvable → wrap as `[[art_NN]]` wiki link
4. If NOT resolvable → add to article's "交叉引用" table with status ⚠️
5. If the same reference appears multiple times, link all occurrences

## 5. Special Cases

- **Self-references:** The document referring to itself as "本规则" or "《无线电规则》" is NOT a cross-reference — do not link
- **Article 10:** Marked as unused — references to Article 10 are likely errors or historical; flag with `[待确认: 第10条未使用]`
- **Frequency bands:** Frequency range references (e.g., "在 1–3 GHz 频段内") are NOT cross-references — do not link
