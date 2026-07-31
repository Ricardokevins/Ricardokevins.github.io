---
name: notes-authoring
description: Repo-local workflow for creating or editing public Notes pages in Ricardokevins.github.io. Use when adding, importing, cleaning, reviewing, or auditing notes under notes/paper-reviews, notes/tech-analysis, notes/llm-interview-question-bank, or notes/math-interview-question-bank; when updating _data/notes.yml; or when removing generation traces, local paths, command logs, and other process noise from public HTML notes.
---

# Notes Authoring Skill

## Core Rule

Public notes are reader-facing articles, not execution logs. Assume the reader has not seen the source. First reconstruct the source in plain language—its background, people or concepts, question flow, argument, examples, evidence, conclusion, and limitations—then switch explicitly to thesis, mechanism, evidence audit, limits, and independent insight. A structured conclusion list cannot replace the explanatory first pass. Put source scope at the end. Do not expose how the agent fetched, rendered, saved, or generated the page.

## Required Inputs

Before creating or heavily editing an independent note, read:

- `notes/NOTE_TEMPLATE.md`
- the target note if it exists
- `_data/notes.yml` if the note needs an index entry
- `scripts/validate_notes_index.rb` when changing note structure or validation rules

## Independent HTML Note Contract

Applies to `notes/paper-reviews/*.html` and `notes/tech-analysis/*.html`.

The page must include:

1. `<!doctype html>` and `<html lang="zh-CN">`
2. one `<title>` in `<head>`
3. viewport meta
4. exactly one `notes-shell.css` reference
5. `<body class="notes-shell-page">`
6. top `notes-sitebar` with `Notes / All Notes / Home`
7. semantic `<main>` wrapper
8. a source-reconstruction section near the top, before independent thesis
9. a direct thesis / takeaway section after the source reconstruction
10. a mechanism / method explanation section
11. explicit term or concept explanations
12. limits / risk / evidence-boundary section
13. final section marked `data-note-role="evidence-appendix"`
14. non-empty `alt` on every image
15. MathJax only when TeX/math markup is present

## Content Shape

Use this order unless the existing page has a strong reason not to:

1. Header: title + short material orientation, not a conclusion dump
2. `#source-reconstruction`: a self-contained explanation of what the source says, in source order or a clearly explained thematic order
3. `#takeaway`: core judgment, now grounded in the first pass
4. `#problem`: why the topic matters and what question the source is trying to answer
5. `#mechanism`: what actually happens, preferably as input -> process -> output -> failure conditions
6. `#evidence`: key experiments, tables, screenshots, or claims with interpretation
7. `#terms`: first-use explanations for non-obvious terms
8. `#limits`: what the material does not prove
9. `#insight`: engineering/research implication
10. `#sources` with `data-note-role="evidence-appendix"`: public source URLs and evidence boundaries only

For interviews and transcripts, `#source-reconstruction` must normally include: who is speaking and why the conversation matters; the host's major questions; the guest's background and chronology; the main claims and examples; the transitions or disagreements between topics; the meaning of unfamiliar terms; the evidence and numbers as the guest presents them; and the guest's own final advice or reservations. A chapter list, evidence table, or later analysis does not satisfy this requirement by itself.

Quality floor for long-form notes:

- usually >= 4,500 visible Chinese/English characters unless intentionally short
- usually >= 5 h2/h3 headings
- include at least one explicit judgment beyond summary
- include at least one boundary/negative case
- explain why the result matters, not just what the source says
- for long interviews, the source-reconstruction pass should be the largest body section and should read as continuous explanation rather than a list of conclusions

## Forbidden in Public Notes

Do not include these in public HTML notes:

- command blocks used to fetch or verify material
- `OpenCLI`, `opencli`, `curl`, `pdftotext`, `pdfinfo`, `mcp-router`, browser automation logs, or similar tool traces
- local paths such as `/tmp/`, `/Users/...`, `Downloads`, `results/...`, `refs/...`, `private/tmp`
- “Generated locally”, “HTML generated”, “报告生成时间”, “本地 HTML 生成”, “最终文件路径”, “文件位置”
- statements about where the agent saved intermediate files
- long “材料怎么抓来的” narratives near the top
- footer boilerplate such as “页面为自包含静态 HTML”

Allowed in the final evidence appendix:

- public URLs
- version/date of the public source if relevant
- evidence boundary: what was verified, what was not verified, what may change
- a short note that a platform page is unstable, without naming local tooling or commands

## Editing Existing Notes

When cleaning an old note:

1. Remove command / reproduction sections first.
2. Replace local artifacts with public source descriptions.
3. Convert source sections to `证据边界与资料索引` and add `data-note-role="evidence-appendix"`.
4. Preserve useful analysis, figures, tables, and citations.
5. Do not rewrite visual design unless layout is broken.
6. If content is short, add mechanism, evidence, limits, and insight rather than adding process details.

## Validation

Always run after note changes:

```bash
ruby scripts/validate_notes_index.rb
git diff --check
```

Run Jekyll build when structure, assets, index, or many pages changed:

```bash
BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build
```

Also scan independent notes for public process noise before finishing:

```bash
rg -n "OpenCLI|opencli|下载 PDF|本地路径|文件位置|本地参考文件位于|Generated locally|HTML generated|/tmp/|/Users/|报告生成|results/|Downloads" "notes/paper-reviews" "notes/tech-analysis"
```

The scan should have no output unless the term is part of the topic itself and is clearly not a process trace.
