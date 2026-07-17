#!/usr/bin/env python3
"""Build deterministic, auditable transcripts from Scripod sentence JSON.

The public Scripod endpoint exposes sentence-level timestamps.  This adapter
keeps the source wording intact, adds speaker labels only when the metadata
declares diarization reliable, and reuses the chapter/paragraph machinery from
``build_youtube_transcript.py``.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from build_youtube_transcript import (
    Chapter,
    Paragraph,
    TranscriptError,
    build_chapters,
    build_paragraphs,
    map_cues_to_chapters,
    normalized_text,
    sha256_bytes,
    stamp,
    write_output,
)


@dataclass(frozen=True)
class SpeakerCue:
    start: float
    end: float
    text: str
    speaker: str = ""


def load_json(path: Path) -> tuple[Any, dict[str, Any]]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise TranscriptError(f"cannot read JSON {path}: {error}") from error
    return value, {"source_bytes": len(raw), "source_sha256": sha256_bytes(raw)}


def flatten_sentences(source: Any) -> tuple[list[SpeakerCue], dict[str, Any]]:
    if not isinstance(source, dict) or not isinstance(source.get("segments"), list):
        raise TranscriptError("Scripod JSON must contain a segments array")
    speakers = source.get("speakers") or {}
    if not isinstance(speakers, dict):
        speakers = {}
    cues: list[SpeakerCue] = []
    malformed = 0
    for segment in source["segments"]:
        if not isinstance(segment, dict):
            malformed += 1
            continue
        speaker_id = str(segment.get("speaker", ""))
        speaker = str(speakers.get(speaker_id, "")).strip()
        sentences = segment.get("sentences")
        if not isinstance(sentences, list):
            malformed += 1
            continue
        for sentence in sentences:
            if not isinstance(sentence, dict):
                malformed += 1
                continue
            text = str(sentence.get("text") or "").strip()
            try:
                start = float(sentence["start"])
                end = float(sentence["end"])
            except (KeyError, TypeError, ValueError) as error:
                raise TranscriptError(f"sentence has invalid timing: {sentence}") from error
            if end < start or start < 0 or not text:
                raise TranscriptError(
                    f"sentence has invalid interval or empty text: {start}, {end}, {text!r}"
                )
            cues.append(SpeakerCue(start=start, end=end, text=text, speaker=speaker))
    if malformed:
        raise TranscriptError(f"source contains {malformed} malformed segments/sentences")
    if not cues:
        raise TranscriptError("Scripod JSON contains no usable sentences")
    if any(cues[index].start < cues[index - 1].start for index in range(1, len(cues))):
        raise TranscriptError("sentence timestamps are not ordered by start time")
    return cues, {
        "segment_count": len(source["segments"]),
        "speaker_map": {str(key): str(value) for key, value in speakers.items()},
    }


def render_exact(cues: Sequence[SpeakerCue], speaker_reliable: bool) -> str:
    lines: list[str] = []
    for cue in cues:
        label = f"{cue.speaker}: " if speaker_reliable and cue.speaker else ""
        lines.append(f"[{stamp(cue.start, milliseconds=True)}] {label}{cue.text}")
    return "\n".join(lines) + "\n"


def render_readable(
    metadata: dict[str, Any],
    mapped: Sequence[tuple[Chapter, Sequence[SpeakerCue]]],
    paragraphs: Sequence[Sequence[Paragraph]],
    language: str,
    window: int,
    speaker_reliable: bool,
) -> str:
    title = str(metadata.get("title") or "访谈完整转录")
    lines = [
        f"# {title}｜完整转录",
        "",
        f"- 视频：{metadata.get('webpage_url') or metadata.get('original_url') or ''}",
        f"- 频道：{metadata.get('channel') or ''}",
        f"- 时长：{metadata.get('duration_string') or stamp(float(metadata.get('duration') or 0))}",
        f"- 转录语言：{language}",
        "- 文字基准：Scripod sentence-level ASR；正文保留原词、口语和重复，不做语义改写。",
        f"- 阅读方式：按节目章节组织，每约 {window} 秒合并为一段；逐句精确时间点见同目录的 `complete-transcript-exact.txt`。",
        (
            "- 说话人：保留 ASR 说话人标签。"
            if speaker_reliable
            else "- 说话人：ASR 未能可靠分离说话人，正文不显示说话人标签。"
        ),
        "",
    ]
    for (chapter, _), chapter_paragraphs in zip(mapped, paragraphs, strict=True):
        marker = "" if chapter.official else "（补充分段）"
        lines.extend([f"## {stamp(chapter.start)}–{stamp(chapter.end)} {chapter.title}{marker}", ""])
        for paragraph in chapter_paragraphs:
            pieces: list[str] = []
            for cue in paragraph.cues:
                label = f"{cue.speaker}：" if speaker_reliable and getattr(cue, "speaker", "") else ""
                pieces.append(f"{label}{cue.text}")
            lines.extend([f"**[{stamp(paragraph.start)}]** {' '.join(pieces)}", ""])
    return "\n".join(lines).rstrip() + "\n"


def render_srt(cues: Sequence[SpeakerCue], speaker_reliable: bool) -> str:
    def srt_stamp(value: float) -> str:
        value = max(0.0, value)
        hours = int(value // 3600)
        minutes = int(value % 3600 // 60)
        seconds = int(value % 60)
        millis = int(round((value - int(value)) * 1000))
        if millis == 1000:
            seconds += 1
            millis = 0
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"

    blocks: list[str] = []
    for index, cue in enumerate(cues, start=1):
        label = f"{cue.speaker}: " if speaker_reliable and cue.speaker else ""
        blocks.append(f"{index}\n{srt_stamp(cue.start)} --> {srt_stamp(cue.end)}\n{label}{cue.text}")
    return "\n\n".join(blocks) + "\n"


def timing_stats(cues: Sequence[SpeakerCue], duration: float) -> dict[str, Any]:
    gaps: list[tuple[float, int]] = []
    overlaps = 0
    for index in range(1, len(cues)):
        gap = cues[index].start - cues[index - 1].end
        if gap > 0:
            gaps.append((gap, index))
        elif gap < 0:
            overlaps += 1
    max_gap, max_index = max(gaps, default=(0.0, 0))
    return {
        "first_sentence_start_seconds": round(cues[0].start, 3),
        "last_sentence_end_seconds": round(cues[-1].end, 3),
        "spoken_span_seconds": round(cues[-1].end - cues[0].start, 3),
        "video_duration_seconds": round(duration, 3),
        "leading_silence_seconds": round(cues[0].start, 3),
        "trailing_silence_seconds": round(max(0.0, duration - cues[-1].end), 3),
        "maximum_positive_gap_seconds": round(max_gap, 3),
        "maximum_positive_gap_after_sentence": max_index,
        "overlapping_adjacent_sentences": overlaps,
    }


def build_audit(
    metadata: dict[str, Any],
    cues: Sequence[SpeakerCue],
    mapped: Sequence[tuple[Chapter, Sequence[SpeakerCue]]],
    paragraphs: Sequence[Sequence[Paragraph]],
    source_info: dict[str, Any],
    source_shape: dict[str, Any],
    exact: str,
    readable: str,
    srt: str,
    language: str,
    window: int,
    speaker_reliable: bool,
) -> dict[str, Any]:
    source_text = normalized_text([cue.text for cue in cues])
    mapped_cues = [cue for _, items in mapped for cue in items]
    readable_cues = [cue for items in paragraphs for paragraph in items for cue in paragraph.cues]
    validations = {
        "source_has_nonempty_text": bool(source_text),
        "timestamps_monotonic": all(cues[i].start >= cues[i - 1].start for i in range(1, len(cues))),
        "chapter_mapping_preserves_sentence_order": mapped_cues == list(cues),
        "readable_mapping_preserves_sentence_order": readable_cues == list(cues),
        "readable_normalized_text_matches_source": normalized_text([cue.text for cue in readable_cues]) == source_text,
        "exact_line_count_matches_sentences": len(exact.rstrip("\n").splitlines()) == len(cues),
        "srt_block_count_matches_sentences": len([line for line in srt.splitlines() if line.isdigit()]) == len(cues),
    }
    duration = float(metadata.get("duration") or cues[-1].end)
    return {
        "schema_version": 1,
        "video": {
            "id": metadata.get("id"),
            "title": metadata.get("title"),
            "channel": metadata.get("channel"),
            "webpage_url": metadata.get("webpage_url") or metadata.get("original_url"),
            "duration_seconds": duration,
        },
        "transcript_language": language,
        "paragraph_window_seconds": window,
        "speaker_attribution": {
            "reliable": speaker_reliable,
            "source_map": source_shape.get("speaker_map", {}),
        },
        "sources": {"scripod_json": source_info, "shape": source_shape},
        "transcript": {
            "segment_count": source_shape.get("segment_count"),
            "sentence_count": len(cues),
            "empty_sentence_count": sum(not cue.text for cue in cues),
            "character_count": sum(len(cue.text) for cue in cues),
            "normalized_character_count": len(source_text),
            "normalized_text_sha256": sha256_bytes(source_text.encode("utf-8")),
            "exact_output_sha256": sha256_bytes(exact.encode("utf-8")),
            "readable_output_sha256": sha256_bytes(readable.encode("utf-8")),
            "srt_output_sha256": sha256_bytes(srt.encode("utf-8")),
            "readable_paragraph_count": sum(len(items) for items in paragraphs),
        },
        "timing": timing_stats(cues, duration),
        "chapters": {
            "source": metadata.get("chapter_source"),
            "rendered_count": len(mapped),
            "sentences_per_rendered_chapter": [len(items) for _, items in mapped],
        },
        "validations": validations,
        "warnings": ([] if speaker_reliable else ["speaker diarization is not reliable; labels omitted from rendered transcript"]),
        "ok": all(validations.values()),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Scripod exact/readable/SRT transcripts and an integrity audit.")
    parser.add_argument("--source-json", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--language", default="zh-CN")
    parser.add_argument("--window", type=int, default=30)
    parser.add_argument("--speaker-reliable", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        source, source_info = load_json(args.source_json)
        metadata, _ = load_json(args.metadata)
        if not isinstance(metadata, dict):
            raise TranscriptError("metadata JSON must contain an object")
        cues, source_shape = flatten_sentences(source)
        chapters, chapter_warnings, _ = build_chapters(metadata, cues)
        mapped = map_cues_to_chapters(cues, chapters)
        paragraphs = [build_paragraphs(items, args.window) for _, items in mapped]
        exact = render_exact(cues, args.speaker_reliable)
        readable = render_readable(metadata, mapped, paragraphs, args.language, args.window, args.speaker_reliable)
        srt = render_srt(cues, args.speaker_reliable)
        audit = build_audit(metadata, cues, mapped, paragraphs, source_info, source_shape, exact, readable, srt, args.language, args.window, args.speaker_reliable)
        audit["warnings"].extend(chapter_warnings)
        audit["ok"] = audit["ok"] and not any("ignored malformed" in warning for warning in audit["warnings"])
        if not audit["ok"]:
            raise TranscriptError("one or more transcript integrity validations failed")
        write_output(args.output_dir / "complete-transcript-exact.txt", exact)
        write_output(args.output_dir / "complete-transcript-readable.md", readable)
        write_output(args.output_dir / "complete-transcript.srt", srt)
        write_output(args.output_dir / "transcript-audit.json", json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(audit, ensure_ascii=False, indent=2))
        return 0
    except TranscriptError as error:
        print(f"transcript build failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
