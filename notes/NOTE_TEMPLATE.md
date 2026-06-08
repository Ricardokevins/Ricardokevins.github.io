# Standalone Notes HTML Template

这个模板用于新建 `notes/paper-reviews/*.html` 或 `notes/tech-analysis/*.html` 这类独立站内笔记。目标是保持页面兼容、可读、可维护：桌面端信息密度足够，手机端不横向挤压正文；公式、图片、表格和代码都能正常展示。

> 写作前先读 `.agent/skills/notes-authoring/SKILL.md`。公共 Notes 是读者文章，不是执行日志。不要把抓取命令、工具名、本地路径、生成时间、临时文件路径写进正文或页脚。

## Required Structure

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{NOTE_TITLE}}</title>
  <!-- 如正文包含公式，保留 MathJax；无公式可删除这两个 script。 -->
  <script>
    window.MathJax = {
      tex: {
        inlineMath: [['\\(', '\\)']],
        displayMath: [['$$', '$$'], ['\\[', '\\]']],
        processEscapes: true
      },
      chtml: {
        matchFontHeight: false,
        mtextInheritFont: true,
        linebreaks: { automatic: true, width: 'container' }
      },
      options: { skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'] }
    };
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
  <link rel="stylesheet" href="../assets/notes-shell.css">
  <style>
    :root {
      color-scheme: light;
      --paper: #f6f2ea;
      --surface: #fffdf8;
      --ink: #1f2428;
      --muted: #5f686f;
      --line: #d8ddd8;
      --accent: #1f6678;
      --accent-2: #8a5a22;
      --shadow: 0 18px 46px rgba(31, 37, 40, 0.09);
      --radius: 8px;
      --max: 1180px;
      --sans: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
      --serif: "Iowan Old Style", "Palatino", "Songti SC", "Noto Serif CJK SC", Georgia, serif;
      --mono: "SFMono-Regular", "Menlo", "Consolas", monospace;
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; background: var(--paper); }
    body {
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: var(--sans);
      line-height: 1.72;
      letter-spacing: 0;
    }

    a { color: var(--accent); text-underline-offset: 3px; }
    main, header, footer {
      width: min(var(--max), calc(100% - 32px));
      margin: 0 auto;
    }

    header { padding: clamp(34px, 6vw, 72px) 0 28px; }
    .kicker {
      margin-bottom: 10px;
      color: var(--accent-2);
      font: 800 13px/1.3 var(--sans);
    }
    h1 {
      max-width: 920px;
      margin: 0;
      font: 780 clamp(34px, 5vw, 62px)/1.08 var(--serif);
      letter-spacing: 0;
    }
    .lede {
      max-width: 860px;
      margin: 18px 0 0;
      color: var(--muted);
      font-size: clamp(17px, 2vw, 20px);
    }

    main {
      display: grid;
      gap: 28px;
      padding-bottom: 56px;
    }
    section {
      padding-top: 28px;
      border-top: 1px solid var(--line);
    }
    h2, h3 {
      margin: 0 0 12px;
      line-height: 1.2;
      letter-spacing: 0;
    }
    h2 { font-size: clamp(25px, 3.5vw, 38px); }
    h3 { margin-top: 20px; font-size: 20px; }

    .grid-2, .grid-3 {
      display: grid;
      gap: 14px;
      margin: 18px 0;
    }
    .grid-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .grid-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .card, .callout {
      min-width: 0;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--surface);
      box-shadow: var(--shadow);
    }
    .callout {
      border-left: 4px solid var(--accent);
      box-shadow: none;
    }

    img {
      display: block;
      max-width: 100%;
      height: auto;
      border-radius: 6px;
    }
    figure {
      margin: 20px 0;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--surface);
    }
    figcaption {
      margin-top: 8px;
      color: var(--muted);
      font-size: 14px;
    }

    .math-display,
    mjx-container {
      max-width: 100%;
      overflow-x: auto;
      overflow-y: hidden;
    }
    pre, .table-wrap {
      max-width: 100%;
      overflow-x: auto;
    }
    code, pre {
      font-family: var(--mono);
    }

    @media (max-width: 760px) {
      main, header, footer { width: min(100% - 24px, var(--max)); }
      .grid-2, .grid-3 { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body class="notes-shell-page">
  <nav class="notes-sitebar" aria-label="Notes navigation">
    <a class="notes-sitebar__brand" href="../"><span class="notes-sitebar__mark" aria-hidden="true"></span><span>Notes</span></a>
    <span class="notes-sitebar__links">
      <a class="notes-sitebar__link" href="../">All Notes</a>
      <a class="notes-sitebar__link" href="../../">Home</a>
    </span>
  </nav>

  <header id="top">
    <div class="kicker">{{NOTE_KIND}} · {{DATE}}</div>
    <h1>{{NOTE_TITLE}}</h1>
    <p class="lede">{{ONE_PARAGRAPH_THESIS}}</p>
  </header>

  <main>
    <section id="takeaway">
      <h2>核心判断</h2>
      <p>{{START_WITH_THE_ACTUAL_POINT}}</p>
    </section>

    <section id="problem">
      <h2>问题背景</h2>
      <p>{{WHY_THIS_MATTERS}}</p>
    </section>

    <section id="mechanism">
      <h2>机制拆解</h2>
      <p>{{EXPLAIN_THE_CORE_MECHANISM_AS_INPUT_PROCESS_OUTPUT_AND_FAILURE_CONDITIONS}}</p>
    </section>

    <section id="evidence">
      <h2>关键证据</h2>
      <p>{{EXPLAIN_EXPERIMENTS_TABLES_FIGURES_OR_CASES_AND_INTERPRET_THEM}}</p>
    </section>

    <section id="terms">
      <h2>术语解释</h2>
      <div class="grid-2">
        <div class="card"><h3>{{TERM}}</h3><p>{{PLAIN_LANGUAGE_DEFINITION}}</p></div>
      </div>
    </section>

    <section id="limits">
      <h2>边界与风险</h2>
      <p>{{WHAT_THIS_DOES_NOT_PROVE}}</p>
    </section>

    <section id="insight">
      <h2>工程 / 研究启发</h2>
      <p>{{WHAT_SHOULD_A_READER_DO_DIFFERENTLY_AFTER_READING_THIS}}</p>
    </section>

    <section id="sources" data-note-role="evidence-appendix">
      <h2>证据边界与资料索引</h2>
      <p>{{SOURCE_SCOPE_AND_VERIFICATION_BOUNDARY_WITHOUT_LOCAL_COMMANDS_OR_PATHS}}</p>
      <ul>
        <li><a href="{{SOURCE_URL}}">{{SOURCE_TITLE}}</a></li>
      </ul>
    </section>
  </main>
</body>
</html>
```

## Content Rules

- 标题和开头只服务读者理解主题，不写“我抓取了什么”“报告生成于哪里”。
- 每个专有名词第一次出现时给一句解释；复杂方法用“输入、处理、输出、失败条件”讲清楚。
- 不写工具名、抓取命令、shell 命令、本地路径、临时目录、`results/`、`Downloads`、生成时间或文件位置。
- 公式使用 `\(...\)` 或 `\[...\]`，不要混用裸 `$...$`，避免普通文本误触发。
- 图片放在同名 `*-assets/` 目录或 `notes/assets/` 下；`alt` 要说明图里是什么，不写空值。
- 文末必须保留 `data-note-role="evidence-appendix"` 的“证据边界与资料索引”，只放公开 URL、证据边界和未确认事项。
- 写完运行 `ruby scripts/validate_notes_index.rb`、`git diff --check`；批量改动再运行 Jekyll build。
