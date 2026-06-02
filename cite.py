# -*- coding: utf-8 -*-

import os
import re
import tempfile
from pathlib import Path

from semanticscholar import SemanticScholar

ABOUT_PAGE = Path("_pages/about.md")
AUTHOR_ID = 2193557733
CITATION_BADGE = re.compile(r"^\[!\[citation\]")
PAPER_ID = re.compile(r"/([a-f0-9]{40})")
CITATION_COUNT = re.compile(r"(citation-)\d+")


def update_citation_badges():
    sch = SemanticScholar()
    author = sch.get_author(AUTHOR_ID)
    citation_counts = {paper.paperId: paper.citationCount for paper in author.papers}

    lines = ABOUT_PAGE.read_text(encoding="utf-8").splitlines(keepends=True)
    for index, line in enumerate(lines):
        if not CITATION_BADGE.match(line):
            continue

        paper_id_match = PAPER_ID.search(line)
        if not paper_id_match:
            continue

        paper_id = paper_id_match.group(1)
        citation_count = citation_counts.get(paper_id)
        if citation_count is None:
            continue

        print(citation_count)
        lines[index] = CITATION_COUNT.sub(rf"\g<1>{citation_count}", line)

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=ABOUT_PAGE.parent,
        delete=False,
    ) as tmp_file:
        tmp_file.writelines(lines)
        tmp_path = Path(tmp_file.name)

    os.replace(tmp_path, ABOUT_PAGE)


if __name__ == "__main__":
    update_citation_badges()
