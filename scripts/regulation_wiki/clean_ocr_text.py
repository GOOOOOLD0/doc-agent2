"""
clean_ocr_text.py (v2)

相对上一版的改动:去掉了写死的错字字典(ocr_correction_dictionary.json)
和基于字典的错字标记逻辑。原因:错字模式因文档、因OCR引擎而异,一个
固定字典只能覆盖"见过的"错误,新文档换一批完全不同的错字就失效了,
维护成本会一直增加。这类"要不要判断某个字符是不是识别错了"本质上
需要结合上下文语义,更适合交给语义层的 LLM 去做(见
common/semantic_enrichment_prompt.md 里新增的"OCR文本清洗"部分),
而不是在 Python 里越堆越多的 if/字典。

本脚本现在只做一件事,而且是纯结构性的、零内容改动的操作:

按款号(如单独一行的 "3.1")把 OCR 输出的零散换行重新组织成
"一款一条结构化记录",输出 `.structured.json`。这一步不判断任何
文字对不对,只是利用"款号是一个明确的、可用正则识别的分段标记"
这个结构信息,把原本被切成好几行的一句话重新拼回一段——不删字、
不加字、不改字,纯粹是换行位置的调整。

后续的"异常符号/错字清洗"由 LLM 在语义加工阶段完成(读
`.structured.json` 里的逐款文字,输出清洗后的版本 + 修改日志),
不在本脚本内处理。

用法:
    python clean_ocr_text.py <raw_chunks目录>/<article_id>.txt
"""

import re
import json
import argparse
from pathlib import Path


CLAUSE_LINE_RE = re.compile(r"^\d+\.\d+[A-Za-z]?$")
PAGE_MARK_RE = re.compile(r"^---\s*page\s*(\d+)\s*---$")
HEADING_RE = re.compile(r"^[笫第]\s*\d+[A-Za-z]?\s*条")
PAGE_NUMBER_RE = re.compile(r"^\d{1,4}$")


def reflow(raw_text: str):
    """
    按款号行重排,返回 (clauses, unassigned):
      clauses: [{"clause_id": "3.1", "page": 37, "text": "..."}]
      unassigned: 不属于任何款的行(标题、页码、无法识别的噪声行),
                  原样保留供人工看,不丢弃、不合并进正文。
    """
    lines = raw_text.split("\n")
    clauses = []
    unassigned = []
    current_page = None
    current_clause = None
    current_buf = []

    def flush():
        nonlocal current_clause, current_buf
        if current_clause is not None:
            text = "".join(current_buf).strip()
            clauses.append({"clause_id": current_clause, "page": current_page, "text": text})
        current_clause = None
        current_buf = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        pm = PAGE_MARK_RE.match(stripped)
        if pm:
            flush()
            current_page = int(pm.group(1))
            continue
        if HEADING_RE.match(stripped):
            flush()
            unassigned.append({"page": current_page, "line": stripped, "note": "条标题行,不计入款内容"})
            continue
        if CLAUSE_LINE_RE.match(stripped):
            flush()
            current_clause = stripped
            continue
        if PAGE_NUMBER_RE.match(stripped):
            unassigned.append({"page": current_page, "line": stripped, "note": "疑似页码/页脚,已从款内容中排除"})
            continue
        if current_clause is not None:
            if current_buf and current_buf[-1] and current_buf[-1][-1].isascii() and stripped[0].isascii():
                current_buf.append(" " + stripped)
            else:
                current_buf.append(stripped)
        else:
            unassigned.append({"page": current_page, "line": stripped, "note": "未归入任何款号,可能是页眉或未识别到款号"})

    flush()
    return clauses, unassigned


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw_txt_path")
    args = ap.parse_args()

    raw_path = Path(args.raw_txt_path)
    raw_text = raw_path.read_text(encoding="utf-8")

    clauses, unassigned = reflow(raw_text)

    out_structured = raw_path.with_suffix("").with_suffix(".structured.json")
    out_structured.write_text(
        json.dumps({"clauses": clauses, "unassigned": unassigned}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"重排完成: {len(clauses)} 款, {len(unassigned)} 行未归入任何款(见 structured.json 的 unassigned)")
    print(f"输出: {out_structured.name}")
    print("提示: 错字/异常符号清洗已改由语义层LLM完成,不在本脚本处理,"
          "参见 common/semantic_enrichment_prompt.md。")


if __name__ == "__main__":
    main()
