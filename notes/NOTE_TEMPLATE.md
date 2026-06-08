# 站内独立笔记模板（Standalone Notes Template）

这个模板用于新建 `notes/paper-reviews/*.html` 与 `notes/tech-analysis/*.html` 这类**自包含**站内笔记。目标：桌面端信息密度足够、手机端不横向挤压；公式、图片、表格、代码、卡片都能正确且美观地渲染。

> 写作前先读 `.agent/skills/notes-authoring/SKILL.md` 和同目录的 `NOTES_GUIDE.md`。公共 Notes 是面向读者的文章，不是执行日志：不要把抓取命令、工具名、本地路径、生成时间、临时文件写进正文或页脚。
>
> 题库章节（`llm-interview-question-bank` / `math-interview-question-bank`）不用本模板，它们有自己的 `question-bank.css` / `math-bank.css` 与侧栏布局，结构见 `NOTES_GUIDE.md`。

---

## 1. 整页骨架（直接复制）

把下面整段复制为新文件，替换 `{{...}}` 占位符。没有公式时删除两个 MathJax `<script>`；保留的话也只在出现 `\(...\)` / `\[...\]` 时才加载。

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{NOTE_TITLE}}</title>

  <!-- 仅当正文含公式时保留这两个 script -->
  <script>
    window.MathJax = {
      loader: { load: ['[tex]/ams', '[tex]/noerrors', '[tex]/noundefined'] },
      tex: {
        inlineMath: [['\\(', '\\)']],
        displayMath: [['\\[', '\\]']],
        processEscapes: true,
        packages: { '[+]': ['ams', 'noerrors', 'noundefined'] }
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
      --paper: #f4f0e8;        /* 页面底色 */
      --surface: #fffdf8;      /* 卡片底色 */
      --ink: #20242a;          /* 正文 */
      --muted: #5f686f;        /* 次要文字 */
      --line: #dcd6c8;         /* 边框 */
      --accent: #0f766e;       /* 主强调（青绿） */
      --accent-soft: #eef7f4;  /* 强调浅底 */
      --accent-2: #b45309;     /* 次强调（赭石） */
      --accent-2-soft: #fdf3e7;
      --info: #284b7a;         /* 信息蓝 */
      --info-soft: #eef3fb;
      --shadow: 0 16px 44px rgba(31, 37, 40, 0.08);
      --radius: 10px;
      --max: 1100px;
      --sans: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
      --serif: "Iowan Old Style", "Palatino", "Songti SC", "Noto Serif CJK SC", Georgia, serif;
      --mono: "SFMono-Regular", "Menlo", "Consolas", monospace;
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; background: var(--paper); }
    body {
      margin: 0;
      background:
        linear-gradient(90deg, rgba(15,118,110,.04) 1px, transparent 1px),
        linear-gradient(180deg, rgba(40,75,122,.035) 1px, transparent 1px),
        var(--paper);
      background-size: 44px 44px;
      color: var(--ink);
      font-family: var(--sans);
      line-height: 1.75;
    }
    a { color: var(--accent); text-underline-offset: 3px; }

    main, header, footer {
      width: min(var(--max), calc(100% - 32px));
      margin: 0 auto;
    }

    /* ---------- 页头 ---------- */
    header { padding: clamp(36px, 6vw, 76px) 0 26px; }
    .kicker {
      margin-bottom: 12px;
      color: var(--accent-2);
      font: 800 13px/1.3 var(--sans);
      letter-spacing: .04em;
      text-transform: uppercase;
    }
    h1 {
      max-width: 940px;
      margin: 0;
      font: 760 clamp(32px, 5vw, 58px)/1.12 var(--serif);
    }
    .lede {
      max-width: 860px;
      margin: 18px 0 0;
      color: var(--muted);
      font-size: clamp(17px, 2vw, 20px);
    }

    /* ---------- 章节 ---------- */
    main {
      display: grid;
      gap: 30px;
      padding-bottom: 60px;
    }
    section {
      padding-top: 30px;
      border-top: 1px solid var(--line);
    }
    h2, h3 { margin: 0 0 12px; line-height: 1.25; }
    h2 { font-size: clamp(24px, 3.2vw, 34px); }
    h3 { margin-top: 22px; font-size: 20px; color: var(--accent); }
    p { margin: 12px 0; }
    ul, ol { padding-left: 1.3rem; }
    li { margin: 6px 0; }
    strong { font-weight: 700; }

    /* ---------- 卡片 / 网格 ---------- */
    .grid-2, .grid-3 { display: grid; gap: 14px; margin: 18px 0; }
    .grid-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .grid-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .card {
      min-width: 0;
      padding: 16px 18px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--surface);
      box-shadow: var(--shadow);
    }
    .card h3, .card h4 { margin: 0 0 8px; font-size: 16px; color: var(--accent); }
    .card p { margin: 0; color: var(--muted); font-size: 14.5px; }

    /* ---------- 提示框 callout ---------- */
    .callout {
      margin: 18px 0;
      padding: 14px 18px;
      border: 1px solid var(--line);
      border-left: 4px solid var(--accent);
      border-radius: var(--radius);
      background: var(--accent-soft);
    }
    .callout > b { display: block; margin-bottom: 6px; color: var(--accent); }
    .callout.info  { border-left-color: var(--info); background: var(--info-soft); }
    .callout.info > b { color: var(--info); }
    .callout.warn  { border-left-color: var(--accent-2); background: var(--accent-2-soft); }
    .callout.warn > b { color: var(--accent-2); }

    /* ---------- 术语 / 要点行 ---------- */
    .def-list { display: grid; gap: 10px; margin: 18px 0; }
    .def-list > div {
      display: grid;
      grid-template-columns: minmax(120px, .24fr) minmax(0, 1fr);
      gap: 14px;
      align-items: start;
      padding: 12px 14px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--surface);
    }
    .def-list b { color: var(--accent); font-weight: 700; }
    .def-list span { min-width: 0; }

    /* ---------- 图片 / 图注 ---------- */
    figure {
      margin: 22px 0;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--surface);
    }
    img { display: block; max-width: 100%; height: auto; border-radius: 6px; }
    figcaption { margin-top: 8px; color: var(--muted); font-size: 14px; }

    /* ---------- 公式 ---------- */
    .math-display {
      margin: 16px 0;
      padding: 12px 14px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--surface);
      max-width: 100%;
      overflow-x: auto;
      overflow-y: hidden;
    }
    mjx-container { max-width: 100%; overflow-x: auto; overflow-y: hidden; }

    /* ---------- 表格 ---------- */
    .table-wrap {
      margin: 16px 0;
      max-width: 100%;
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--surface);
    }
    table { width: 100%; min-width: 560px; border-collapse: collapse; font-size: 14.5px; }
    th, td { padding: 10px 13px; border-bottom: 1px solid var(--line); vertical-align: top; text-align: left; }
    th { background: var(--accent-soft); color: var(--ink); font-weight: 700; }
    tr:nth-child(even) td { background: rgba(0,0,0,.015); }

    /* ---------- 代码 ---------- */
    code { padding: 2px 6px; border-radius: 5px; background: #ece5d7; color: #7c2d12; font-family: var(--mono); font-size: .92em; }
    pre { margin: 16px 0; padding: 16px; border-radius: var(--radius); background: #18201f; color: #edf7f3; overflow-x: auto; }
    pre code { padding: 0; background: transparent; color: inherit; }

    @media (max-width: 760px) {
      main, header, footer { width: min(100% - 24px, var(--max)); }
      .grid-2, .grid-3 { grid-template-columns: 1fr; }
      .def-list > div { grid-template-columns: 1fr; gap: 6px; }
    }
  </style>
</head>
<body class="notes-shell-page">
  <nav class="notes-sitebar" aria-label="站点导航">
    <a class="notes-sitebar__brand" href="../"><span class="notes-sitebar__mark" aria-hidden="true"></span><span>Notes</span></a>
    <span class="notes-sitebar__links">
      <a class="notes-sitebar__link" href="../">All Notes</a>
      <a class="notes-sitebar__link" href="../../">Home</a>
    </span>
  </nav>

  <header id="top">
    <div class="kicker">{{NOTE_KIND}} · {{TOPIC_TAG}}</div>
    <h1>{{NOTE_TITLE}}</h1>
    <p class="lede">{{ONE_PARAGRAPH_THESIS}}</p>
  </header>

  <main>
    <section id="takeaway">
      <h2>核心判断</h2>
      <p>{{START_WITH_THE_ACTUAL_POINT}}</p>
      <div class="grid-3">
        <div class="card"><h3>{{KEY_1}}</h3><p>{{KEY_1_DETAIL}}</p></div>
        <div class="card"><h3>{{KEY_2}}</h3><p>{{KEY_2_DETAIL}}</p></div>
        <div class="card"><h3>{{KEY_3}}</h3><p>{{KEY_3_DETAIL}}</p></div>
      </div>
    </section>

    <section id="problem">
      <h2>问题背景</h2>
      <p>{{WHY_THIS_MATTERS}}</p>
    </section>

    <section id="mechanism">
      <h2>机制拆解</h2>
      <p>{{INPUT_PROCESS_OUTPUT_AND_FAILURE_CONDITIONS}}</p>
      <div class="math-display">\[ {{KEY_FORMULA}} \]</div>
    </section>

    <section id="evidence">
      <h2>关键证据</h2>
      <p>{{INTERPRET_EXPERIMENTS_TABLES_FIGURES}}</p>
      <div class="table-wrap">
        <table>
          <thead><tr><th>{{COL_1}}</th><th>{{COL_2}}</th><th>{{COL_3}}</th></tr></thead>
          <tbody>
            <tr><td>{{R1C1}}</td><td>{{R1C2}}</td><td>{{R1C3}}</td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <section id="terms">
      <h2>术语解释</h2>
      <div class="def-list">
        <div><b>{{TERM}}</b><span>{{PLAIN_LANGUAGE_DEFINITION}}</span></div>
      </div>
    </section>

    <section id="limits">
      <h2>边界与风险</h2>
      <div class="callout warn"><b>需要谨慎</b><p>{{WHAT_THIS_DOES_NOT_PROVE}}</p></div>
    </section>

    <section id="insight">
      <h2>工程 / 研究启发</h2>
      <p>{{WHAT_SHOULD_A_READER_DO_DIFFERENTLY}}</p>
    </section>

    <section id="sources" data-note-role="evidence-appendix">
      <h2>证据边界与资料索引</h2>
      <p>{{VERIFICATION_BOUNDARY_WITHOUT_LOCAL_COMMANDS_OR_PATHS}}</p>
      <ul>
        <li><a href="{{SOURCE_URL}}">{{SOURCE_TITLE}}</a></li>
      </ul>
    </section>
  </main>
</body>
</html>
```

---

## 2. 组件库（按需复制到正文）

### 2.1 提示框 callout（三种语气）

```html
<div class="callout"><b>核心视角</b><p>一句话点题，强调本节最该记住的判断。</p></div>
<div class="callout info"><b>背景补充</b><p>读者可能缺的前置信息。</p></div>
<div class="callout warn"><b>需要谨慎</b><p>结论的边界、反例、容易踩的坑。</p></div>
```

### 2.2 要点卡片网格

```html
<div class="grid-3">
  <div class="card"><h3>标题</h3><p>一句话说明。</p></div>
  <div class="card"><h3>标题</h3><p>一句话说明。</p></div>
  <div class="card"><h3>标题</h3><p>一句话说明。</p></div>
</div>
```

### 2.3 术语 / 公式逐条解释（左标签 + 右说明）

`.def-list` 的直接子元素**必须是 `<div>`**，且每个 `<div>` 内是 `<b>` + `<span>` 两个子节点。
不要把整段正文写成 `<p>` 放进 `.def-list`：含行内公式的 `<p>` 会被两列网格拆散（这是历史上最常见的“显示错乱”根因）。正文段落写在 `.def-list` **之外**的普通 `<p>` 里。

```html
<div class="def-list">
  <div><b>logits</b><span>\(z\in\mathbb{R}^{V}\)，\(V\) 是词表大小。</span></div>
  <div><b>softmax</b><span>\(p_i=\dfrac{\exp(z_i)}{\sum_j \exp(z_j)}\)，把实数向量变成概率分布。</span></div>
</div>
```

### 2.4 图片与图注

图片放在与笔记同名的 `*-assets/` 目录（如 `my-note-assets/fig1.png`）或 `notes/assets/`。`alt` 必须非空且说明图里是什么。

```html
<figure>
  <img src="my-note-assets/architecture.png" alt="系统架构：检索、重排、生成三段链路的数据流向">
  <figcaption>图 1：三段式 RAG 链路。</figcaption>
</figure>
```

### 2.5 行内公式与展示公式

```html
<!-- 行内 -->
<p>注意力复杂度随序列长度呈 \(O(n^2)\) 增长。</p>

<!-- 展示（独立成块，可横向滚动，手机不挤压） -->
<div class="math-display">\[
\operatorname{Attention}(Q,K,V)=\operatorname{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
\]</div>
```

### 2.6 表格（始终包一层 `.table-wrap` 以便横向滚动）

```html
<div class="table-wrap">
  <table>
    <thead><tr><th>方案</th><th>优点</th><th>代价</th></tr></thead>
    <tbody>
      <tr><td>全参微调</td><td>表达能力强</td><td>显存与成本高</td></tr>
      <tr><td>LoRA</td><td>参数高效</td><td>复杂能力可能欠拟合</td></tr>
    </tbody>
  </table>
</div>
```

---

## 3. 公式规则（最容易出错，务必遵守）

- 行内公式用 `\(...\)`，展示公式用 `\[...\]`；**不要**用裸 `$...$`，避免普通文本里的金额/美元符号误触发。
- 公式里需要“小于号”时，写 `\lt`，**不要**写裸 `<`。裸 `<` 后跟字母会被浏览器当成 HTML 标签，破坏整页 DOM（历史严重事故）。同理“大于等于”用 `\ge`、“小于等于”用 `\le`。
- 展示公式一律包进 `<div class="math-display">\[ ... \]</div>`，保证手机端可横向滚动、不撑破布局。
- 矩阵、长公式优先用 `bmatrix` / `aligned`；超长行用 `aligned` 拆行。
- 希腊字母、上下标必须用 LaTeX（`\theta`、`\Sigma`、`x_t`、`d_k`），**不要**用纯文本 `theta`、`sigma`、`x_t` 冒充公式。
- 含公式的页面必须加载 MathJax（见骨架）；不含公式则删掉 MathJax `<script>`，校验脚本会检查这一致性。

---

## 4. 内容规则（面向读者，不是执行日志）

- 标题与开头直接进入主题判断，不写“我抓取了什么”“报告生成于哪里”。
- 每个专有名词第一次出现给一句解释；复杂方法用“输入 → 处理 → 输出 → 失败条件”讲清楚。
- 正文与页脚不出现：工具名、抓取命令、shell 命令、本地路径、临时目录、`results/`、`Downloads`、生成时间、文件位置、`OpenCLI/opencli` 等痕迹。
- 文末必须保留 `data-note-role="evidence-appendix"` 的“证据边界与资料索引”，只放公开 URL、证据边界与未确认事项；不要写“本地证据/截图保存在 xxx-assets/”这类生成痕迹。
- 篇幅目标：长文一般 ≥ 4500 可见中文/英文字符、≥ 5 个 h2/h3，至少一处明确判断、一处边界或反例。

---

## 5. 写完必做的校验

```bash
ruby scripts/validate_notes_index.rb
git diff --check
```

结构、资产、索引或多页改动后再跑构建并用浏览器视觉检查（流程见 `NOTES_GUIDE.md`）：

```bash
BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build
```
