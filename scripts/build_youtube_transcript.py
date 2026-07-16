#!/usr/bin/env python3
"""Build deterministic, auditable transcripts from an uploaded YouTube VTT track."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


TIMING_LINE = re.compile(
    r"^(?P<start>(?:\d+:)?\d{2}:\d{2}[.,]\d{3})\s+-->\s+"
    r"(?P<end>(?:\d+:)?\d{2}:\d{2}[.,]\d{3})(?:\s+.*)?$"
)
TAG = re.compile(r"<[^>]+>")
WHITESPACE = re.compile(r"\s+")


class TranscriptError(RuntimeError):
    """Raised when a source cannot produce a trustworthy transcript."""


@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    text: str


@dataclass(frozen=True)
class Chapter:
    start: float
    end: float
    title: str
    official: bool = True


@dataclass(frozen=True)
class Paragraph:
    start: float
    cues: tuple[Cue, ...]


@dataclass(frozen=True)
class TimingRepair:
    cue_number: int
    original_start: float
    original_end: float
    corrected_start: float
    corrected_end: float


def parse_timestamp(value: str) -> float:
    """Convert VTT HH:MM:SS.mmm or MM:SS.mmm to seconds."""
    parts = value.replace(",", ".").split(":")
    if len(parts) == 2:
        hours = 0
        minutes, seconds = parts
    elif len(parts) == 3:
        hours, minutes, seconds = parts
    else:
        raise TranscriptError(f"invalid VTT timestamp: {value}")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def stamp(value: float, milliseconds: bool = False) -> str:
    """Render seconds as a stable transcript timestamp."""
    value = max(0.0, value)
    hours = int(value // 3600)
    minutes = int(value % 3600 // 60)
    seconds = value % 60
    if milliseconds:
        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d}"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_text(texts: Sequence[str]) -> str:
    """Normalize layout-only whitespace while preserving every spoken character."""
    return "".join(WHITESPACE.sub("", text) for text in texts)


def clean_cue_text(lines: Sequence[str]) -> str:
    text = " ".join(line.strip() for line in lines)
    return WHITESPACE.sub(" ", TAG.sub("", html.unescape(text))).strip()


def parse_vtt(
    path: Path, repairs: dict[int, TimingRepair] | None = None
) -> tuple[list[Cue], dict[str, Any]]:
    """Parse a VTT file and reject timing corruption instead of silently dropping it."""
    repairs = repairs or {}
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise TranscriptError(f"cannot read VTT file {path}: {error}") from error
    if not raw:
        raise TranscriptError("VTT file is empty")

    try:
        source = raw.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise TranscriptError(f"VTT is not valid UTF-8: {error}") from error
    if not source.lstrip().startswith("WEBVTT"):
        raise TranscriptError("VTT header is missing")

    cues: list[Cue] = []
    malformed_timing_lines = 0
    reversed_cues = 0
    applied_repairs: list[dict[str, Any]] = []
    blocks = re.split(r"\r?\n\s*\r?\n", source.strip())
    for block in blocks:
        lines = block.splitlines()
        timing_indexes = [index for index, line in enumerate(lines) if "-->" in line]
        if not timing_indexes:
            continue
        timing_index = timing_indexes[0]
        match = TIMING_LINE.match(lines[timing_index].strip())
        if match is None:
            malformed_timing_lines += 1
            continue
        start = parse_timestamp(match.group("start"))
        end = parse_timestamp(match.group("end"))
        cue_number = len(cues) + 1
        repair = repairs.get(cue_number)
        if repair is not None:
            if abs(start - repair.original_start) > 0.0005 or abs(end - repair.original_end) > 0.0005:
                raise TranscriptError(
                    f"timing repair for cue {cue_number} does not match source timing"
                )
            start = repair.corrected_start
            end = repair.corrected_end
            applied_repairs.append(
                {
                    "cue_number": cue_number,
                    "original_start_seconds": repair.original_start,
                    "original_end_seconds": repair.original_end,
                    "corrected_start_seconds": repair.corrected_start,
                    "corrected_end_seconds": repair.corrected_end,
                }
            )
        if end < start:
            reversed_cues += 1
            continue
        cues.append(Cue(start=start, end=end, text=clean_cue_text(lines[timing_index + 1 :])))

    if malformed_timing_lines or reversed_cues:
        raise TranscriptError(
            "VTT timing corruption detected: "
            f"{malformed_timing_lines} malformed, {reversed_cues} reversed"
        )
    if not cues:
        raise TranscriptError("VTT contains no cues")
    unused_repairs = sorted(set(repairs) - {item["cue_number"] for item in applied_repairs})
    if unused_repairs:
        raise TranscriptError(f"timing repairs were not applied to cues: {unused_repairs}")
    if any(cues[index].start < cues[index - 1].start for index in range(1, len(cues))):
        raise TranscriptError("VTT cues are not ordered by start time")

    return cues, {
        "source_bytes": len(raw),
        "source_sha256": sha256_bytes(raw),
        "timing_repairs": applied_repairs,
    }


def parse_timing_repairs(values: Sequence[str]) -> dict[int, TimingRepair]:
    """Parse explicit, source-checked cue repairs without mutating the uploaded VTT."""
    repairs: dict[int, TimingRepair] = {}
    for value in values:
        parts = value.split(",")
        if len(parts) != 5:
            raise TranscriptError(
                "timing repair must be CUE,ORIGINAL_START,ORIGINAL_END,"
                "CORRECTED_START,CORRECTED_END in seconds"
            )
        try:
            repair = TimingRepair(
                cue_number=int(parts[0]),
                original_start=float(parts[1]),
                original_end=float(parts[2]),
                corrected_start=float(parts[3]),
                corrected_end=float(parts[4]),
            )
        except ValueError as error:
            raise TranscriptError(f"invalid timing repair: {value}") from error
        if repair.cue_number <= 0:
            raise TranscriptError("timing repair cue number must be positive")
        if repair.corrected_end < repair.corrected_start:
            raise TranscriptError("corrected cue end cannot precede its start")
        if repair.cue_number in repairs:
            raise TranscriptError(f"duplicate timing repair for cue {repair.cue_number}")
        repairs[repair.cue_number] = repair
    return repairs


def load_metadata(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        raw = path.read_bytes()
        metadata = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise TranscriptError(f"cannot read metadata JSON {path}: {error}") from error
    if not isinstance(metadata, dict):
        raise TranscriptError("metadata JSON must contain an object")
    return metadata, {"source_bytes": len(raw), "source_sha256": sha256_bytes(raw)}


def build_chapters(
    metadata: dict[str, Any], cues: Sequence[Cue]
) -> tuple[list[Chapter], list[str], int]:
    """Return complete chapter coverage, preserving official chapters when available."""
    warnings: list[str] = []
    raw_chapters = metadata.get("chapters") or []
    official: list[Chapter] = []
    duration = float(metadata.get("duration") or cues[-1].end)

    if isinstance(raw_chapters, list):
        for index, raw_chapter in enumerate(raw_chapters):
            if not isinstance(raw_chapter, dict) or raw_chapter.get("start_time") is None:
                warnings.append(f"ignored malformed chapter at index {index}")
                continue
            start = float(raw_chapter["start_time"])
            next_start = None
            if index + 1 < len(raw_chapters) and isinstance(raw_chapters[index + 1], dict):
                next_start = raw_chapters[index + 1].get("start_time")
            end = raw_chapter.get("end_time")
            if end is None:
                end = next_start if next_start is not None else duration
            title = str(raw_chapter.get("title") or f"章节 {index + 1}").strip()
            if title.startswith("<Untitled"):
                title = "开场与内容预告"
            official.append(Chapter(start=start, end=float(end), title=title))

    if not official:
        warnings.append("metadata has no usable official chapters; used one full-interview chapter")
        return (
            [Chapter(cues[0].start, max(duration, cues[-1].end), "完整访谈", False)],
            warnings,
            0,
        )

    if any(official[index].start < official[index - 1].start for index in range(1, len(official))):
        raise TranscriptError("metadata chapters are not ordered by start time")
    if any(chapter.end < chapter.start for chapter in official):
        raise TranscriptError("metadata contains a chapter whose end precedes its start")

    chapters = list(official)
    if cues[0].start < official[0].start:
        chapters.insert(0, Chapter(cues[0].start, official[0].start, "章节前内容", False))
        warnings.append("added a preface chapter so early cues are not lost")
    if cues[-1].start >= official[-1].end:
        chapters.append(Chapter(official[-1].end, max(duration, cues[-1].end), "章节后内容", False))
        warnings.append("added a trailing chapter so late cues are not lost")
    return chapters, warnings, len(official)


def map_cues_to_chapters(
    cues: Sequence[Cue], chapters: Sequence[Chapter]
) -> list[tuple[Chapter, list[Cue]]]:
    mapped: list[tuple[Chapter, list[Cue]]] = []
    cursor = 0
    for index, chapter in enumerate(chapters):
        chapter_cues: list[Cue] = []
        while cursor < len(cues):
            cue = cues[cursor]
            in_chapter = cue.start >= chapter.start and (
                cue.start < chapter.end or index == len(chapters) - 1
            )
            if in_chapter:
                chapter_cues.append(cue)
                cursor += 1
                continue
            if cue.start < chapter.start:
                raise TranscriptError(f"cue at {stamp(cue.start, True)} was not mapped to a chapter")
            break
        mapped.append((chapter, chapter_cues))
    if cursor != len(cues):
        raise TranscriptError(f"chapter mapping lost {len(cues) - cursor} cues")
    return mapped


def build_paragraphs(cues: Sequence[Cue], window: int) -> list[Paragraph]:
    if window <= 0:
        raise TranscriptError("paragraph window must be greater than zero")
    paragraphs: list[Paragraph] = []
    current: list[Cue] = []
    paragraph_start: float | None = None
    for cue in cues:
        if paragraph_start is None:
            paragraph_start = cue.start
        if current and cue.start - paragraph_start >= window:
            paragraphs.append(Paragraph(paragraph_start, tuple(current)))
            current = []
            paragraph_start = cue.start
        current.append(cue)
    if current and paragraph_start is not None:
        paragraphs.append(Paragraph(paragraph_start, tuple(current)))
    return paragraphs


def render_exact(cues: Sequence[Cue]) -> str:
    return "\n".join(
        f"[{stamp(cue.start, milliseconds=True)}] {cue.text}" for cue in cues
    ) + "\n"


def render_readable(
    metadata: dict[str, Any],
    mapped: Sequence[tuple[Chapter, Sequence[Cue]]],
    paragraphs: Sequence[Sequence[Paragraph]],
    language: str,
    window: int,
) -> str:
    title = str(metadata.get("title") or "YouTube 访谈完整转录")
    lines = [
        f"# {title}｜完整转录",
        "",
        f"- 视频：{metadata.get('webpage_url') or metadata.get('original_url') or ''}",
        f"- 频道：{metadata.get('channel') or metadata.get('uploader') or ''}",
        f"- 时长：{metadata.get('duration_string') or stamp(float(metadata.get('duration') or 0))}",
        f"- 字幕语言：{language}",
        "- 文字基准：上传者提供的字幕；正文保留字幕原词、口语和重复，不做语义改写。",
        f"- 阅读方式：按官方章节组织，每约 {window} 秒合并为一段；逐 cue 精确时间点见同目录的 `complete-transcript-exact.txt`。",
        "",
    ]
    for (chapter, _), chapter_paragraphs in zip(mapped, paragraphs, strict=True):
        marker = "" if chapter.official else "（补充分段）"
        lines.extend(
            [
                f"## {stamp(chapter.start)}–{stamp(chapter.end)} {chapter.title}{marker}",
                "",
            ]
        )
        for paragraph in chapter_paragraphs:
            text = " ".join(cue.text for cue in paragraph.cues)
            lines.extend([f"**[{stamp(paragraph.start)}]** {text}", ""])
    return "\n".join(lines).rstrip() + "\n"


def analyze_timing(cues: Sequence[Cue], duration: float) -> dict[str, Any]:
    positive_gaps: list[tuple[float, int]] = []
    overlap_count = 0
    for index in range(1, len(cues)):
        gap = cues[index].start - cues[index - 1].end
        if gap > 0:
            positive_gaps.append((gap, index))
        elif gap < 0:
            overlap_count += 1
    max_gap, max_gap_index = max(positive_gaps, default=(0.0, 0))
    return {
        "first_cue_start_seconds": round(cues[0].start, 3),
        "last_cue_end_seconds": round(cues[-1].end, 3),
        "spoken_span_seconds": round(cues[-1].end - cues[0].start, 3),
        "video_duration_seconds": round(duration, 3),
        "leading_silence_seconds": round(max(0.0, cues[0].start), 3),
        "trailing_silence_seconds": round(max(0.0, duration - cues[-1].end), 3),
        "maximum_positive_gap_seconds": round(max_gap, 3),
        "maximum_positive_gap_after_cue": max_gap_index,
        "overlapping_adjacent_cues": overlap_count,
    }


def build_audit(
    metadata: dict[str, Any],
    cues: Sequence[Cue],
    mapped: Sequence[tuple[Chapter, Sequence[Cue]]],
    paragraphs: Sequence[Sequence[Paragraph]],
    language: str,
    vtt_info: dict[str, Any],
    metadata_info: dict[str, Any],
    exact: str,
    readable: str,
    warnings: Sequence[str],
    official_chapter_count: int,
) -> dict[str, Any]:
    source_texts = [cue.text for cue in cues]
    mapped_cues = [cue for _, chapter_cues in mapped for cue in chapter_cues]
    readable_cues = [
        cue
        for chapter_paragraphs in paragraphs
        for paragraph in chapter_paragraphs
        for cue in paragraph.cues
    ]
    normalized = normalized_text(source_texts)
    duration = float(metadata.get("duration") or cues[-1].end)
    validations = {
        "chapter_mapping_preserves_cue_order": mapped_cues == list(cues),
        "readable_mapping_preserves_cue_order": readable_cues == list(cues),
        "readable_normalized_text_matches_source": normalized_text(
            [cue.text for cue in readable_cues]
        )
        == normalized,
        "exact_line_count_matches_cues": len(exact.rstrip("\n").splitlines()) == len(cues),
        "source_has_nonempty_text": bool(normalized),
    }
    return {
        "schema_version": 1,
        "video": {
            "id": metadata.get("id"),
            "title": metadata.get("title"),
            "channel": metadata.get("channel") or metadata.get("uploader"),
            "webpage_url": metadata.get("webpage_url") or metadata.get("original_url"),
            "upload_date": metadata.get("upload_date"),
            "duration_seconds": duration,
        },
        "subtitle_language": language,
        "sources": {"vtt": vtt_info, "metadata": metadata_info},
        "transcript": {
            "cue_count": len(cues),
            "empty_cue_count": sum(not cue.text for cue in cues),
            "subtitle_character_count": sum(len(cue.text) for cue in cues),
            "normalized_character_count": len(normalized),
            "normalized_text_sha256": sha256_bytes(normalized.encode("utf-8")),
            "exact_output_sha256": sha256_bytes(exact.encode("utf-8")),
            "readable_output_sha256": sha256_bytes(readable.encode("utf-8")),
            "readable_paragraph_count": sum(len(items) for items in paragraphs),
        },
        "timing": analyze_timing(cues, duration),
        "chapters": {
            "official_count": official_chapter_count,
            "rendered_count": len(mapped),
            "cues_per_rendered_chapter": [len(items) for _, items in mapped],
        },
        "validations": validations,
        "warnings": list(warnings),
        "ok": all(validations.values()),
    }


def write_output(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build exact and chapter-readable transcripts plus an integrity audit."
    )
    parser.add_argument("--vtt", type=Path, required=True, help="uploaded subtitle VTT")
    parser.add_argument("--metadata", type=Path, required=True, help="yt-dlp info JSON")
    parser.add_argument("--output-dir", type=Path, required=True, help="output directory")
    parser.add_argument("--language", required=True, help="subtitle language code")
    parser.add_argument(
        "--window", type=int, default=30, help="readable paragraph window in seconds"
    )
    parser.add_argument(
        "--timing-repair",
        action="append",
        default=[],
        metavar="CUE,OLD_START,OLD_END,NEW_START,NEW_END",
        help="explicit source-checked timing repair in seconds; may be repeated",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repairs = parse_timing_repairs(args.timing_repair)
        cues, vtt_info = parse_vtt(args.vtt, repairs)
        metadata, metadata_info = load_metadata(args.metadata)
        chapters, warnings, official_chapter_count = build_chapters(metadata, cues)
        if repairs:
            warnings.append(
                f"applied {len(repairs)} explicit source-checked timing repair(s)"
            )
        mapped = map_cues_to_chapters(cues, chapters)
        paragraphs = [build_paragraphs(chapter_cues, args.window) for _, chapter_cues in mapped]
        exact = render_exact(cues)
        readable = render_readable(
            metadata, mapped, paragraphs, args.language, args.window
        )
        audit = build_audit(
            metadata,
            cues,
            mapped,
            paragraphs,
            args.language,
            vtt_info,
            metadata_info,
            exact,
            readable,
            warnings,
            official_chapter_count,
        )
        if not audit["ok"]:
            raise TranscriptError("one or more transcript integrity validations failed")
        write_output(args.output_dir / "complete-transcript-exact.txt", exact)
        write_output(args.output_dir / "complete-transcript-readable.md", readable)
        write_output(
            args.output_dir / "transcript-audit.json",
            json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        )
        print(json.dumps(audit, ensure_ascii=False, indent=2))
        return 0
    except TranscriptError as error:
        print(f"transcript build failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
