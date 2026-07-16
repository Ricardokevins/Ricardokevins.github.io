# Zhang Xiaojun Podcast AI / 机器人访谈知识库实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** 完整转录、核验并深度分析 Zhang Xiaojun Podcast 第一批 10 期 AI、机器人与科技产业访谈，形成 9 篇新增独立笔记、1 篇系列总索引，并复用已经完成的柯丽一鸣笔记。

**Architecture:** 采用“规范节目条目 → 字幕版映射 → 仓库外完整转录 → 私有证据账本 → 仓库内读者型深度笔记 → 系列横向综合”的六层流程。按主题分三批交付，每批先完成字幕完整性和来源核验，再写笔记并独立验证，避免在材料未读完时提前形成结论。

**Tech Stack:** `yt-dlp`、Python 3 标准库、上传者提供的 VTT/SRT、Jekyll、Ruby Notes 校验器、隔离 Chromium/Playwright、Git worktree。

---

## 一、设计选择

### 采用方案：主题批次 + 统一转录管线

- **批次 A：机器人、具身智能与世界模型**——何小鹏、高继扬、谢晨、谢赛宁。
- **批次 B：模型训练、Agent 与 AI for Math**——姚顺宇、罗福莉、洪乐潼。
- **批次 C：工程组织、产品与产业**——SpaceX 洪力德、Anker 阳萌。
- **系列综合**——把上述 9 期与已经完成的柯丽一鸣 / Physical Intelligence 笔记放进同一知识图谱。

### 未采用方案

- **一次性写完九篇再验证：** 反馈周期过长，容易把转录、事实核验或页面结构错误复制到所有页面。
- **只写一篇总综述：** 文件少，但会丢失每位嘉宾的完整时间线、原始论证和证据边界，不符合“内容完整”的要求。
- **为全部 145 期立即建空页面：** 制造目录噪声和未完成内容；当前只落地第一批 10 期，后续沿同一索引增量扩展。

## 二、固定范围

### 已完成基线

- `notes/tech-analysis/kay-ke-physical-intelligence-robotics-interview.html`
- 视频：`dPXZrTw-Hgk`

### 本轮新增节目

| 批次 | 嘉宾 / 主题 | 视频 ID | 目标笔记 |
|---|---|---|---|
| A | 何小鹏 / IRON 与 AI 转型 | `rUjaLPE3mME` | `notes/tech-analysis/he-xiaopeng-iron-robotics-ai-transformation-interview.html` |
| A | 高继扬 / GALAXEA 与具身智能创业 | `c-ZVu-Cr1FQ` | `notes/tech-analysis/gao-jiyang-galaxea-embodied-ai-interview.html` |
| A | 谢晨 / AI 与机器人数据综述 | `KcujArdWR8w` | `notes/tech-analysis/xie-chen-ai-robotics-data-survey-interview.html` |
| A | 谢赛宁 / 世界模型与 AMI Labs | `rIwgZWzUKm8` | `notes/tech-analysis/saining-xie-world-models-ami-labs-interview.html` |
| B | 姚顺宇 / Anthropic、Gemini 与模型训练 | `ttkd0t5qTD4` | `notes/tech-analysis/yao-shunyu-frontier-model-training-agent-interview.html` |
| B | 罗福莉 / OpenClaw、Agent 与后训练 | `V9eI-t3TApE` | `notes/tech-analysis/luo-fuli-openclaw-agent-posttraining-interview.html` |
| B | 洪乐潼 / AI for Math 与 Lean | `78Vyy_dzWXA` | `notes/tech-analysis/carina-hong-ai-for-math-lean-interview.html` |
| C | 洪力德 / SpaceX 工程史 | `a93FT2340c0` | `notes/tech-analysis/spacex-hong-lide-engineering-history-interview.html` |
| C | 阳萌 / Anker、端侧模型与产品哲学 | `kBsqirnWTpI` | `notes/tech-analysis/anker-steven-yang-product-philosophy-interview.html` |

### 系列入口

- Create: `notes/tech-analysis/zhang-xiaojun-podcast-ai-robotics-series.html`
- Modify: `_data/notes.yml`
- Modify: `Progress.md`

## 三、存储与版权边界

- 原始元数据、VTT、SRT、逐时间片文本、章节阅读版和私有证据账本放在：
  `/Users/bytedance/Downloads/VideoProcessor/zhang-xiaojun-podcast/episodes/<video-id>/`
- 仓库只保存分析型 HTML、系列索引、可复用处理脚本和研发记录，不提交完整逐字转录，不提交音频或视频。
- 优先使用上传者字幕；只有字幕缺失或完整性验证失败才下载音频做本地识别。
- 不读取浏览器 Cookie，不绑定或驱动用户前台 Chrome。
- 完整转录用于个人学习与核验；公开笔记以结构化分析、有限短引和来源链接为主。

## 四、每期完成门槛

每期必须同时满足以下条件：

1. 元数据、发布日期、时长、章节、规范 URL 和字幕语言已核验。
2. 中文源字幕的 cue 数、字符数、起止时间、最大空白、空 cue 和末尾无对白时长已统计。
3. `complete-transcript-exact.txt` 与源字幕逐 cue 一致。
4. `complete-transcript-readable.md` 与源字幕归一化文本一致，并按官方章节组织。
5. 全部官方章节已通读；没有只读标题、简介或搜索摘要。
6. 建立“已核验事实 / 发布方报告 / 分析推断 / 建议”四层证据账本。
7. 至少核验 5 个会改变核心结论的一手来源；不足 5 个时必须说明材料本身没有更多可核验外链。
8. 独立笔记至少包含：完整时间地图、核心机制、关键人物/组织、术语、反例与限制、至少 3 条独立 insight、证据附录。
9. 可见正文通常不少于 7,000 字符，至少 10 个 h2/h3；不以灌水满足长度。
10. Notes 结构、Jekyll 构建、桌面端和 390px 手机端渲染全部通过。

## 五、执行任务

### Task 1：建立隔离工作区与计划基线

**Files:**

- Create: `docs/plans/2026-07-16-zhang-xiaojun-podcast-series.md`
- Modify: `Progress.md`

**Steps:**

1. 从 `cad5eff` 创建 `codex/zhang-xiaojun-podcast-series` 独立 worktree。
2. 确认主工作区现有 DeepSeek-V4 修改不进入本分支。
3. 在 `Progress.md` 顶部登记范围、批次、完成门槛与当前状态。
4. 运行 `git diff --check`。
5. Commit: `docs(plan): define Zhang Xiaojun podcast series workflow`。

### Task 2：实现可复用转录构建器

**Files:**

- Create: `scripts/build_youtube_transcript.py`

**Steps:**

1. 从 VTT 读取 cue、时间戳和文本，保留重复与口语。
2. 依据 `info.json` 的官方章节映射 cue。
3. 输出逐 cue 精确版和约 30 秒阅读段落版。
4. 输出机器可读审计 JSON：cue 数、字符数、时间覆盖、空 cue、最大间隔、文本哈希和一致性结果。
5. 用已完成的 `dPXZrTw-Hgk` 数据回归，要求 8,054 cue、74,162 字符和文本一致性全部通过。
6. 对损坏 VTT、缺章节和末尾空白写显式失败或降级路径。
7. Run: `python3 scripts/build_youtube_transcript.py --help`，预期退出 0。
8. Commit: `feat(transcripts): add deterministic YouTube transcript builder`。

### Task 3：获取并核验九期字幕

**Files outside repository:**

- `/Users/bytedance/Downloads/VideoProcessor/zhang-xiaojun-podcast/manifest.json`
- `/Users/bytedance/Downloads/VideoProcessor/zhang-xiaojun-podcast/episodes/<video-id>/*`

**Steps:**

1. 只下载九期元数据和上传字幕，不下载视频。
2. 下载可用中文与英文字幕为 VTT，同时生成 SRT。
3. 对九期运行转录构建器。
4. 汇总 cue、字符、覆盖率、章节数、最大空白与哈希。
5. 失败项最多重试三轮；仍失败时只对该期进入音频识别路径。
6. 人工抽查每期首段、章节边界和末段。
7. 生成总 manifest，去除中文主版本与英文字幕版的重复映射。

### Task 4：批次 A 来源图与完整通读

**Materials:** 何小鹏、高继扬、谢晨、谢赛宁四期完整转录。

**Steps:**

1. 逐章阅读四期全部转录并写章节级论点表。
2. 为每期建立四层证据账本。
3. 核验公司官网、研究项目、论文、模型/产品发布、公开演讲或官方文档。
4. 标出嘉宾判断与独立证据不一致之处。
5. 提炼跨访谈主线：本体、世界模型、数据、评估、组织与商业化。

### Task 5：写作并验证批次 A 四篇笔记

**Files:**

- Create: `notes/tech-analysis/he-xiaopeng-iron-robotics-ai-transformation-interview.html`
- Create: `notes/tech-analysis/gao-jiyang-galaxea-embodied-ai-interview.html`
- Create: `notes/tech-analysis/xie-chen-ai-robotics-data-survey-interview.html`
- Create: `notes/tech-analysis/saining-xie-world-models-ami-labs-interview.html`
- Modify: `_data/notes.yml`
- Modify: `Progress.md`

**Steps:**

1. 按 Notes 模板完成四篇独立文章。
2. 每完成一篇先运行定向结构、生成痕迹和锚点检查。
3. 四篇完成后运行 Notes 索引校验和 Jekyll build。
4. 用隔离浏览器检查桌面和手机，共 8 个渲染场景。
5. Commit: `docs(notes): analyze robotics and world-model interviews`。

### Task 6：批次 B 来源图与完整通读

**Materials:** 姚顺宇、罗福莉、洪乐潼三期完整转录。

**Steps:**

1. 逐章阅读三期全部转录并写章节级论点表。
2. 核验模型训练经历、Agent 相关研究、后训练方法、Lean/形式化数学项目和公开论文。
3. 区分个人预测、机构公开事实和录制后新进展。
4. 提炼跨访谈主线：预训练—后训练—环境—验证器—形式化证明。

### Task 7：写作并验证批次 B 三篇笔记

**Files:**

- Create: `notes/tech-analysis/yao-shunyu-frontier-model-training-agent-interview.html`
- Create: `notes/tech-analysis/luo-fuli-openclaw-agent-posttraining-interview.html`
- Create: `notes/tech-analysis/carina-hong-ai-for-math-lean-interview.html`
- Modify: `_data/notes.yml`
- Modify: `Progress.md`

**Steps:**

1. 完成三篇读者型深度笔记。
2. 定向检查术语、公式、来源归属、短引和事实时点。
3. 运行 Notes 校验、Jekyll build 与 6 个桌面/手机渲染场景。
4. Commit: `docs(notes): analyze model training agents and AI for math`。

### Task 8：批次 C 来源图与完整通读

**Materials:** SpaceX 洪力德、Anker 阳萌两期完整转录。

**Steps:**

1. 逐章阅读两期全部转录。
2. 核验 SpaceX 历史节点、组织机制、公开发射/工程材料，以及 Anker 产品、品类和端侧模型公开材料。
3. 区分口述史、公司叙事、可独立验证事实和个人管理哲学。
4. 提炼跨访谈主线：高不确定工程、组织设计、产品边界和长期复利。

### Task 9：写作并验证批次 C 两篇笔记

**Files:**

- Create: `notes/tech-analysis/spacex-hong-lide-engineering-history-interview.html`
- Create: `notes/tech-analysis/anker-steven-yang-product-philosophy-interview.html`
- Modify: `_data/notes.yml`
- Modify: `Progress.md`

**Steps:**

1. 完成两篇深度笔记。
2. 运行定向内容与证据检查。
3. 运行 Notes 校验、Jekyll build 与 4 个桌面/手机渲染场景。
4. Commit: `docs(notes): analyze SpaceX and Anker interviews`。

### Task 10：建立系列总索引与跨访谈 Insight

**Files:**

- Create: `notes/tech-analysis/zhang-xiaojun-podcast-ai-robotics-series.html`
- Modify: `_data/notes.yml`
- Modify: `Progress.md`

**Steps:**

1. 建立 10 期节目卡片、主题标签、嘉宾、时长、来源与完成状态。
2. 建立概念交叉矩阵：数据、世界模型、Agent、VLA、评估、组织、产品与产业。
3. 写出至少 7 条跨访谈 insight，并注明它们来自哪些节目、推理链和适用边界。
4. 明确嘉宾间的共识、分歧与利益位置，禁止把不同语境下的同名概念强行合并。
5. 给出后续 145 期扩展策略和下一批候选，但不创建空页面。
6. 运行定向页面验证。
7. Commit: `docs(notes): add Zhang Xiaojun podcast series synthesis`。

### Task 11：整体验收与发布

**Steps:**

1. 核对 9 期原始字幕、精确版、阅读版、审计 JSON 和证据账本均存在。
2. 核对 9 篇新增笔记、1 篇系列索引和已有柯丽一鸣笔记形成完整 10 期入口。
3. Run: `ruby scripts/validate_notes_index.rb`，预期无错误。
4. Run: `git diff --check`，预期无输出。
5. Run: `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build`，预期退出 0。
6. 对 10 个新增页面执行桌面和手机自动验收：HTTP 200、无整页溢出、无断锚、无 console/page/request error。
7. 人工目检系列首页和每批至少一篇代表页。
8. 扫描敏感凭证、占位文本和公开生成痕迹，预期无命中。
9. 将分支更新到最新 `origin/main`，解决共享 `_data/notes.yml` / `Progress.md` 变更时只保留双方有效内容。
10. 推送 `codex/zhang-xiaojun-podcast-series`，验证远端 SHA。
11. 在主工作区无未处理冲突时合并到 `main` 并推送；若主工作区仍有其他未提交工作，则保留已推送分支并采用不覆盖用户改动的发布路径。
12. 验证 GitHub Pages 部署成功及所有公开 URL 返回 200。

## 六、最终用户交付

- 一个公开系列总索引。
- 九篇新增深度笔记，加上既有柯丽一鸣笔记，共十期。
- 九期仓库外完整中文逐句转录、章节阅读版和中英文 SRT。
- 每期转录完整性统计和证据边界。
- 系列级共识、分歧、知识图谱和至少七条跨访谈 insight。
- 分阶段 commit、最终远端 SHA、构建与浏览器验收证据。
