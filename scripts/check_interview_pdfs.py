#!/usr/bin/env python3
"""Check PDF chapter/question/code coverage; needs bs4, pypdf and Poppler."""
from pathlib import Path
import argparse
import json
import re
import subprocess

from bs4 import BeautifulSoup
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
BOOKS = {
    book["file"]: [ROOT / source for source in book["sources"]]
    for book in json.loads((ROOT / "scripts/interview_books.json").read_text())["books"].values()
}


def normalize(text):
    return re.sub(r"\s+", "", text).replace("\u200b", "")

def poppler(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    diagnostics = result.stderr.decode(errors="replace")
    assert not re.search(r"(?:Syntax|Internal) Error", diagnostics), diagnostics
    return result.stdout.decode()


def check_book(filename, sources):
    pdf = ROOT / "notes/downloads" / filename
    reader = PdfReader(pdf)
    text = poppler(["pdftotext", "-layout", str(pdf), "-"])
    # A code block can span pages. Remove the known footer before comparing.
    text = re.sub(r"(?m)^\s*\d+\s*/\s*\d+\s*$", "", text)
    compact = normalize(text)
    # Formula baselines can make layout extraction interleave math with a line
    # of Chinese prose; raw stream order provides an independent text reading.
    raw_text = poppler(["pdftotext", "-raw", str(pdf), "-"])
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
        expected_slow = {"026.html": 6, "027.html": 8, "028.html": 6, "029.html": 10, "030.html": 10}
        if "quant-interview-question-bank/chapters" in str(source) and source.name in expected_slow:
            assert len(main.select(".slow-walkthrough")) == expected_slow[source.name], f"{source}: missing slow worked examples"

        if source.parent.name == "chapters" and source.name == "044.html" and "quant-interview-question-bank" in str(source):
            cards = main.select('section.problem[id^="e"]')
            assert len(cards) == 120, "quant 044: expected 120 exercise cards"
            for card in cards:
                supplements_for_card = card.select("[data-derivation]")
                expected = f"44-{card['id']}"
                assert len(supplements_for_card) == 1 and supplements_for_card[0]["data-derivation"] == expected, f"quant 044: derivation attached to wrong exercise {card['id']}"
        for heading in main.select("h2, h3"):
            label = heading.get_text(" ", strip=True)
            # TeX is rendered, so compare the stable title before inline math.
            label = label.split("\\(")[0].split("\\[")[0].split("$")[0]
            if len(normalize(label)) < 4:
                continue
            assert normalize(label) in compact, f"{filename}: missing heading {label!r}"
            headings += 1
        for code in main.select("pre code"):
            if normalize(code.get_text()) not in compact and normalize(code.get_text()) not in raw_compact:
                # Poppler can order a CJK inline comment before its ASCII //
                # marker. Check both code and comment independently in that case.
                for line in code.get_text().splitlines():
                    if normalize(line) in compact or normalize(line) in raw_compact:
                        continue
                    pieces = line.split("//", 1)
                    comment_words = re.findall(r"[A-Za-z_][A-Za-z_0-9]*|[\u4e00-\u9fff]+", pieces[-1])
                    assert len(pieces) == 2 and normalize(pieces[0]) in compact and all(word in compact for word in comment_words), f"{filename}: missing code line from {source.name}: {line!r}"
            codes += 1
        for supplement in main.select('[data-derivation], [data-exercise], .derivation-steps, .foundation-bridge, .reading-prerequisites, .state-walkthrough, .term-bridge, .worked-bridge, [data-slow-derivation], [data-slow-foundation], .slow-walkthrough'):
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
    fonts = poppler(["pdffonts", str(pdf)]).splitlines()[2:]
    assert fonts and all(re.search(r"\s+yes\s+(?:yes|no)\s+(?:yes|no)\s+\d+\s+\d+\s*$", line) for line in fonts), f"{filename}: unembedded font"
    return {"file": filename, "pages": len(reader.pages), "headings": headings,
            "code_blocks": codes, "supplements": supplements, "bytes": pdf.stat().st_size}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-archives", action="store_true",
                        help="also validate the two optional large archive PDFs")
    args = parser.parse_args()
    catalog = json.loads((ROOT / "scripts/interview_books.json").read_text())["books"]
    chosen = [b["file"] for b in catalog.values()
              if args.include_archives or not b.get("archive")]
    reports = [check_book(name, BOOKS[name]) for name in chosen]
    print(json.dumps({"pdfs": reports, "result": "passed"}, ensure_ascii=False, indent=2))
