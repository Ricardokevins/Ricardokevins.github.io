# 站内笔记写作流程与质量规范（Notes Guide & QA Spec）

本文件是站内 Notes 的**唯一权威流程与规范**。新建、导入、清理、审查、批量修复笔记时都以本文件为准。配套文件：

- `notes/NOTE_TEMPLATE.md` —— 自包含笔记的整页骨架 + 组件库 + 公式规则。
- `.agent/skills/notes-authoring/SKILL.md` —— 内容口径（面向读者、去执行痕迹）。
- `scripts/validate_notes_index.rb` —— 结构与索引自动校验。

---

## 0. 两套笔记体系（先分清，别用错样式）

| 体系 | 路径 | 样式来源 | 布局 | 用什么模板 |
|------|------|----------|------|------------|
| 自包含笔记 | `notes/paper-reviews/*.html`、`notes/tech-analysis/*.html` | 页内 `<style>` + `notes-shell.css` | 单栏文章 | `NOTE_TEMPLATE.md` |
| 题库章节 | `notes/llm-interview-question-bank/chapters/*.html` | `question-bank.css` + `notes-shell.css` | 左侧栏目录 + 右正文 | 复制同题库相邻章节 |
| 题库章节 | `notes/math-interview-question-bank/chapters/*.html` | `math-bank.css` + `notes-shell.css` | 左侧栏目录 + 右正文 | 复制同题库相邻章节 |

新建题库章节时，**复制同目录相邻章节**作为骨架（侧栏目录、`chapter-orientation`、`chapter-nav` 都要保持一致），不要套用自包含模板。

---

## 1. 写作 / 修复流程（标准动作）

1. **读规范**：先读本文件 + `NOTE_TEMPLATE.md` + `notes-authoring/SKILL.md`。
2. **起骨架**：自包含笔记复制 `NOTE_TEMPLATE.md`；题库章节复制相邻章节。
3. **写内容**：按“核心判断 → 问题背景 → 机制 → 证据 → 术语 → 边界 → 启发 → 证据索引”组织；专有名词首次出现给一句解释。
4. **过公式**：严格按第 3 节公式规则；含公式才加载 MathJax，不含公式就删掉。
5. **静态自检**：跑第 4 节的扫描命令，把命中项清零或确认无害。
6. **构建**：`BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build`。
7. **视觉验证（必做）**：按第 5 节用浏览器看 `_site/` 编译结果的真实渲染，桌面 + 窄屏各看一遍。只看 HTML 源码不算通过。
8. **跑校验**：`ruby scripts/validate_notes_index.rb` 与 `git diff --check`。
9. **登记**：在 `Progress.md` 记录改了什么、验证结果。

---

## 2. QA 检查清单（规范核心 · 逐项过）

每篇笔记完成后，按下面四类逐项检查。括号内是问题级别。

### 2.1 公式正确性
- [ ] （严重）`\(...\)` / `\[...\]` 内**没有裸 `<` 或 `>` 后跟字母**。小于写 `\lt`，大于写 `\gt`，`≤`/`≥` 写 `\le`/`\ge`。
      典型错误：`\(x_{<t}\)` → 必须写 `\(x_{\lt t}\)`；浏览器会把 `<t` 当成 HTML 标签，破坏整页 DOM。
- [ ] （严重）行内公式不要混用裸 `$...$`；金额、`$1.5` 这类文本不会被误解析。
- [ ] （美观）希腊字母、上下标用 LaTeX（`\theta`、`\Sigma`、`x_t`、`d_k`），不要用纯文本 `theta`/`sigma`/`x_t` 冒充公式。
- [ ] （美观）成段数学表达式优先用 LaTeX，而不是行内 `code`（`QK^T/sqrt(d_k)` → `\(QK^\top/\sqrt{d_k}\)`）。
- [ ] （一致）页面有公式 → 必须加载 MathJax；无公式 → 删掉 MathJax `<script>`。

### 2.2 布局不炸裂（最常见的“显示错乱”）
- [ ] （严重）**两列/网格容器里不要放含行内公式的 `<p>`**。`.def-list` / `.formula-list` 的直接子元素只能是 `<div><b>…</b><span>…</span></div>`；正文段落写在容器**之外**。
      原因：MathJax 把每个 `\(…\)` 渲染成一个元素，`<p>` 一旦进了两列 grid，文字和公式会被拆成交替的行（008.html 的历史事故）。
- [ ] （布局）每个 `<table>` 都包在可横向滚动的容器里（自包含笔记用 `<div class="table-wrap">`，题库用既有 `.table-wrap`）。
- [ ] （布局）展示公式包在 `<div class="math-display">\[ … \]</div>`，手机端可横向滚动。
- [ ] （布局）`<pre>` 代码、超长不可断 token 不撑破正文；窄屏可滚动。
- [ ] （布局）窄屏（≈390px）下侧栏/正文不横向溢出，网格塌成单列。

### 2.3 结构完整
- [ ] 一个 `<title>`、viewport meta、恰好一次 `notes-shell.css`、`<body class="notes-shell-page">`。
- [ ] 顶部 `notes-sitebar` 含 `Notes / All Notes / Home`。
- [ ] 自包含笔记有语义 `<main>`；题库章节有 `.chapter` section、`chapter-orientation`、唯一一个 `chapter-nav`。
- [ ] 每个 `<img>` 有非空 `alt`，描述图里是什么；图片用本地资源（同名 `*-assets/` 或 `notes/assets/`）。
- [ ] 无重复 HTML `id`；锚点 `href="#..."` 都指向页面内存在的 id。
- [ ] 文末有 `data-note-role="evidence-appendix"` 的“证据边界与资料索引”。

### 2.4 内容口径（面向读者，去执行痕迹）
- [ ] 开头直接进入主题判断，不写“我抓取了什么/报告生成于哪里”。
- [ ] 正文与页脚**不出现**：工具名、抓取命令、shell、本地路径、`/tmp/`、`/Users/`、`Downloads`、`results/`、生成时间、文件位置、`OpenCLI/opencli`。
- [ ] 证据附录**不写**“本地证据”“截图/配图保存在 xxx-assets/”“附图保存为本地证据图”这类生成痕迹；只放公开 URL、证据边界、未确认事项。
- [ ] 篇幅：长文一般 ≥ 4500 字、≥ 5 个 h2/h3，至少一处明确判断、一处边界/反例。

---

## 3. 公式规则速记

| 想表达 | 写法 | 不要写 |
|--------|------|--------|
| 小于 | `\lt` | 裸 `<` |
| 大于 | `\gt` | 裸 `>`（行内公式中） |
| ≤ / ≥ | `\le` / `\ge` | `<=` / `>=` |
| 行内 | `\( ... \)` | 裸 `$...$` |
| 展示 | `<div class="math-display">\[ ... \]</div>` | 裸 `\[...\]` 不包容器 |
| 希腊字母 | `\theta \Sigma \alpha` | 纯文本 `theta` |
| 转置 | `\top` | 纯文本 `^T`（行内 code） |

---

## 4. 静态自检命令（命中即排查）

在仓库根目录跑。理想结果：A/B/C 无输出或全部确认无害。

```bash
# A. 公式里裸 < 后跟字母（严重，破坏 DOM）
rg -n '\\\([^)]*<[a-zA-Z]' notes/paper-reviews notes/tech-analysis \
  notes/llm-interview-question-bank/chapters notes/math-interview-question-bank/chapters

# B. 证据附录 / 正文里的生成痕迹
rg -n '本地证据|截图保存在|配图保存在|保存在.{0,20}-assets|文件位置|本地路径|下载 PDF|Generated locally|/tmp/|/Users/|OpenCLI|opencli|results/' \
  notes/paper-reviews notes/tech-analysis

# C. 表格是否都包了 table-wrap（counts 仅作参考，需人工核对未包裹的 <table>）
for d in notes/paper-reviews notes/tech-analysis; do \
  echo "$d table=$(rg -c '<table' $d | awk -F: '{s+=$2} END{print s}') \
  wrap=$(rg -c 'table-wrap' $d | awk -F: '{s+=$2} END{print s}')"; done

# D. 结构与索引校验
ruby scripts/validate_notes_index.rb
git diff --check
```

---

## 5. 视觉验证流程（必做，光看 HTML 会漏问题）

```bash
# 1) 构建（验证编译产物，而不是源 HTML）
BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build

# 2) 起本地静态服务（file:// 会被浏览器工具拒绝）
python3 -m http.server 8847   # 在仓库根目录

# 3) 在浏览器打开编译产物（注意是 _site 路径）
#    http://localhost:8847/_site/notes/<folder>/<file>.html
```

用浏览器自动化逐页检查时，至少覆盖：

1. **整页截图**：标题、卡片、公式、表格、图片是否对齐美观，有无错乱。
2. **公式区**：行内公式是否真的内联、展示公式是否成块且可滚动、有没有 LaTeX 报错红字。
3. **表格区**：是否在容器内、窄屏能横向滚动而不撑破布局。
4. **窄屏**：把视口设到 ≈390px，确认网格塌成单列、无横向滚动条溢出。
5. **控制台**：无 MathJax / 资源 404 报错。

发现问题 → 改源文件（`notes/...`，不是 `_site/`）→ 重新构建 → 再看。

---

## 6. 设计基调（美观、简洁、大方）

- 暖色纸张底 + 青绿主强调 + 赭石次强调，留白充足，圆角 8–10px，阴影克制。
- 标题用衬线，正文/标签用无衬线；行高 1.7 左右，正文宽度上限约 1100px。
- 组件统一走 `NOTE_TEMPLATE.md` 的 `callout / card / def-list / figure / math-display / table-wrap`；不要每篇自创不一致的盒子样式。
- 颜色只用三档强调（主/信息/警示），不堆砌多色；同一页风格一致优先于花哨。
