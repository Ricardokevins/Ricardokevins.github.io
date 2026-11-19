# -*- coding: utf-8 -*-

import os
import re
import tempfile
from pathlib import Path

ABOUT_PAGE = Path(__file__).resolve().parent / "_pages/about.md"
AUTHOR_ID = 2193557733
CITATION_BADGE = re.compile(r"^\[!\[citation\]")
PAPER_ID = re.compile(r"/([a-f0-9]{40})")
CITATION_COUNT = re.compile(r"(citation-)\d+")


def refresh_badges(content, citation_counts):
    lines = content.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if not CITATION_BADGE.match(line):
            continue
        paper_id_match = PAPER_ID.search(line)
        if not paper_id_match:
            continue
        citation_count = citation_counts.get(paper_id_match.group(1))
        if not isinstance(citation_count, int) or isinstance(citation_count, bool) or citation_count < 0:
            continue
        lines[index] = CITATION_COUNT.sub(rf"\g<1>{citation_count}", line)
    return "".join(lines)


def update_citation_badges():
    from semanticscholar import SemanticScholar

    sch = SemanticScholar()
    author = sch.get_author(AUTHOR_ID, fields=["papers.paperId", "papers.citationCount"])
    citation_counts = {paper.paperId: paper.citationCount for paper in author.papers}

    original = ABOUT_PAGE.read_text(encoding="utf-8")
    refreshed = refresh_badges(original, citation_counts)
    if refreshed == original:
        print("Citation badges unchanged")
        return

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=ABOUT_PAGE.parent,
        delete=False,
    ) as tmp_file:
        tmp_file.write(refreshed)
        tmp_path = Path(tmp_file.name)

    os.replace(tmp_path, ABOUT_PAGE)
    print("Citation badges updated")


if __name__ == "__main__":
    update_citation_badges()
