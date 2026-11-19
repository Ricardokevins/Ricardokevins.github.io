#!/usr/bin/env python3
"""Check built-site references and exclusions using Python and Ruby standard libraries."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class PageReferences(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, int]] = []
        self.ids: list[str] = []
        self.names: set[str] = set()

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.names.add(attrs["name"])
        for attribute in ("href", "src", "poster", "data"):
            value = attrs.get(attribute)
            if value and (attribute != "data" or tag == "object"):
                self.references.append((value, self.getpos()[0]))


def validate_site(site: Path, root: Path, config: dict) -> tuple[list[str], dict]:
    site = site.resolve()
    root = root.resolve()
    if site == root:
        raise ValueError("build directory must differ from the source directory")
    if not (site / "index.html").is_file():
        raise ValueError(f"build directory has no index.html: {site}")
    host = urlsplit(config["url"]).hostname
    baseurl = config.get("baseurl", "").rstrip("/")
    errors: list[str] = []
    pages: dict[Path, PageReferences] = {}
    references: list[tuple[Path, str, int | None]] = []
    for path in sorted(site.rglob("*.html")):
        page = PageReferences()
        page.feed(path.read_text(encoding="utf-8"))
        pages[path] = page
        duplicates = [value for value, count in Counter(page.ids).items() if count > 1]
        if duplicates:
            errors.append(f"{path.relative_to(site)}: duplicate ids {duplicates}")
        references.extend((path, ref, line) for ref, line in page.references)
    for path in site.rglob("*.css"):
        source = path.read_text(encoding="utf-8")
        for match in re.finditer(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", source, re.I):
            references.append((path, match.group(1).strip(), None))
    for path in site.rglob("*manifest*.json"):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        references.extend((path, icon["src"], None) for icon in manifest.get("icons", []) if icon.get("src"))
    for scope in config.get("exclude", []):
        if any(character in scope for character in "*?[]"):
            continue
        if (root / scope).exists() and (site / scope).exists():
            errors.append(f"excluded source leaked into build: {scope}")
    for path, reference, line in references:
        reference = reference.strip()
        label = f"{path.relative_to(site)}:{line or 0}"
        try:
            parts = urlsplit(reference)
            if parts.scheme and parts.scheme not in ("http", "https"):
                continue
            if parts.netloc and parts.hostname != host:
                continue
            address = unquote(parts.path)
            if baseurl and (address == baseurl or address.startswith(baseurl + "/")):
                address = address[len(baseurl):]
            target = ((site / address.lstrip("/") if address.startswith("/") else path.parent / address)
                      if address else path).resolve()
            if not target.is_relative_to(site):
                errors.append(f"{label}: reference escapes the build: {reference}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file() and not target.suffix and target.with_suffix(".html").is_file():
                target = target.with_suffix(".html")
            if not target.is_file():
                errors.append(f"{label}: missing target {reference}")
                continue
            if parts.fragment and target in pages and not parts.fragment.startswith(":~:text="):
                anchor = unquote(parts.fragment)
                anchors = set(pages[target].ids) | pages[target].names
                if anchor not in anchors:
                    errors.append(f"{label}: missing anchor {reference}")
        except ValueError as error:
            errors.append(f"{label}: invalid reference {reference!r}: {error}")
    return list(dict.fromkeys(errors)), {"html_pages": len(pages), "references": len(references)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path, nargs="?", default=Path("_site"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        result = subprocess.run(
            ["ruby", "-ryaml", "-rjson", "-e",
             "puts JSON.generate(YAML.safe_load(File.read(ARGV.fetch(0)), aliases: true))",
             str(root / "_config.yml")],
            text=True, capture_output=True, check=True,
        )
        errors, counts = validate_site(args.site, root, json.loads(result.stdout))
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"site validation failed: {error}", file=sys.stderr)
        return 1
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"site ok: {counts['html_pages']} HTML pages, {counts['references']} references; "
          "no missing targets, duplicate ids or excluded files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
