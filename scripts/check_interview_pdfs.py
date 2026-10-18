#!/usr/bin/env python3
"""Check PDF chapter/question/code coverage; needs bs4, pypdf and Poppler."""
from pathlib import Path
import json
import re
import subprocess

from bs4 import BeautifulSoup
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
BOOKS = {
    "quant-interview-handbook.pdf": sorted((ROOT / "notes/quant-interview-question-bank/chapters").glob("*.html")),
    "quant-interview-52.pdf": [ROOT / "notes/tech-analysis/xiaohongshu-quant-interview-question-bank.html"],
    "quant-interview-61.pdf": [ROOT / "notes/tech-analysis/xiaohongshu-quant-interview-practice-expansion.html"],
    "leetcode-hot-100.pdf": [ROOT / "notes/leetcode-hot-100/index.html"],
    "quant-probability-statistics.pdf": [ROOT / "notes/quant-foundations/probability-statistics.html"],
    "quant-machine-learning.pdf": [ROOT / "notes/quant-foundations/machine-learning.html"],
}


def normalize(text):
    return re.sub(r"\s+", "", text).replace("\u200b", "")


def check_book(filename, sources):
    pdf = ROOT / "notes/downloads" / filename
    reader = PdfReader(pdf)
    text = subprocess.check_output(["pdftotext", "-layout", str(pdf), "-"]).decode()
    # A code block can span pages. Remove the known footer before comparing.
    text = re.sub(r"(?m)^\s*\d+\s*/\s*\d+\s*$", "", text)
    compact = normalize(text)
    # Formula baselines can make layout extraction interleave math with a line
    # of Chinese prose; raw stream order provides an independent text reading.
    raw_text = subprocess.check_output(["pdftotext", "-raw", str(pdf), "-"]).decode()
    raw_text = re.sub(r"(?m)^\s*\d+\s*/\s*\d+\s*$", "", raw_text)
    raw_compact = normalize(raw_text)
    assert len(reader.pages) > 5, f"{filename}: unexpectedly short"
    assert reader.outline, f"{filename}: missing PDF outline"
    assert "目录" in compact, f"{filename}: missing printed contents"
    assert "file:///" not in text and "/Users/" not in text, f"{filename}: local path in visible text"
    headings = codes = supplements = 0
    for source in sources:
        soup = BeautifulSoup(source.read_text(), "html.parser")
        for anchor in soup.select(".anchor-link"):
            anchor.decompose()
        main = soup.select_one("main")
        for heading in main.select("h2, h3"):
            label = heading.get_text(" ", strip=True)
            # TeX is rendered, so compare the stable title before inline math.
            label = label.split("\\(")[0].split("\\[")[0].split("$")[0]
            if len(normalize(label)) < 4:
                continue
            assert normalize(label) in compact, f"{filename}: missing heading {label!r}"
            headings += 1
        for code in main.select("pre code"):
            if normalize(code.get_text()) not in compact:
                # Poppler can order a CJK inline comment before its ASCII //
                # marker. Check both code and comment independently in that case.
                for line in code.get_text().splitlines():
                    if normalize(line) in compact:
                        continue
                    pieces = line.split("//", 1)
                    comment_words = re.findall(r"[A-Za-z_][A-Za-z_0-9]*|[\u4e00-\u9fff]+", pieces[-1])
                    assert len(pieces) == 2 and normalize(pieces[0]) in compact and all(word in compact for word in comment_words), f"{filename}: missing code line from {source.name}: {line!r}"
            codes += 1
        for supplement in main.select('[data-derivation], [data-exercise], .derivation-steps, .foundation-bridge, .reading-prerequisites, .state-walkthrough, .term-bridge, .worked-bridge'):
            phrases = re.findall(r"[\u4e00-\u9fff]{4,}", supplement.get_text(" ", strip=True))
            phrases = [p for p in phrases if p not in {"推导补全与自检", "补足中间步骤与检验"}]
            assert phrases, f"{source}: supplement lacks substantive explanation"
            for phrase in sorted(phrases, key=len, reverse=True)[:2]:
                assert phrase in compact or phrase in raw_compact, f"{filename}: stale or omitted supplement: {phrase!r}"
            supplements += 1
    for page in reader.pages:
        for ref in page.get("/Annots", []):
            annotation = ref.get_object()
            action = annotation.get("/A")
            if action:
                uri = str(action.get_object().get("/URI", ""))
                assert not uri.startswith("file:"), f"{filename}: local link {uri}"
    fonts = subprocess.check_output(["pdffonts", str(pdf)]).decode().splitlines()[2:]
    assert fonts and all(re.search(r"\s+yes\s+(?:yes|no)\s+(?:yes|no)\s+\d+\s+\d+\s*$", line) for line in fonts), f"{filename}: unembedded font"
    return {"file": filename, "pages": len(reader.pages), "headings": headings,
            "code_blocks": codes, "supplements": supplements, "bytes": pdf.stat().st_size}


if __name__ == "__main__":
    reports = [check_book(name, sources) for name, sources in BOOKS.items()]
    print(json.dumps({"pdfs": reports, "result": "passed"}, ensure_ascii=False, indent=2))
