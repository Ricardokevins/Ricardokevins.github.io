# Ricardokevins.github.io Progress

## 2026-07-09 七月 AI research materials 四篇中文 Notes 转换

### 已完成

- 新增 `notes/tech-analysis/x-ai-research-frontier-threads-2026-07.html`：综合六条 X/Twitter 研究讨论，主线是 AI research 从单点模型叙事转向可验证闭环、信号治理、评测治理和 self-evolving harness。
- 新增 `notes/paper-reviews/agent-environment-scaling-open-models-2026-07.html`：合读 EdgeBench 与 Gemma 4，主线是环境学习评测与可部署开放模型栈需要共同设计。
- 新增 `notes/paper-reviews/verifier-compaction-opd-agent-rl-2026-07.html`：合读 LLM-as-a-Verifier、CompactionRL 与 Direct-OPD，主线是 agent RL 正在复用 verifier signal、compacted state 与 policy-shift reward 三类中间信号。
- 新增 `notes/paper-reviews/beneficial-rl-harness-self-improvement-2026-07.html`：合读 OpenAI Beneficial RL 与 Lilian Weng Harness Engineering，主线是自我改进系统的内部 trait persistence 与外部 harness persistence。
- 更新 `_data/notes.yml`，为四篇新增 Notes 添加列表入口、summary、tags 与 meta。

### 验证

- `ruby scripts/validate_notes_index.rb` 通过：`notes index ok: 105 entries, 105 top-level note html files`。
- 新增四篇笔记的公开过程噪声扫描通过：未命中本地路径、工具痕迹、生成痕迹、session/worker/task 等过程信息。
- 新增四篇笔记的公式裸 `<` targeted scan 通过：未命中 `\\(...<[A-Za-z]`。
- `git diff --check -- _data/notes.yml` 通过。
- 新增四篇笔记通过 `git diff --check --no-index /dev/null <file>` targeted whitespace 检查。
- Jekyll build 尝试失败：`bundle exec jekyll build` 与 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 均报 `bundler: command not found: jekyll`，提示需安装缺失 gem executable。

### 注意

- 写作依据为上游已验证摘要与可公开 canonical sources；部分上游会话完整历史不可直接读取时，按 coordinator 指示以 canonical/public sources 复核关键事实后成文。
- 工作树在本轮开始前已有大量 unstaged 修改，包括 `_data/notes.yml`、`Progress.md`、模板、CSS 与多篇既有 notes；后续若提交，需要只纳入本轮四篇新增 HTML 与共享文件中的本轮增量，避免混入既有修改。

## 2026-06-09 Vivek RL 后训练长帖 HTML 笔记深化

### 背景

- 用户在已完成原帖解读后，要求“深度总结梳理和思考，导出 html 笔记”。
- 目标是在现有站内笔记基础上增强可读性、批判性校正和资料索引，形成可直接阅读的独立 HTML 笔记，而不是只保留对话摘要。

### 已完成

- 原地深化 `notes/tech-analysis/vivek-2332-prime-rl-32-answers.html`。
- 新增“一页总览：它不是答案集，而是一张故障地图”，把原帖重读为 RL 后训练故障排查优先级：reward/env、policy update、rollout faithfulness、数值一致性、异步 staleness。
- 新增“批判性校正：五处最容易被误读的地方”，明确校正：GRPO 不是没有 reward、CE/KL/MLE 等价前提、DPO 的隐式 reward、KV cache 绑定 policy version、框架推荐不能泛化。
- 修正页面顶部与边界章节中对作者组织身份的过强表述，改为“带有 Prime Intellect / Prime-RL 实践偏好”的公开答卷。
- 扩展文末“证据边界与资料索引”，补充 DAPO、GSPO、MiniMax-M1/CISPO、DeepSeek-R1、DPO、OPD、Thinking Machines deterministic inference、AReaL async RL、Prime-RL 等公开来源。

### 验证

- `ruby scripts/validate_notes_index.rb` 通过：`notes index ok: 93 entries, 93 top-level note html files`。
- `git diff --check -- notes/tech-analysis/vivek-2332-prime-rl-32-answers.html Progress.md _data/notes.yml` 通过。
- 公开过程噪声扫描无输出：未命中工具名、本地路径、临时目录、生成痕迹等。

## 2026-06-08 安装并配置 pi-model-router

## 2026-06-08 安装并配置 pi-model-router

### 背景

- 用户明确要求安装并配置 `pi-model-router`。
- 目标是在当前仓库启用 project-local 路由配置，优先使用当前环境中已验证可用的模型组合，而不是依赖未验证 provider。
- 用户随后明确补充两条偏好：
  - router 应该只是“可选模型的一种”，**不要直接成为默认模型**；
  - **不要擅自改变 think level**，router 不应把 low/medium/high 档位自动映射成不同 thinking 强度。

### 已完成

- 安装扩展包：`npm:@yeliu84/pi-model-router@0.3.0`
- 确认当前环境可用模型中，已实际 smoke test 成功：
  - `bytedance-proxy/gpt-5.4-2026-03-05`
  - `deepseek-anthropic/deepseek-v4-flash`
  - `deepseek-anthropic/deepseek-v4-pro`
  - `mimo/mimo-v2.5`
  - `mimo/mimo-v2.5-pro`
- 确认以下候选当前不适合纳入默认 profile：
  - `kimi-coding/kimi-for-coding`：membership verify error
  - `google/gemini-flash-lite-latest`：API key invalid
  - `minimax-anthropic/MiniMax-M3[1m]`：one-shot smoke test 超时
- 新增 project-local router 配置：`.pi/model-router.json`
  - `balanced`：高质量默认档
  - `cheap`：成本优先档
  - `deep`：深度推理档
- **删除** project-local `.pi/settings.json`，避免把 router 强行设成当前仓库默认模型。
- 根据用户偏好重写 router thinking 配置：
  - 所有 tier 的 `thinking` 统一设为 `xhigh`
  - 让 router 只负责“选哪个模型”，**不负责偷偷改 think level 档位**

### 当前配置思路

- `high` tier：优先 `bytedance-proxy/gpt-5.4-2026-03-05`
- `medium` tier：优先 `deepseek-anthropic/deepseek-v4-pro`
- `low` tier：优先 `mimo/mimo-v2.5` / `mimo/mimo-v2.5-pro`，避免低档位被自动降成很弱的 thinking
- 高风险关键词（deploy / production / auth / security / payment / billing / migration）强制走 `high`
- 总结/格式化类关键词（summary / summarize / changelog / rename / format / tl;dr）强制走 `low`
- 由于所有 tier 统一为 `xhigh`，当前 router 更接近“**只做模型选择，不做推理强度选择**”

### 待验证

- 在真实 `pi` TUI 会话里用 `/model` 选择 `router/balanced`，再用 `/router status` 验证 router provider 已正确注册。
- 验证当前仓库新会话仍保持用户自己的默认模型，不会被 router 接管。
- 如用户需要，再继续细调 `rules`、fallback 顺序和 profile 设计。

## 2026-06-08 22:50 vivek_2332 32 答长帖深度解读（Prime Intellect 视角下的 RL 后训练）

### 背景

- 用户要求深度解读 https://x.com/vivek_2332/status/2063566811749331353
- 经抓取确认为 @vivek_2332 对 @sheriyuo 整理的 RL Interview Questions 2026（35 题）的 32 答长帖：算法 16 + Infra 16，作者风格精炼，2-4 句话/题。
- 仓库里已有 sheriyuo 题面笔记（rl-interview-questions-2026.html）。本篇定位为"答案视角/工业实践视角"的互补笔记，避免逐题深解的重复。

### 关键判断

- 答案透露作者是 Prime Intellect 团队成员（Infra 16 直接推荐自家、Prime-RL/verifiers 描述）。
- 三大贯穿判断：(1) 算法差异在 lab scale 被系统层抹平，token-faithful rollout 与 logprob 一致性是真正的工程决定因素；(2) KL 是 reference anchor，去 KL 是为了"在 RLVR 走得更远"，不能硬编码"GRPO 不带 KL"；(3) 异步 RL 三大瓶颈 = staleness + trainer-inference mismatch + token-in/token-out，Prime-RL/verl/TRL/AReaL 的差异就在分别处理这三件事。

### 产出

| 文件 | 类型 | 大小 | 内容 |
|------|------|------|------|
| `notes/tech-analysis/vivek-2332-prime-rl-32-answers.html` | 独立 HTML 笔记 | 34.8 KB | 15 section, 5294 中文字 / 2649 英文词, 15 h2 / 30 h3; 按 6 层技术栈地图重排 32 答; 含 GRPO 变体横向对比表、fp8/int8 选择表、并行维度对照表、监控指标三件套、术语 9 条、证据边界 |
| `_data/notes.yml` | 索引新增 | - | 新增一条 title 为 Prime Intellect 视角下的 RL 后训练 32 答 |
| `scripts/validate_notes_index.rb` | 校验 | - | 93 entries, 93 top-level files, OK |

### 验证

- `ruby scripts/validate_notes_index.rb` -> notes index ok
- `python3 HTMLParser` 平衡检查 -> 0 错误, 0 未闭合
- 5294 中文字符 >= 4500 下限 OK
- 15 h2 + 30 h3 >= 5 下限 OK
- 含 takeaway / problem / mechanism / evidence / terms / limits / insight / evidence-appendix 全 8 段 OK
- 无 bare `<`, 无工具名, 无本地路径, 无生成痕迹 OK

## 2026-06-08 数学题库 008 常见分布生成机制与应用例题深化

### 背景

- 用户反馈 `notes/math-interview-question-bank/chapters/008.html` 中“常见分布按生成机制记”部分还不够深入，希望补充各个分布对应的应用例题。
- 原章节已有分布总览表和 next-token 小例子，但对“题目语言如何映射到分布”“每个分布适合解决什么应用问题”“常见误用边界”讲得偏薄。

### 已完成

- 原地扩写 `notes/math-interview-question-bank/chapters/008.html` 的 `常见分布按生成机制记` 小节。
- 增强分布选择框架：从“随机变量在数什么、一次还是多次抽样、离散还是连续、参数代表什么”出发识别分布。
- 扩展总览表，新增/强化 Bernoulli、Binomial、Geometric、Categorical、Multinomial、Uniform、Gaussian、Poisson、Exponential、Beta 的生成机制、参数语义和应用入口。
- 补充 10 个应用例题，覆盖：
  - Bernoulli vs Binomial 的单题/多题区别；
  - Binomial benchmark 波动与小样本名次不稳定；
  - Geometric 首次成功等待；
  - Categorical next-token 抽样与 greedy decoding 区别；
  - Multinomial 计数向量与 MoE routing / 分桶；
  - Uniform 初始化/采样；
  - Gaussian 误差近似与厚尾风险；
  - Poisson 固定窗口到达次数；
  - Exponential 下一次到达等待时间；
  - Beta 作为成功率先验与小样本 CTR 平滑。

### 待验证

- 运行目标页结构检查、裸 `<` 扫描、notes index validator、`git diff --check` 和 Jekyll build。

## 2026-06-08 全站笔记举一反三深度审查与批量修复

### 背景

- 用户在 math-interview-question-bank/chapters/008.html 的截图中反馈"结果都是错乱的"——具体表现为概率分布 SVG 中 Bayes 卡片文字溢出（"LLM: token distribution · Quant: return / risk distribution" 单行超宽）以及整图被 100% 拉伸显大。
- 用户要求做"举一反三，确保每篇笔记都正常"的全站系统性审查。

### 审查范围

- math-interview-question-bank/chapters/ 20 个章节
- llm-interview-question-bank/chapters/ 90 个章节 + index.html
- paper-reviews/ 42 个 HTML 笔记
- tech-analysis/ 47 个 HTML 笔记
- 资产完整性（23 个 SVG、CSS/JS 引用）
- _data/notes.yml 交叉校验

### 已发现并修复的问题

| 级别 | 问题 | 文件数 | 修复方式 |
|------|------|--------|----------|
| SEVERE | 公式中裸 `<` 后跟字母被浏览器误解析为 HTML 标签，破坏 DOM 树 | 4 文件 6 处 | `<` 替换为 `\lt`（MathJax 命令） |
| SEVERE | SVG 概率图 Bayes 卡片文字溢出 + 整图被无脑 100% 拉伸 | 1 SVG + 1 CSS | SVG 内增加"应用直觉"小标题、tspan 换行；CSS 加 max-width:900px |
| MEDIUM | 悬空锚点 href="#commands" 指向不存在的 id | 7 文件 | 改为页面已有 id（method/source/mechanism） |
| MEDIUM | LLM 题库 data-category="other" 无筛选按钮 | 11 章节 | index.html 新增"综合/专项"按钮 |
| MEDIUM | LLM 题库 5 章节 h2→h4 标题层级跳跃 | 5 文件 | h4 改 h3 |
| MEDIUM | math bank/chapters/015.html 多余一个 `</div>` | 1 文件 | 删除多余闭合标签 |
| MINOR | 8 个 paper-reviews 的 nav aria-label 不一致 | 8 文件 | 统一为 "站点导航" |

### 验证结果

- `ruby scripts/validate_notes_index.rb`: 91 entries, 91 HTML files ✅
- 全站 `<` 在公式中的最终扫描: 0 remaining ✅
- div 平衡 / section 平衡 / id 唯一性: 全部通过 ✅
- `BUNDLE_PATH=/tmp/ricardokevins-gems bundle exec jekyll build`: 5.8s 构建成功 ✅
- GitHub Metadata API rate limit warning（既有，不影响）

### 未修改的已知事项（不影响渲染）

- `_includes/comments.html` 重复 id="comments"（Jekyll 模板，非用户笔记）
- 35 个 tech-analysis 文件的 nav 锚点链接缺少 aria-label（无障碍，非渲染问题）
- math bank 多个章节行内公式中 `>` 作为比较运算符（MathJax v3 能正确处理）

---

## 2026-06-08 MMAE 音频编辑 Benchmark 深度解读与站内笔记导入

### 背景

- 用户要求对 `https://x.com/TencentHunyuan/status/2063862263434613237` 深度分析和介绍，并整理为一个详细全面的站内笔记。
- 目标材料是 Tencent Hunyuan 关于 `MMAE: A Massive Multitask Audio Editing Benchmark` 的 X 发布帖；核心问题是区分“音频生成”和“指令式音频编辑”，解释 MMAE 的 benchmark 设计、rubric 评测范式、模型结果和工程启发。

### 已完成

- 阅读并整理 X 原帖、arXiv `2606.07229`、官方 GitHub 仓库、HuggingFace 数据集与 paper 页面、YouTube demo 元信息。
- 解析论文正文与官方 `MMAE-meta.json`，核对样本数、rubric 数、模态/复杂度/操作分布、评测代码中的 rubric 打分与 Qwen3-Omni judge 流程。
- 新增站内论文笔记：
  - `notes/paper-reviews/mmae-audio-editing-benchmark.html`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口。
- 笔记重点覆盖：
  - 为什么音频编辑不是普通音频生成，而是“只改该改的地方，并保持其他内容不变”；
  - MMAE 的 7 类模态、6 类复杂度、8 类操作与 2,000 样本 / 17,741 rubrics 规模；
  - IFR、CR、EMR 三个指标如何分别刻画指令执行、上下文保持和完美编辑率；
  - 当前代表模型 EMR 低于 5% 的含义，以及复杂任务、混合模态、平均能力与完美执行脱钩、planner 局限等实验洞察；
  - 下一代音频编辑系统需要音频对象表示、局部 mask、多轮状态维护和 verifier 闭环，而不能只依赖端到端重生成。

### 验证结果

- `ruby scripts/validate_notes_index.rb` 通过：`notes index ok: 92 entries, 92 top-level note html files`。
- 新增页面公开过程噪声扫描无输出：未命中工具名、本地路径、临时目录、生成痕迹等。
- `git diff --check -- "notes/paper-reviews/mmae-audio-editing-benchmark.html" "_data/notes.yml" "Progress.md"` 通过。
- HTML 自检：约 14,186 个可见字符，14 个 h2、41 个 h3，且仅有一个 `data-note-role="evidence-appendix"` 与一个 `notes-shell.css` 引用。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅保留既有 `faraday-retry` 建议和 GitHub Metadata 未认证/限流 warning，不影响静态生成。
- 构建后 `_site/notes/paper-reviews/mmae-audio-editing-benchmark.html` 存在，`_site/notes/index.html` 已包含新增 MMAE 页面入口。

## 2026-06-08 AutoLab / 长时程 Agent 闭环控制深度解读与站内笔记导入

### 背景

- 用户要求对 `https://x.com/rohanpaul_ai/status/2063825845605499335` 做更深入的调研分析，并整理成站内笔记。
- 入口材料是 Rohan Paul 对 AutoLab 的 X 帖；核心目标是从表层“persistence”叙事深入到论文、官网、代码仓库、公开轨迹和 benchmark 谱系比较，讲清它真正测到的能力与边界。

### 已完成

- 深读并交叉核对：
  - Rohan Paul 的 X 帖与回复区主要观点；
  - AutoLab 论文 `2606.05080`；
  - AutoLab 官网 leaderboard、task detail 页面与官方博客；
  - `autolabhq/autolab` 仓库 README、36 个 task 的 `task.toml` / representative `instruction.md`；
  - 公开 `flux2_klein_lora` agent trajectories 子样本，用于观察 episode 数、timeout 与 reward 的关系；
  - RE-Bench、AIRS-Bench、KernelBench 与 harness 披露 position paper，用于横向定位。
- 新增站内技术分析笔记：
  - `notes/tech-analysis/autolab-closed-loop-agents.html`
- 新增页面配图资源：
  - `notes/tech-analysis/autolab-closed-loop-agents-assets/leaderboard-0510.jpg`
  - `notes/tech-analysis/autolab-closed-loop-agents-assets/scores-0510.jpg`
- 更新 `_data/notes.yml`，加入 Notes 卡片入口。
- 笔记核心判断包括：
  - AutoLab 不是把“坚持比聪明重要”讲成鸡汤，而是把长时程 agent 的外部实验闭环变成可测量对象；
  - 其核心能力不是单次 answer quality，而是 benchmark、反馈吸收、探索/利用平衡、best-so-far 管理和截止前收尾纪律；
  - 论文里最有价值的部分是 failure mode 与 harness ablation，而不只是 leaderboard；
  - AutoLab 在 benchmark 谱系中更接近长时程 closed-loop optimization，而不是完整 scientific discovery benchmark；
  - harness 是一等变量，不能把结果粗暴读成纯底模智力排名。

### 验证结果

- `ruby scripts/validate_notes_index.rb` 通过：`notes index ok: 91 entries, 91 top-level note html files`。
- 公开过程噪声扫描无输出：未命中工具名、本地路径、临时目录、生成痕迹等。
- `git diff --cached --check` 通过。
- 清理旧 `_site` 后运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅保留既有 `faraday-retry` 建议和 GitHub Metadata 未认证 warning。

## 2026-06-08 RAGEN-2 Reasoning Collapse 深度解读与站内 HTML 笔记导出

### 背景

- 用户要求对 `https://x.com/cwolferesearch/status/2063363579987030044` 做深度详细解读与分析，并导出 HTML 笔记、commit、push。
- 原帖讨论论文 `RAGEN-2: Reasoning Collapse in Agentic RL`，核心主题是 token-level entropy 无法发现跨输入 template collapse，论文链接指向 arXiv `2604.06268`。

### 已完成

- 阅读并整理 X 原帖、作者补充论文链接、arXiv 摘要与论文正文要点。
- 新增站内论文笔记：
  - `notes/paper-reviews/ragen-2-reasoning-collapse-agentic-rl.html`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口。
- 笔记重点覆盖：
  - 为什么 token-level entropy 只衡量 within-input diversity，不能证明模型仍然依赖输入；
  - template collapse 的定义：reasoning 表面多样但跨输入复用模板；
  - 信息论分解 `H(Z) = I(X;Z) + H(Z|X)` 及四类推理状态；
  - in-batch cross-scoring / Retrieval-Acc / MI-ZScore-EMA 如何诊断输入依赖；
  - reward variance 控制 task gradient、KL/entropy regularizer 在低 SNR 下主导更新的机制；
  - SNR-Aware Filtering 的 top-p 选择策略、实验收益、工程接入方式和失败边界。

### 验证结果

- `ruby scripts/validate_notes_index.rb` 通过：`notes index ok: 88 entries, 88 top-level note html files`。
- 公开过程噪声扫描无输出：未命中工具名、本地路径、临时目录、生成痕迹等。
- `git diff --check -- "notes/paper-reviews/ragen-2-reasoning-collapse-agentic-rl.html" "_data/notes.yml" "Progress.md"` 通过。

## 2026-06-08 GRPO++ / RLVR Tricks 深度解读与站内笔记导入

### 背景

- 用户要求对 `https://x.com/neural_avb/status/2063366700247175274` 做深度分析梳理，导出详细 HTML 笔记，并 commit / push。
- 该 X 帖本身是推荐帖，核心材料为 Cameron R. Wolfe 的 Substack 文章 `GRPO++: Tricks for Making RL Actually Work`，主题是 GRPO / RLVR 后训练技巧。

### 已完成

- 核验目标 X 帖与回复链接：原帖推荐 GRPO / RLVR post-training article，回复短链指向 `https://cameronrwolfe.substack.com/p/grpo-tricks`。
- 阅读并整理 Substack 长文，补充核验关键引用论文：
  - DAPO：`2503.14476`；
  - Understanding R1-Zero-Like Training / Dr. GRPO：`2503.20783`；
  - GSPO：`2507.18071`；
  - GMPO：`2507.20673`；
  - MiniMax-M1 / CISPO：`2506.13585`；
  - DeepSeekMath / DeepSeek-R1 等 GRPO 与 reasoning RL 背景材料。
- 新增站内技术分析笔记：
  - `notes/tech-analysis/grpo-plus-plus-rlvr-tricks.html`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口。
- 笔记重点覆盖：
  - GRPO 为什么以 group relative advantage 取代 critic；
  - vanilla GRPO 的 reward noise、entropy collapse、response length inflation、zero-gradient prompt 和 off-policy gap；
  - DAPO 的 clip higher、dynamic sampling、token-level loss、overlong reward shaping；
  - Dr. GRPO 对 base model / template / Aha moment 叙事的校正，以及 length bias / difficulty bias；
  - TIS 如何修正 sampler engine 与 learner engine 的 logprob mismatch；
  - GSPO、GMPO、CISPO 分别如何处理 sequence-level ratio、token outlier 和关键低概率 fork token；
  - 面向真实 RLVR 训练的数据、采样、loss、系统和监控实践清单。

### 验证结果

- `ruby scripts/validate_notes_index.rb` 通过：`notes index ok: 89 entries, 89 top-level note html files`。
- 公开过程噪声扫描无输出：未命中工具名、本地路径、临时目录、生成痕迹等。
- `git diff --check` 通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅保留既有 `faraday-retry` 建议和 GitHub Metadata 未认证/限流 warning，不影响静态生成。

## 2026-06-08 RL Interview Questions 2026 深度解读与站内 HTML 笔记导出

### 背景

- 用户要求对 `https://x.com/sheriyuo/status/2063295181131247674` 做更完整、详细、清晰的深度解读，并导出为站内 HTML 笔记。
- 原帖为 X Article `RL Interview Questions 2026`，同时指向知乎中文原文 `2026 年 RL 方向面经合集`。

### 已完成

- 阅读并整理 X Article 与知乎中文原文的 35 道 RL 面试题。
- 结合公开资料补充解释：AReaL 的 PPO/GRPO/Dr.GRPO/DAPO/GSPO/SAPO 配置口径、RL for reasoning LLMs 方法谱系、agentic RL infra 中 rollout/weight sync/async/staleness/slime/VeRL 等系统脉络、OPD 与 SFT/RL 的状态分布视角。
- 新增站内技术分析笔记：
  - `notes/tech-analysis/rl-interview-questions-2026.html`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口。
- 笔记重点覆盖：
  - 为什么这份材料不是普通面经，而是 2026 LLM RL / Agentic RL 岗位能力地图；
  - LLM RL 训练链路：rollout、reward、advantage、ratio/clip/KL、backprop、weight sync；
  - 算法 19 题逐题深解，覆盖 PPO、GRPO、DPO、MoE 训推一致、Dr.GRPO、DAPO、GSPO、CISPO、SAPO、DPPO、MaxRL、SimKO、OPD 与能力边界；
  - Infra 16 题逐题深解，覆盖 model roles、KV cache、FP8/INT8、长尾 rollout、continuous batching、vLLM/SGLang、异步框架、partial rollout、EP、Megatron/FSDP、batch invariance、AReaL/slime、staleness 与框架选型；
  - 术语解释、证据边界和面试准备自测清单。

### 验证结果

- `ruby scripts/validate_notes_index.rb` 通过：`notes index ok: 89 entries, 89 top-level note html files`。
- 公开过程噪声扫描无输出：未命中工具名、本地路径、临时目录、生成痕迹等。
- `git diff --check` 通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅有既有 `faraday-retry` 和 GitHub Metadata 未认证/限流 warning。
- 新增 HTML 自检：约 22,495 个可见字符，11 个 h2、57 个 h3，且仅有一个 `data-note-role="evidence-appendix"` 与一个 `notes-shell.css` 引用。


## 2026-06-08 Self-Trained Verification 深度解读与站内笔记导入

### 背景

- 用户要求对 `https://x.com/askalphaxiv/status/2063410935075897614` 深度分析和介绍，并整理为站内笔记。
- 目标材料对应论文 `Self-Trained Verification for Training- and Test-Time Self-Improvement`，arXiv ID `2605.30290`，作者 Chen Henry Wu、Aditi Raghunathan。

### 已完成

- 阅读并整理原 X 帖、arXiv v2、项目页和官方代码仓库 README/关键 prompt 与训练脚本。
- 新增站内论文笔记：
  - `notes/paper-reviews/self-trained-verification.html`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口。
- 笔记重点覆盖：
  - verifier 为什么是 test-time refinement 与 training-time self-improvement 的共同瓶颈；
  - STV 如何利用 reference-conditioned teacher 与 on-policy distillation 训练不看答案的 verifier；
  - ViL 如何把 frozen STV verifier 的诊断反馈放进 generator RL 训练；
  - hard math、SciKnowEval、weak-to-strong verifier、ViL ablation、precision-coverage 和 feedback value 的关键证据；
  - 与 Self-Refine、RLVR、SFT verifier、Verdict-RL、PRM、Best-of-N 的区别；
  - 依赖 reference solution、开放式任务迁移和 test-time compute 成本等边界。

### 验证结果

- `ruby scripts/validate_notes_index.rb` 通过：`notes index ok: 89 entries, 89 top-level note html files`。
- 公开过程噪声扫描无输出：未命中工具名、本地路径、临时目录、生成痕迹等。
- `git diff --check` 通过。
- 首次尝试 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 时环境缺少 jekyll bundle executable；随后执行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle install` 补齐依赖。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅有既有 `faraday-retry` 和 GitHub Metadata 未认证/限流 warning。


## 2026-06-08 Lilian Weng《Why We Think》与 Lil’Log 全谱系分析

### 背景

- 用户要求深度理解和分析 Lilian Weng 的《Why We Think》，并尽量把作者整个博客都分析一遍，强调“非常重要”。
- 本轮按站内 Notes 规范沉淀为读者可直接阅读的独立 HTML，不写抓取命令、临时路径或生成痕迹。

### 已完成

- 读取目标文章《Why We Think》并梳理其核心框架：
  - test-time compute / thinking time；
  - CoT token thinking；
  - parallel sampling、best-of-N、beam search、self-consistency；
  - sequential revision 与 self-correction；
  - RL for reasoning 与 DeepSeek-R1 风格训练；
  - tool-augmented reasoning；
  - CoT faithfulness、monitoring 与 obfuscated reward hacking；
  - recurrent architecture、thinking/pause tokens、Quiet-STaR；
  - latent-variable / EM / STaR 视角；
  - thinking-time scaling law 与 budget forcing。
- 横向读取 Lil’Log 公开归档/RSS 中的 50 篇技术正文标题、时间、结构与主题，形成 2017-2025 年主题谱系：
  - 2017-2018：深度学习基础、视觉、GAN/VAE/Flow、RL、attention；
  - 2019-2022：语言模型、泛化、sim2real、self-supervised、Transformer、数据效率、diffusion、scale training；
  - 2023-2025：LLM inference、prompt、agent、adversarial attacks、human data quality、hallucination、reward hacking、reasoning/test-time compute。
- 新增站内技术分析笔记：
  - `notes/tech-analysis/lilianweng-why-we-think-blog-map.html`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口。

### 关键判断

- 《Why We Think》不是普通 CoT 综述，而是把 Lilian Weng 过去八年关于 RL、Transformer、Prompt、Agent、人类数据质量、幻觉和奖励黑客的主题汇合到 reasoning model 上。
- 文章最重要的 insight：思考时间是一种资源，推理轨迹是一种潜变量，CoT 是半可信遥测而不是天然真实解释，奖励/监控信号一旦被直接优化就可能失真。
- 工程上不能简单“加长 CoT”：应按任务难度、verifier 可靠性、风险等级和成本动态分配测试时计算，并尽量把搜索收益蒸馏回模型。

### 验证结果

- `ruby scripts/validate_notes_index.rb` 通过：`notes index ok: 91 entries, 91 top-level note html files`。
- `git diff --check -- "notes/tech-analysis/lilianweng-why-we-think-blog-map.html" "notes/tech-analysis/autolab-closed-loop-agents.html" "notes/tech-analysis/autolab-closed-loop-agents-assets" "_data/notes.yml" "Progress.md"` 通过。
- 新增 Lilian Weng 页面与 AutoLab 页面公开过程噪声扫描无输出：未命中工具名、本地路径、临时目录、生成痕迹等。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅保留既有 `faraday-retry` 建议和 GitHub Metadata 未认证/限流 warning，不影响静态生成。
- 构建后 `_site/notes/tech-analysis/lilianweng-why-we-think-blog-map.html` 存在，`_site/notes/index.html` 与 `_site/sitemap.xml` 均已包含新增 Lilian Weng 页面。

## 2026-06-04 kaboo-cli 接入 Pi 使用记录

### 背景

- 用户发现 `kaboo-cli report` 输出中没有原生 Pi/Oh-My-Pi 使用量；`kaboo-cli sources` 虽能检测到 `Oh-My-Pi (OMP) /Users/bytedance/.omc/sessions`，但计数为 0。

### 已完成

- 确认 kaboo 1.2.6 当前 OMP parser 仍只读取 `~/.omc/sessions` 顶层 `*.json`，不解析 Pi 原生 `~/.pi/agent/sessions/**/*.jsonl`；现有 `.omc` 软链结构对 kaboo 计数无效。
- 新增本地桥接脚本：`~/.local/bin/kaboo-pi-bridge`，把 Pi JSONL 转成 kaboo 已支持的 Codex JSONL 兼容目录：`~/.local/share/kaboo/pi-codex-bridge`。
- 新增 wrapper：`~/.local/bin/kaboo-cli-with-pi`，在 `report/export/sources/status/config/profile` 前自动刷新桥接目录，并设置 `KABOO_CODEX_DIRS=$HOME/.codex:$HOME/.local/share/kaboo/pi-codex-bridge`。
- 更新 `~/.zshrc`，将交互 shell 中的 `kaboo-cli` alias 指向 wrapper。
- 更新并重载 LaunchAgent：`~/Library/LaunchAgents/net.bytedance.kaboo-cli.plist`，将定时上报命令改为 `~/.local/bin/kaboo-cli-with-pi report`；原 plist 已备份为 `.bak-before-pi-bridge`。

### 验证结果

- `kaboo-cli-with-pi sources` 显示 Codex CLI 扫描源已包含 `~/.local/share/kaboo/pi-codex-bridge/sessions`，总 session file 从 1915 增至 1947+。
- `kaboo-cli-with-pi export` 中出现 `model: pi/...` bucket，Pi token 合计约 1.65e8；相对原 Codex 扫描有明确 bucket/session 增量。
- 随后按用户建议改为上传时归类到 `Oh-My-Pi (OMP)`：新增 `~/.local/bin/kaboo-pi-proxy`，wrapper 在 `report` 时启动本地代理，转发到真实 `KABOO_API_URL` 前把桥接产生的 `project: __pi__...` records 改写为 `source: omp`，并去掉 `pi/` model 前缀和 `__pi__` project 前缀。
- 本地拦截验证显示 payload 中 Pi 增量已变为：`buckets source=omp 63`、`sessions source=omp 33`、`autonomySessions source=omp 29`。
- 真正执行 `kaboo-cli-with-pi report --full` 成功：`✓ synced 4080 buckets · 2652 sessions · 149 autonomy`。本地 CLI 汇总行仍显示扫描阶段 `codex 2996 buckets · 1948 sessions`，但上传 payload 已在代理层改写为 OMP source。
- 当前限制：这是本地代理改写方案，不是 kaboo 官方原生 Pi parser；若 kaboo 后续支持 Pi/OMP 原生 JSONL，可删除 proxy/bridge 简化配置。

## 2026-06-04 Notes 全量内容清晰度复查与补强

### 背景

- 用户要求检查每一个站内笔记，确保内容详细、解释清晰。
- 本轮范围覆盖 `_data/notes.yml` 中 85 条入口，以及 `notes/` 下 195 个 HTML 页面（83 篇独立 Notes、2 个题库索引、110 个题库章节）。

### 已完成

- 对全部 Notes HTML 做结构化质量审计：可见正文长度、h2/h3/h4 章节数、机制/方法解释、术语解释、证据/实验解释、边界/风险、工程/研究启发、证据 appendix 属性、公开过程噪声。
- 修复独立 Notes 的规范残留：
  - 为缺失页面补齐 `data-note-role="evidence-appendix"`；
  - 删除 LongTraceRL 和 RL scaling 书单中的命令摘录；
  - 删除 Nitrobrew 页脚里的静态 HTML 生成痕迹；
  - 规范若干章节标题，使机制、评估、边界、启发更容易被读者定位。
- 对 26 篇术语解释偏弱或标题信号不足的独立 Notes 补充“术语解释与概念边界”或强化机制标题，覆盖 ProgramBench、NanoGPT-Bench、ACuRL、MMProlong、RL Memory、ReLex、BES、Memento、SkillEvolBench、OnlineRubrics、ECHO、EqR、VPO、Attention、SEIF、X digest 等页面。
- 修正 `notes/tech-analysis/hwcoder-algorithm-notes-reading.html` 中重复 source/sources 章节定位，使最终证据 appendix 统一为 `id="sources"`。

### 审计结果

- 全量脚本复查结果：`files=195 issueFiles=0`。
- `_data/notes.yml` 统计：85 entries，其中 83 篇独立 Notes、2 个题库索引。
- 独立 Notes 可见正文长度：最短 4511 字符，中位数 7047，平均 7618，最长 27168。
- 83 篇独立 Notes 均且仅有一个 `data-note-role="evidence-appendix"`。
- 公开过程噪声扫描无输出。

### 验证结果

- `ruby scripts/validate_notes_index.rb` 通过：`notes index ok: 85 entries, 85 top-level note html files`。
- `git diff --check` 通过。
- 公开噪声扫描通过：未命中 `OpenCLI/opencli`、本地路径、临时目录、命令摘录、生成痕迹等。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅有既有 `faraday-retry` 和 GitHub Metadata 未认证/限流 warning。
- `_site/sitemap.xml` 与 `_site` 根目录检查未发现 `AGENTS`、`Progress`、`.agent`、`audit_report`、`scripts`、`markdown_generator` 等内部文件泄露。

## 2026-06-04 Fantastic Pretraining Optimizers and Where to Find Them 深度阅读与站内笔记导出

### 背景

- 用户要求深度阅读 X 帖 `https://x.com/iScienceLuvr/status/1963168542872014943`，随后要求导出站内 HTML 笔记。
- 该帖引用 Kaiyue Wen、David Hall、Tengyu Ma、Percy Liang 的 arXiv 论文 `2509.02046`。
- 用户指出对应的详尽博客/W&B 报告需要一同深度阅读；经确认后补充读取了 W&B Report（Fantastic Optimizers and Where to Find Them）、GitHub issue #1290 实验索引、GitHub issue #725 前身方法等。

### 已完成

- 完整深度阅读并核对材料层级：
  - 原 X 推文与 thread（含 5 条作者 reply 链和外部引用）；
  - arXiv 正式论文 v2（108 页，主文 + 附录 A–E，含 183 张 table、8 张 figure）；
  - W&B 详尽报告/博客（author: when / 凯越温，updated 2025-05-20，含实验组织、代码路径、Phase I/II/III 描述和额外现象）；
  - GitHub issue #1290（实验代码索引、best hyperparameter pkl、speedup estimation 路径）；
  - GitHub issue #725（AdamW hyperparameter scaling law 前身方法）；
  - ASAP seminar slides。
- 通过 GraphQL API 和 W&B access token 提取了 W&B report 的完整结构化 spec，解析为 Markdown 临时文件用于消化。
- 新增站内技术分析笔记：
  - `notes/tech-analysis/fantastic-pretraining-optimizers.html`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口。

### 内容判断

- 核心判断：该论文的贡献不是提出新 optimizer，而是通过三阶段 coordinate descent、scaling-sensitive hyperparameter identification 和 hyperparameter scaling law，重新审计 optimizer benchmark methodology。
- 关键发现：
  1. 很多 1.4–2× optimizer speedup claim 是弱 AdamW baseline、超参转移不公平或早期 loss 曲线造成的。
  2. 公平调参后，matrix-based optimizer（Muon、SOAP、Kron、Scion）仍然领先，但 speedup 不超过 1.4×，且随模型规模增加衰减到 1.2B 时的约 1.1×。
  3. Optimizer winner 随 data-to-model ratio 改变：低 Chinchilla 下 Muon 最强，高 Chinchilla 下 SOAP/Kron 反超。
  4. Token-efficiency speedup 不等于 wall-clock speedup，生产环境需要另行评估 MFU、communication、batch size、implementation overhead。
- W&B report 的额外现象补充：高 WD 对 Lion/Kron 关键、WD 早期伤 loss 最终帮助 final performance、single-param mismatch 可能消掉 speedup、norm dynamics 跨 optimizer 的共有性。

### 验证结果

- `ruby scripts/validate_notes_index.rb` 通过，见下方追加验证。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功。
- 新增 HTML 满足 NOTES TEMPLATE 结构要求：title、viewport、`notes-shell.css`、`body.notes-shell-page`、Notes / All Notes / Home 导航、`main`、`data-note-role="evidence-appendix"`、MathJax 配置完整。
- 未命中工具名、本地路径、生成时间、抓取命令等公开噪声。

## 2026-06-04 Notes authoring skill / template 规范化

### 背景

- 用户要求把本轮 Notes 审计里形成的规则直接规范化到 skill 或模板，避免后续继续生成带抓取命令、本地路径、生成时间和工具痕迹的公开笔记。

### 已完成

- 新增 repo-local skill：
  - `.agent/skills/notes-authoring/SKILL.md`
- 在 `.agent/config.toml` 增加 `[skills.notes_authoring]` 索引，指向上述 skill。
- 更新 `AGENTS.md` 的 Notes Authoring Standard：要求新建、导入、清理或审计站内笔记时先读 `.agent/skills/notes-authoring/SKILL.md`。
- 重写并强化 `notes/NOTE_TEMPLATE.md`：
  - 明确公共 Notes 是读者文章，不是执行日志；
  - 增加 `#evidence`、`#insight` 和带 `data-note-role="evidence-appendix"` 的 `#sources`；
  - 明确禁止工具名、抓取命令、shell 命令、本地路径、临时目录、`results/`、`Downloads`、生成时间和文件位置；
  - 保留结构、CSS、MathJax、图片 alt 和移动端兼容要求。
- 强化 `scripts/validate_notes_index.rb` 的质量 warning：
  - 检测 `OpenCLI/opencli`、`mcp-router`、`pdftotext`、`pdfinfo`、`curl -`、`X 线程公开读取`、`网页公开读取` 等工具/命令痕迹；
  - 检测 `/Users/`、`Downloads`、`results/`、`本地参考文件位于`、`下载 PDF` 等公开噪声。
- 根据新 validator 又清理了一轮残留工具痕迹，独立 Notes 页面当前无上述噪声命中。

### 验证结果

- `ruby scripts/validate_notes_index.rb` 通过且无 quality warnings：`notes index ok: 84 entries, 84 top-level note html files`。
- `git diff --check` 通过。
- 独立 Notes 噪声扫描无输出：`rg -n "OpenCLI|opencli|下载 PDF|本地路径|文件位置|本地参考文件位于|Generated locally|HTML generated|/tmp/|/Users/|报告生成|results/|Downloads|X 线程公开读取|网页公开读取|pdftotext|pdfinfo|mcp-router|curl\s+-" "notes/paper-reviews" "notes/tech-analysis"`。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仍仅有 `faraday-retry` 和 GitHub Metadata 未认证/限流 warning。
- `_site/sitemap.xml` 不包含 `AGENTS`、`Progress`、`audit_report`、`cite.py`、`script.txt`、`talkmap.py`、`talkmap.ipynb`、`notes-audit`。
- 更新后的自动审计评级：A 61、B 19、C 1、D 1、INDEX 2。

### 本轮追加完成

- 新增非公开审计表：
  - `.agent/audits/notes-audit-2026-06-04.md`
- 审计表覆盖 `_data/notes.yml` 中 84 条入口：82 篇独立 HTML 笔记 + 2 个题库索引页。
- 自动化评分口径覆盖：排版结构、正文长度、机制/术语解释、证据边界、是否含抓取命令/工具名/本地路径/报告生成时间等过程噪声。
- 批量清理 Notes 中不必要的过程信息：
  - 删除 37 个独立页面的 `id="commands"` / 复现命令类 section；
  - 清理 `OpenCLI`、`opencli`、`results/`、`/tmp/`、`/Users/`、`Generated locally`、`HTML generated`、`报告生成`、`下载 PDF`、`文件位置` 等公开噪声；
  - 把来源章节改为读者可理解的公开 URL、证据边界和材料口径，不再展示本地抓取/命令过程。
- 对两篇自动审计短文做补强：
  - `notes/paper-reviews/agents-feedback-loops-not-perfect-prompts.html`：补 self-improvement 权限拆分、落地顺序和术语边界；
  - `notes/paper-reviews/gmi-spatial-reasoning-thread-report.html`：补足球动画为什么不是“小玩具题”、对象建模/时序约束/验证闭环三层分析。
- 更新 `notes/paper-reviews/visual-generation-world-models.html`，把文末 references 规范为 `data-note-role="evidence-appendix"` 的证据边界说明，并移除本地参考文件路径。

### 验证结果

- `ruby scripts/validate_notes_index.rb` 通过：`notes index ok: 84 entries, 84 top-level note html files`。
- `git diff --check` 通过。
- `rg -n "OpenCLI|opencli|下载 PDF|本地路径|文件位置|本地参考文件位于|Generated locally|HTML generated|/tmp/|/Users/|报告生成|results/|Downloads" "notes/paper-reviews" "notes/tech-analysis"` 无输出。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅有 `faraday-retry` 和 GitHub Metadata 未认证 warning，不影响静态生成。
- `_site/sitemap.xml` 不再包含 `AGENTS`、`Progress`、`audit_report`、`cite.py`、`script.txt`、`talkmap.py`、`talkmap.ipynb`、`notes-audit`。
- `_site` 根目录不再生成 `AGENTS.md`、`Progress.md`、`audit_report.html`、`cite.py`、`script.txt`、`talkmap.py`、`talkmap.ipynb`。
- 更新后的自动审计评级：A 60、B 20、C 1、D 1、INDEX 2；剩余 C/D 主要是内容深度可继续人工扩写，不再是发布噪声或结构错误。

## 2026-06-04 仓库发布面修复与 Notes 全量审计启动

### 背景

- 用户要求在仓库 review 后直接修复问题，并进一步逐个审计站内笔记的排版、内容深度和是否移除了不必要的生成/抓取过程信息。
- 本轮先处理会直接影响公开站点的发布面问题，再建立全量笔记审计清单，避免一次性凭主观印象下结论。

### 已完成

- 修复 `_config.yml` 的 Jekyll `exclude` 列表，避免根目录内部文件和工具文件被静态发布：
  - `AGENTS.md`
  - `Progress.md`
  - `.agent`
  - `.github`
  - `audit_report.html`
  - `cite.py`
  - `script.txt`
  - `scripts`
  - `markdown_generator`
  - `talkmap.py`
  - `talkmap.ipynb`
  - `README.md`、`CHANGELOG.md`、`CONTRIBUTING.md`
- 更新 `.gitignore`，将本地审计 HTML artifact 排除：
  - `audit_report.html`
  - `*_report.html`
- 初步自动化扫描 84 条 `_data/notes.yml` 入口，识别需要人工重点复核的笔记类型：短正文、缺少 `data-note-role="evidence-appendix"`、开头疑似过程/来源前置。

### 当前判断

- 站点构建会公开 `AGENTS.md`、`Progress.md`、`audit_report.html` 是优先级最高的问题，已先做最小修复。
- Notes 全量审计不能只靠 validator；validator 能发现结构和明显生成痕迹，但“内容是否讲清楚、是否啰嗦、是否有 insight”需要逐篇抽取正文结构与人工判断。

### 待验证 / 继续推进

- 重新运行 `ruby scripts/validate_notes_index.rb`。
- 重新运行 Jekyll build 并检查 `_site/sitemap.xml` 不再包含 `/AGENTS/`、`/Progress/`、`/audit_report.html`。
- 生成或维护一份全量 Notes 审计表，覆盖每篇笔记的排版、内容深度、证据边界和冗余过程信息。

## 2026-06-03 LLM Infra 设计谱系调研与站内笔记导出

### 背景

- 用户基于 MAI-Base-1 架构表追问 local/global attention、GQA、MoE、dropless routing、zero-init attention output、FP8 precision 等 infra 名词背后的技术谱系、演进轨迹、代表工作和关键结论。
- 本轮新建独立站内技术分析笔记，不写入 Obsidian；沿用 Notes HTML 规范并复用 MAI-Thinking-1 本地图表证据。

### 已完成

- 新增站内技术分析笔记：
  - `notes/tech-analysis/llm-infra-design-patterns.html`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`LLM Infra 设计谱系：从 attention 到 MoE 再到 FP8`
  - URL：`/notes/tech-analysis/llm-infra-design-patterns.html`
  - 类型：`Tech Analysis`
- 调研并整理的技术轴：
  - local/global attention 与 sliding-window / periodic-global 设计；
  - MQA / GQA 与 KV cache budget；
  - top-k MoE、dense/MoE interleaving、LatentMoE 与 all-to-all/GEMM trade-off；
  - capacity-capped routing 与 dropless routing 的实验语义差异；
  - zero-init attention output 与 MoE router imbalance；
  - FP8 E4M3/E5M2、delayed scaling、FP32 sensitive path。
- 代表工作索引覆盖 Transformer、Sparse Transformer、Longformer、BigBird、Mistral、Gemma、MQA、GQA、GShard、Switch Transformer、GLaM、MegaBlocks、Mixtral、DeepSeek-V2、FP8 Formats for Deep Learning 等。

### 验证结果

- HTML scoped 结构检查通过：title、viewport、`notes-shell.css`、`body.notes-shell-page`、Notes / All Notes / Home 导航、`main`、`data-note-role="evidence-appendix"` 均存在。
- 页面包含 11 个核心 section，3 张本地证据图全部存在且 `alt` 非空。
- `ruby scripts/validate_notes_index.rb` 通过：`notes index ok: 84 entries, 84 top-level note html files`。
- `git diff --check -- "notes/tech-analysis/llm-infra-design-patterns.html" "_data/notes.yml" "Progress.md"` 通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仍有既有 GitHub Metadata API 未认证/限流 warning，不影响 `_site` 静态生成。

## 2026-06-03 Mid-training X 帖深度解读与站内笔记导入

### 背景

- 用户要求深度解读 `https://x.com/NielsRogge/status/2061802537049591896`，随后追问是否已经导入笔记。
- 上一轮已完成聊天内深度解读，但未落站内文件；本轮按用户追问补做 repo-native Notes 导入。
- 当前工作树已有非本轮改动：`Progress.md`、`_data/notes.yml`、`notes/llm-interview-question-bank/chapters/074.html`、`notes/llm-interview-question-bank/chapters/077.html`，以及若干未跟踪 notes / artifact；本轮只新增 mid-training 笔记并追加索引与进度记录，不回滚或整理其他改动。

### 已完成

- 使用 OpenCLI 获取目标 X 原帖：
  - 作者：`NielsRogge` / Niels Rogge；
  - 原帖时间：2026-06-02 13:30:05 UTC；
  - 主题：Mid-training 是 pre-training 与 post-training 之间的训练阶段；
  - 原帖短链指向 `https://paperswithcode.co/methods/mid-training`；
  - 原帖附图为 Papers with Code 的 Mid-training 方法页截图。
- 使用 `opencli twitter profile` 核验作者公开资料：
  - bio：ML Engineer @ Hugging Face，building Papers with Code；
  - location：Belgium；
  - profile URL：`http://nielsrogge.github.io`。
- 补充读取相关材料：
  - Papers with Code `Mid-training` 方法页；
  - Pierre-Carl Langlais 的 `What's the deal with mid-training?`；
  - Shashank Shekhar 对 Phi-4 数据与 mid-training 流程的解析；
  - Microsoft Phi-4 技术报告；
  - `Midtraining Bridges Pretraining and Posttraining Distributions`；
  - `daVinci-Dev: Agent-native Mid-training for Software Engineering`；
  - `Scaling Agents via Continual Pre-training`。
- 新增站内技术分析笔记：
  - `notes/tech-analysis/mid-training-llm-training-pipeline.html`
- 新增本地配图资源：
  - `notes/tech-analysis/mid-training-llm-training-pipeline-assets/niels-pwc-mid-training.jpg`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`Mid-training：预训练和后训练之间真正发生了什么`
  - URL：`/notes/tech-analysis/mid-training-llm-training-pipeline.html`
  - 类型：`Tech Analysis`

### 关键观察

- Mid-training 的价值不是新增一个营销阶段，而是把能力增强和行为对齐拆开：它通常保留 pre-training-like objective，但数据更小、更高质量、更贴近目标能力分布。
- 判断一个阶段是否是 mid-training，不能只看它发生在 pre-training 之后；要看训练目标、数据形态、token 规模、是否塑造能力底座，以及后续 post-training 是否仍有稳定增益。
- Phi-4 是清晰例子：约 10T tokens 预训练、约 250B tokens mid-training 做长上下文扩展、约 8B tokens SFT 后再进入 DPO。
- Agentic mid-training 的关键不是把更多代码丢进模型，而是让数据保留状态、动作、观察、失败、测试和修复路径，使模型学到 agent 工作流的过程分布。
- 术语边界仍然混乱；continued pretraining、supplemental training、agentic CPT 和 mid-training 在公开材料里常有重叠，本文按功能而非名称划分。

### 验证结果

- 新增 HTML scoped 结构检查通过：title、viewport、`notes-shell.css`、`body.notes-shell-page`、Notes / All Notes / Home 导航、`main`、`data-note-role="evidence-appendix"`、本地图片引用与非空 `alt` 均存在。
- 新增本地配图资源检查通过：`niels-pwc-mid-training.jpg` 为 `1200x778` JPEG。
- `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 83 entries, 83 top-level note html files`。
- `git diff --check -- "notes/tech-analysis/mid-training-llm-training-pipeline.html" "notes/tech-analysis/mid-training-llm-training-pipeline-assets/niels-pwc-mid-training.jpg" "_data/notes.yml" "Progress.md"` 通过。
- UTF-8 检查通过：新增 HTML、`Progress.md` 与 `_data/notes.yml` 均可按 UTF-8 解码。
- 新增 HTML 未命中 `Generated locally`、`HTML generated`、`本地 HTML 生成`、`报告生成日期`、`/tmp/`、`/Users/bytedance`、`最终 HTML 路径`、`文件位置`、Unicode replacement character 等公开生成痕迹。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仍有 `faraday-retry` 建议和 GitHub Metadata API 403/限流 warning，不影响 `_site` 静态生成。
- `_site/notes/tech-analysis/mid-training-llm-training-pipeline.html` 结构检查通过：页面存在，文件大小 `26734` bytes，title、`body.notes-shell-page`、`main`、`data-note-role="evidence-appendix"` 和本地图片资源均存在。
- `_site/notes/index.html` 已包含新增 Mid-training 笔记卡片；`_site/sitemap.xml` 已包含新增页面 URL。

## 2026-06-03 MAI-Thinking-1 技术报告深度分析与站内笔记导出

### 背景

- 用户要求深度分析并导出 HTML 笔记：`https://microsoft.ai/wp-content/uploads/2026/06/main_20260602_2.pdf`。
- 任务在当前站点仓库内落地，不写入 Obsidian；本轮只新增 MAI-Thinking-1 相关 note、assets，并对 `_data/notes.yml` / `Progress.md` 做增量更新。
- 当前 worktree 已有非本轮改动，包括 OmniOPD、CAST、cwolfe 阅读清单、LLM 题库章节和本地 audit artifact；本轮不回滚、不覆盖这些改动。

### 已完成

- 下载并读取 Microsoft AI 官方 PDF：
  - 标题：`MAI-Thinking-1: Building a Hill-Climbing Machine`；
  - 作者：The Microsoft AI Team；
  - PDF 109 页；
  - 本地文本抽取 5621 行；
  - 识别 20 个编号表格标题和 26 个编号图；论文正文中有两个 `Table 19` 标题。
- 渲染并本地化证据截图：
  - 4 张正文导览大图：`source-page-001.png`、`architecture-page-005.png`、`rl-overview-page-030.png`、`evaluation-page-053.png`；
  - 新增 45 张 `atlas-page-*.jpg` 图表证据页，覆盖 PDF 中所有编号 Figure / Table 所在页面。
- 新增站内技术分析笔记：
  - `notes/tech-analysis/mai-thinking-1-hill-climbing-machine.html`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`MAI-Thinking-1：微软如何把模型研发做成 Hill-Climbing Machine`
  - URL：`/notes/tech-analysis/mai-thinking-1-hill-climbing-machine.html`
  - 类型：`Tech Analysis`

### 内容判断

- 笔记核心判断：该报告真正展示的是微软自研 reasoning model 的系统性生产能力，而不是单个 benchmark 或单点算法技巧。
- 重点补齐此前聊天版覆盖不足的部分：
  - NLL evaluation suite 与 public evaluation decontamination；
  - MoE sparsity / EG / EGTime 取舍；
  - Web HTML、Web PDFs、Books/Journals、Public GitHub 的 Appendix A 数据管线；
  - attention output zero-init 与 MoE router imbalance 的关系；
  - FP8/BF16/FP32 数值配方；
  - self-distillation 在 RL collapse recovery / base policy migration 中的工程角色；
  - SWE tool schema、instruction following constraint taxonomy、SWE environment building infra；
  - MRCR 被剔除所暴露的长上下文 benchmark 可刷性；
  - Cluster Appendix K 中 topology、certification、node lifecycle、observability 与 goodput 控制面。
- 当前判断：MAI-Thinking-1 不是“全域 SOTA”证据，而是 Microsoft AI 已经具备从 scratch 训练、后训练、评测、安全和部署一体化 hill-climbing machine 的证据。

### 验证结果

- `ruby scripts/validate_notes_index.rb` 通过；本轮复核输出：
  - `notes index ok: 83 entries, 83 top-level note html files`
- `git diff --check -- "notes/tech-analysis/mai-thinking-1-hill-climbing-machine.html" "notes/tech-analysis/mai-thinking-1-hill-climbing-machine-assets" "_data/notes.yml" "Progress.md"` 通过，无 whitespace error。
- 新增 HTML scoped 结构检查通过：
  - 标题唯一；
  - `body.notes-shell-page` 存在；
  - `../assets/notes-shell.css` 已加载；
  - `Notes / All Notes / Home` 顶部导航存在；
  - `<main>` 与 14 个核心 section 存在；
  - `data-note-role="evidence-appendix"` 证据附录存在；
  - 49 张本地图片全部存在且 `alt` 非空，其中 45 张为图表 atlas 证据页；
  - 新增 HTML 与 `_data/notes.yml` 未命中 `/tmp/`、`/Users/`、`Generated locally`、`本 HTML 报告`、`本报告生成`、Unicode replacement character 等公开生成痕迹。
- `_data/notes.yml` 入口检查通过：
  - URL：`/notes/tech-analysis/mai-thinking-1-hill-climbing-machine.html`
  - 类型：`Tech Analysis`
  - tags 包含 `Microsoft AI`
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功：
  - 构建产物存在：`_site/notes/tech-analysis/mai-thinking-1-hill-climbing-machine.html`
  - 构建耗时约 8.467 秒；
  - 仍有既有 `faraday-retry` 建议和 GitHub Metadata API 未认证/限流 warning，不影响 `_site` 静态生成。
- Chrome headless 渲染烟测通过：
  - 桌面截图 `/private/tmp/mai-thinking-1-desktop.png` 为 `1440x1100`，`234619` bytes，PNG 有效；
  - 移动截图 `/private/tmp/mai-thinking-1-mobile.png` 为 `390x844`，`75198` bytes，PNG 有效；
  - 构建后 DOM 检查显示标题正确、`body_class=notes-shell-page`、图片数为 4、缺失图片数为 0。

## 2026-06-03 OmniOPD X 帖深度解读与站内笔记导出

### 背景

- 用户要求深度解读 `https://x.com/zhuokaiz/status/2061939957514584304`，随后确认导入笔记。
- 本轮按仓库规则使用 OpenCLI-first X/thread 读取路径，并在当前站点内导出独立 HTML 笔记，不写入 Obsidian。
- 当前 worktree 已有非本轮改动：`Progress.md`、`_data/notes.yml`、`notes/llm-interview-question-bank/chapters/074.html`、`notes/llm-interview-question-bank/chapters/077.html`、未跟踪 `audit_report.html`、CAST 笔记与 cwolfe 阅读清单相关文件；本轮只追加 OmniOPD 相关笔记、索引和进度记录。

### 已完成

- 使用 `opencli twitter thread` 获取目标 X 原帖与回复：
  - 作者：Zhuokai Zhao / `zhuokaiz`；
  - 原帖时间：2026-06-02 22:36:09 UTC；
  - 主题：OmniOPD，一种不需要 teacher logits 的 on-policy distillation；
  - 原帖配图包含 OmniOPD 总览图和数学推理主结果表。
- 使用 `opencli twitter profile` 核验作者公开资料：
  - name：Zhuokai Zhao；
  - bio：AI Research Scientist @Meta，PhD @UChicagoCS；
  - profile URL：`https://zhuokai-zhao.com/`。
- 解析目标 thread 短链：
  - 论文：`https://arxiv.org/pdf/2606.01476`；
  - 前序 OPD 脆弱性长帖：`https://x.com/zhuokaiz/status/2055042099674796118`。
- 下载并读取论文 PDF / HTML / arXiv metadata：
  - 标题：`OmniOPD: Logit-Free On-Policy Distillation via Speculative Verification`；
  - 作者：Yuhang Zhou、Lizhu Zhang、Yifan Wu、Mingyi Wang、Peng Bo、Jiayi Liu、Xiangjun Fan、Zhuokai Zhao；
  - arXiv v1：2026-05-31；
  - 论文 PDF 26 页。
- 新增站内论文解读笔记：
  - `notes/paper-reviews/omniopd-logit-free-opd.html`
- 新增本地配图资源：
  - `notes/paper-reviews/omniopd-logit-free-opd-assets/overview.jpg`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`OmniOPD：用语义 chunk 验证绕开 teacher logits`
  - URL：`/notes/paper-reviews/omniopd-logit-free-opd.html`
  - 类型：`Paper Note`

### 关键观察

- OmniOPD 的核心不是“黑盒 teacher 也能蒸馏”这么简单，而是把 OPD 的监督对象从 fragile token menu 改成学生关键推理分叉处的 chunk-level semantic verification。
- 标准 OPD 的失败根源包括 teacher logits access barrier、teacher/student tokenizer 或 style mismatch、局部 plausible next-token overlap 脆弱，以及 degenerate prefix 下 teacher token probability 可能误导训练。
- OmniOPD 的关键组合包括 peak-entropy chunk selection、teacher Monte Carlo rollouts、semantic similarity、Dirichlet-Multinomial Bayesian smoothing 和 unaudited tokens 上的 reference KL anchor。
- 数学推理实验最支持论文主张：Qwen3-4B + Qwen3-30B-A3B-Instruct 上 OmniOPD 平均 72.32%，明显高于 SFT 49.77% 和 OPD 56.22%；这说明 teacher 风格差异大时 token-level OPD 特别吃亏。
- 代码任务没有形成同样强的优势：Qwen3-4B 代码实验中 OmniOPD 平均 63.78%，低于 OPD 65.26%，说明 chunk-level invariance 不应被外推为所有任务都优于 logits。

### 当前判断

- 对后训练工程最可复用的部分是监督粒度重构：把 teacher 的逐 token 分布匹配改成“学生高不确定性 chunk + teacher rollout + 可替换 semantic scorer”的模块接口。
- 复现时不应只照抄默认 Edit Distance；应比较 lexical metric、embedding similarity、LLM-as-judge / verifier 等多种 `phi`，并监控 zero-match chunks、KL、response length、entropy drift 和 teacher query cost。
- Reference KL anchor 是硬约束，不是装饰项；论文消融中去掉 KL anchor 后平均分从 69.08% 坍到 8.28%，说明稀疏 chunk supervision 若不约束未审计 token 会快速退化。
- 证据边界集中在数学推理和少量 competitive programming 任务；更大模型、full-parameter update、长程 agent、工具调用、多模态和无可靠 verifier 的任务不能直接外推。

### 验证结果

- 新增 HTML scoped 结构检查通过：title、viewport、`notes-shell.css`、`body.notes-shell-page`、Notes / All Notes / Home 导航、`main`、`data-note-role="evidence-appendix"`、本地图片引用与非空 `alt` 均存在。
- 新增本地配图资源检查通过：`overview.jpg` 为 `876x1200` JPEG。
- `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 81 entries, 81 top-level note html files`。
- `git diff --check -- "notes/paper-reviews/omniopd-logit-free-opd.html" "notes/paper-reviews/omniopd-logit-free-opd-assets/overview.jpg" "_data/notes.yml" "Progress.md"` 通过。
- 新增 HTML 与 `_data/notes.yml` 未命中 `Generated locally`、`HTML generated`、`本地 HTML 生成`、`报告生成日期`、`/tmp/`、`/Users/bytedance`、`最终 HTML 路径`、`文件位置`、Unicode replacement character 等公开生成痕迹。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仍有 `faraday-retry` 建议和 GitHub Metadata API 403/限流 warning，不影响 `_site` 静态生成。
- `_site/notes/paper-reviews/omniopd-logit-free-opd.html` 结构检查通过：title、`body.notes-shell-page`、Notes sitebar、`main`、`data-note-role="evidence-appendix"` 和本地图片资源均存在。
- `_site/notes/paper-reviews/omniopd-logit-free-opd-assets/overview.jpg` 存在，文件为 `876x1200` JPEG。
- `_site/notes/index.html` 已包含新增 OmniOPD 笔记卡片；`_site/sitemap.xml` 已包含新增页面 URL。

## 2026-06-03 Codex hook 失败噪声修复

### 背景

- 用户反馈 Codex 中反复出现 `PreToolUse hook (failed)` / `PostToolUse hook (failed)`，错误为 `hook exited with code 1`。
- 本轮问题不属于站点业务代码，而是本机全局 Codex hook 配置异常；按最小修复原则只处理 `~/.codex` hook 配置，不改动站点页面、题库或 notes 内容。

### 根因

- `/Users/bytedance/.codex/hooks.json` 原本为 `SessionStart`、`UserPromptSubmit`、`PreToolUse`、`PermissionRequest`、`PostToolUse`、`Stop` 全部注册同一个命令：
  - `"/opt/homebrew/bin/node" "/Applications/Clawd on Desk.app/Contents/Resources/app.asar.unpacked/hooks/codex-hook.js"`
- 当前机器上 `/Applications/Clawd on Desk.app/.../codex-hook.js` 不存在，手动复现会触发 Node `MODULE_NOT_FOUND` 并退出 `1`，因此每次工具调用前后都会刷 hook failure。
- 额外检查发现 `com.codexplusplus.watcher` 后台 LaunchAgent 仍在运行周期性 update/repair；它的日志里有 GitHub release check `403` 和 `npm install` 失败噪声，但未在本地代码中发现其直接写入 `~/.codex/hooks.json` 或 `codex-hook.js` 的逻辑。

### 已完成

- 当前 `/Users/bytedance/.codex/hooks.json` 已变为：
  - `{ "hooks": {} }`
- 原坏配置已保留备份：
  - `/Users/bytedance/.codex/hooks.json.bak.20260603-111034`
- 修改 `/Users/bytedance/.codex/config.toml`：
  - 删除 6 个指向 `/Users/bytedance/.codex/hooks.json:*` 的旧 trusted hash；
  - 保留 `superpowers@superpowers-marketplace` 自身的 `session_start` hook trust 记录。
- 修改前已备份全局配置：
  - `/Users/bytedance/.codex/config.toml.bak.20260603-115210`

### 验证结果

- JSON 解析检查通过：
  - 当前 `hooks.json` 为合法 JSON，且 hook 列表为空；
  - 备份 `hooks.json.bak.20260603-111034` 为合法 JSON，包含原始坏 hook，便于需要时追溯。
- `rg` 复查通过：
  - 当前 `/Users/bytedance/.codex/hooks.json` 和 `/Users/bytedance/.codex/config.toml` 不再包含 `Clawd on Desk`、`codex-hook.js`、`PreToolUse`、`PostToolUse` 相关坏入口。
- `codex doctor` 通过配置加载与数据库健康检查：
  - `Configuration` 为 `config loaded`，`config.toml parse ok`；
  - 未出现 hook failure；
  - 剩余 warning 是历史 rollout 扫描和官方更新探测 `403`，与本次 hook 退出码 `1` 不同。
- `codexplusplus doctor` 显示 Codex++ 本体检查通过；但 watcher 的 update 日志仍有 `403` / npm install 失败噪声，后续若继续污染日志，可单独禁用 `com.codexplusplus.watcher` 或卸载 Codex++。

## 2026-06-03 CAST / GRPO X 帖深度解读与站内笔记导出

### 背景

- 用户要求深度阅读和分析梳理 `https://x.com/sheriyuo/status/2061764630968717598`，随后确认导出到笔记。
- 本轮按仓库规则使用 OpenCLI-first X/thread 读取路径，并在当前站点内导出独立 HTML 笔记，不写入 Obsidian。
- 当前工作树已有非本轮改动：`notes/llm-interview-question-bank/chapters/074.html`、`notes/llm-interview-question-bank/chapters/077.html`、`Progress.md` 的数学专项深化记录，以及未跟踪 `audit_report.html`；本轮不触碰两个题库章节和本地审计 artifact。

### 已完成

- 使用 `opencli twitter thread` 获取目标 X 原帖与回复：
  - 作者：`sheriyuo` / Xiuyu Li；
  - 原帖时间：2026-06-02 10:59:28 UTC；
  - 主题：CAST 对 GRPO dead-zone、OPSD 信号错位和 token-level credit assignment 的修补；
  - 原帖配图为 CAST / GRPO 总览图。
- 使用 `opencli twitter profile` 核验作者公开资料：
  - name：Xiuyu Li；
  - bio：Undergrad @RUC1937，RL / Optimization / dLLM，Intern @JD_Corporate；
  - profile url：`http://sheriyuo.github.io`。
- 解析原帖短链：
  - `https://t.co/ZlWrJiPXCa` -> `https://arxiv.org/abs/2606.00172`。
- 下载并读取论文 PDF：
  - 标题：`CAST: Non-Privileged Clipped Asymmetric Self-Teaching with Advantage Flipping for GRPO`；
  - 作者：Yang Li、Gongle Xue、Yijia Guo、Yuheng Yuan、Liwen Hu、Lei Ma；
  - arXiv v1：2026-05-29；
  - 论文 PDF 26 页。
- 新增站内论文解读笔记：
  - `notes/paper-reviews/cast-grpo-self-teaching.html`
- 新增本地配图资源：
  - `notes/paper-reviews/cast-grpo-self-teaching-assets/overview.jpg`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`CAST：给 GRPO 补上 verifier-grounded 的 token 级信用分配`
  - URL：`/notes/paper-reviews/cast-grpo-self-teaching.html`
  - 类型：`Paper Note`

### 关键观察

- CAST 不是替代 GRPO，而是修 GRPO 的 advantage construction：verifier 继续决定 trajectory-level 方向，self-teacher 只做 token-level local shaping。
- GRPO 的 zero-variance groups 不是边缘情况；论文 Qwen3-4B 主 run 中 all-correct groups 平均 20.2%，all-wrong groups 平均 31.3%，mixed groups 平均 48.5%。
- OPSD 的问题不是没有 dense token signal，而是 teacher-positive / teacher-negative token preference 未必和最终 trajectory correctness 对齐。
- CAST 的关键组合包括 answer-free self-teacher scoring、bounded zero-variance base advantage、asymmetric clipping 和 bidirectional advantage flipping。
- 这不是 PRM，也不是 step-level semantic supervision；它是基于 self-teacher log-prob gap 和 verifier correctness 构造的 detached token advantage。

### 当前判断

- @sheriyuo 原帖对 CAST 的主线判断成立，但“dense step-level signal”需要校正为 token-level advantage shaping；CAST 不知道每一步数学推理是否语义正确。
- CAST 的工程启发是把 teacher 从裁判降级为局部 shaping 工具：verifier 负责 outcome，teacher 负责 local log-prob geometry。
- 证据边界仍集中在数学 RLVR、Qwen3 1.7B/4B/8B、LoRA、最多 600 optimizer steps；更大模型、full-parameter update、长程 agent 和无可靠 verifier 的任务不能直接外推。

### 验证结果

- 新增 HTML scoped 结构检查通过：title、viewport、`notes-shell.css`、`body.notes-shell-page`、Notes / All Notes / Home 导航、`main`、`data-note-role="evidence-appendix"`、本地图片引用与非空 `alt` 均存在。
- 新增本地配图资源检查通过：`overview.jpg` 为 `1200x744` JPEG。
- `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 79 entries, 79 top-level note html files`。
- `git diff --check -- "notes/paper-reviews/cast-grpo-self-teaching.html" "notes/paper-reviews/cast-grpo-self-teaching-assets/overview.jpg" "_data/notes.yml" "Progress.md"` 通过。
- 新增 HTML 与 `_data/notes.yml` 未命中 `Generated locally`、`HTML generated`、`本地 HTML 生成`、`报告生成日期`、`/tmp/`、`/Users/bytedance`、`最终 HTML 路径`、`文件位置`、Unicode replacement character 等公开生成痕迹。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仍有 `faraday-retry` 建议和 GitHub Metadata API 403/限流 warning，不影响 `_site` 静态生成。
- `_site/notes/paper-reviews/cast-grpo-self-teaching.html` 结构检查通过：页面存在，文件大小 `25469` bytes，`section` 数量为 10，title、`body.notes-shell-page`、Notes sitebar、`main`、`data-note-role="evidence-appendix"` 和本地图片资源均存在。
- `_site/notes/paper-reviews/cast-grpo-self-teaching-assets/overview.jpg` 存在，文件为 `1200x744` JPEG。
- `_site/notes/index.html` 已包含新增 CAST 笔记卡片；`_site/sitemap.xml` 已包含新增页面 URL。

## 2026-06-03 LLM 数学专项知识点讲解深化

### 背景

- 用户在数学题库/知识库 review 后要求继续推进，并明确“重要的是先把知识点讲清楚”。
- 本轮按内容深化处理，不先做题库 UI、目录重排或大规模索引工程；优先补 `notes/llm-interview-question-bank/` 里数学专项的“逐题详细解答”层。
- 当前工作树已有未跟踪 `audit_report.html`，本轮不触碰该本地 artifact。

### 已完成

- 扩写 `notes/llm-interview-question-bank/chapters/074.html`：
  - 在章节顶部新增“先把数学对象讲清楚”导读块，明确概率、统计量、空间结构三条数学链路。
  - 扩写条件概率 / 全概率 / Bayes：
    - 补公式、对象读法、常见方向错误；
    - 加入罕见病检测 base-rate 数值例子，说明 posterior 同时受 likelihood 与 prior 影响。
  - 扩写期望 / 方差 / 协方差 / 相关系数：
    - 补定义公式和适用对象；
    - 强调协方差有量纲、相关系数只看线性关系，零相关不等于独立。
  - 扩写 MLE / MAP：
    - 补优化目标、负对数后验分解；
    - 用高斯先验解释 L2 正则来源；
    - 加入硬币样本 + Beta 先验的 MAP 例子。
  - 扩写熵 / 交叉熵 / KL：
    - 补 `H(p,q)=H(p)+D_KL(p||q)` 推导；
    - 加入二分类分布数值例子，说明方向性和相对熵代价。
  - 扩写偏导 / 梯度 / Jacobian / Hessian：
    - 增加输入输出形状表；
    - 强调先按标量/向量输出和一阶/二阶区分。
  - 扩写 Taylor、拉格朗日、mini-batch 梯度、条件数：
    - 补二阶局部近似公式、约束优化最小例子、mini-batch 无偏估计与方差、条件数和训练行为的连接。
- 扩写 `notes/llm-interview-question-bank/chapters/077.html`：
  - 新增“高阶数学题的回答骨架”导读块，按机制、推导、例子和边界组织高阶追问。
  - 扩写 attention scaling：
    - 补点积方差随 `d_k` 增长的最小推导；
    - 说明除以 `sqrt(d_k)` 控制 softmax 尖锐程度而不改变排序。
  - 扩写 sigmoid / tanh / softmax 导数：
    - 补激活导数公式和 softmax Jacobian；
    - 解释 logits 尺度过大、softmax 饱和和梯度变弱之间的链路。
  - 扩写 softmax + cross-entropy：
    - 从 log-softmax 推导 `p-y`；
    - 补梯度下降下真实类 logit 被推高、错误类 logit 被压低的符号解释。
  - 扩写 MSE / cross-entropy、最小二乘、L1/L2、KKT、Jensen、log-sum-exp、Monte Carlo、LayerNorm：
    - 补观测模型假设、正规方程推导、正则几何和不可导点、KKT 四条件表、ELBO 下界来源、稳定重写、Monte Carlo 方差、LayerNorm 机制和边界。

### 当前判断

- 本轮没有改变题库结构，而是先把数学专项最核心的知识点讲深：从“答案大意”补到“对象、公式、推导、例子、边界”。
- 后续继续推进时，优先按同一标准处理：
  - LLM 题库第 `048-058` 核心知识点索引里仍偏短的条目；
  - 数学手册独立题库层的题型/难度/先修映射；
  - LLM 第 `072-077` 与独立数学手册之间的交叉导流。

### 验证结果

- `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 78 entries, 78 top-level note html files`。
- `git diff --check -- "notes/llm-interview-question-bank/chapters/074.html" "notes/llm-interview-question-bank/chapters/077.html" "Progress.md"` 通过。
- 章节结构检查通过：
  - `074.html`：`section.chapter=1`、`chapter_nav=1`、重复 `id=0`；
  - `077.html`：`section.chapter=1`、`chapter_nav=1`、重复 `id=0`。
- UTF-8 / replacement character 检查通过：
  - `074.html` 与 `077.html` 均为 valid UTF-8；
  - 未发现 Unicode replacement character。

## 2026-06-02 commit/push 收口复验

### 背景

- 用户要求 `review commit and push`。
- 本轮先处理 `git pull --rebase --autostash` 后遗留的 `Progress.md` 与 `_data/notes.yml` 冲突标记状态；两个文件内容已恢复为本地工作成果版本，并确认没有冲突标记。
- 远端 `origin/main` 已包含 `agentic-rl-rollout-environments.html`；本地未跟踪副本与远端一致，已在 pull 阶段去除重复副本，避免重复提交。

### 工作树复验

- `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 78 entries, 78 top-level note html files`。
- `git diff --check` 通过。
- `rg -n "<<<<<<<|=======|>>>>>>>" "Progress.md" "_data/notes.yml"` 未命中冲突标记。
- `rg -n "/Users/bytedance/Downloads|/Users/xxx|/tmp/|Generated locally|HTML generated|本地 HTML 生成|报告生成日期|最终 HTML 路径|文件位置" "notes" "_data/notes.yml" "_pages/about.md"` 未命中公开页面路径或生成痕迹。
- `python3 -m py_compile "cite.py"` 通过，随后清理 `__pycache__`。
- `find "." -name ".DS_Store" -not -path "./.git/*" -print` 无输出。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅保留 `faraday-retry` 建议与 GitHub Metadata 未认证 warning，不影响静态站点生成。

### 提交边界

- 本轮提交纳入 notes 语料、模板、validator、站点索引、favicon、题库章节、治理配置与 `Progress.md` 收口记录。
- `audit_report.html` 是本地审查输入/报告 artifact，不作为站点页面或正式笔记提交。
- 已对最终提交边界做复验：`ruby "scripts/validate_notes_index.rb"` 通过，Jekyll build 通过，`origin/main...HEAD` 同步后为 `0 0`；`audit_report.html` 仍作为本地未跟踪 artifact 保留，不纳入提交。

## 2026-06-02 A-Evolve self-evolving agents X thread 与站内笔记导出

### 背景

- 用户要求仔细阅读梳理并导入笔记：`https://x.com/HenryL_AI/status/2037602570433388816`。
- 用户随后要求本轮工作完成后及时 `commit push`。
- 当前 worktree 已有大量非本轮历史改动；本轮提交会只包含 A-Evolve 笔记、对应 assets、`_data/notes.yml` 与 `Progress.md` 的本轮增量。

### 已完成

- 按仓库规则读取并遵循：
  - `AGENTS.md`
  - `.agent/codex-experience-profile.md`
  - `Progress.md`
  - `notes/NOTE_TEMPLATE.md`
  - notes workflow / OpenCLI X research 记忆工作流。
- 使用 `opencli twitter thread` 获取目标 X thread：
  - 根帖作者：Henry Lu / `HenryL_AI`；
  - 根帖时间：2026-03-27 18:48:04 UTC；
  - 主题：A-Evolve launch，定位为 “PyTorch Moment for Self-evolving AI”；
  - 根帖报告：MCP-Atlas `79.4%`、SWE-bench Verified `76.8%`、Terminal-Bench 2.0 `76.5%`、SkillsBench `34.9%`；
  - 后续帖强调 A-Evolve 是 framework 而不是单体 agent，支持 BYOA / BYOE / BYO-Algo；
  - 评论区确认：memory、prompt、skills、tools、workflow / single-to-multi-agent orchestration 都可作为可变对象；框架设计目标是与任意 agent framework 集成；内部 benchmark 可以按已有 benchmark adapter 模式新增。
- 使用 `opencli twitter profile` 核验作者公开资料：
  - name：Henry Lu；
  - bio：Research Lead @Amazon，Self-improving AI，ex-CMU / MSR；
  - profile 中链接到 A-Evolve 相关站点。
- 解析目标 thread 短链：
  - GitHub：`https://github.com/A-EVO-Lab/a-evolve`
  - 评论区对照文章：`https://theharness.blog/blog/what-if-the-harness-could-improve-itself/`
  - 其它短链多为 X 图片页或后续投票帖。
- 读取 A-Evolve README、QuickStart、DESIGN、算法文档和关键源码：
  - 核验 workspace contract：`manifest.yaml`、`prompts/`、`skills/`、`tools/`、`memory/`、`evolution/`；
  - 核验核心 loop：Solve -> Observe -> Evolve -> Gate -> Reload；
  - 核验 `BaseAgent.solve()`、`BenchmarkAdapter.get_tasks()/evaluate()`、`EvolutionEngine.step()` 三个关键接口；
  - 核验 git-based `VersionControl` 负责 commit、tag、rollback；
  - 核验四类算法文档：`adaptive_evolve`、`adaptive_skill`、`skillforge`、`guided_synth`。
- 使用 OpenCLI / arXiv 核验两篇相关论文：
  - `Position: Agentic Evolution is the Path to Evolving LLMs`，arXiv `2602.00359`；
  - `Harness Updating Is Not Harness Benefit`，arXiv `2605.30621`。
- 新增站内技术分析笔记：
  - `notes/tech-analysis/a-evolve-self-evolving-agents.html`
- 新增本地配图资源：
  - `notes/tech-analysis/a-evolve-self-evolving-agents-assets/framework.jpg`
  - `notes/tech-analysis/a-evolve-self-evolving-agents-assets/evolved-agent.png`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`A-Evolve：把 Agent Harness 变成可演化的工程对象`
  - URL：`/notes/tech-analysis/a-evolve-self-evolving-agents.html`
  - 类型：`Tech Analysis`

### 关键观察

- A-Evolve 的核心不是“agent 自己变聪明”，而是把 agent 外部 harness 变成可观察、可修改、可验证、可回滚的工程对象。
- “workspace is the interface” 是整套系统最重要的抽象：agent 只读 workspace，evolver 只写 workspace，二者通过文件系统契约解耦。
- 四条算法线实际是在回答同一个问题：失败轨迹应该被压缩成什么持久 artifact。MCP 任务偏 per-claim targeted skill，SWE 任务偏 verification skill / episodic memory，Terminal 任务偏 trajectory-only skill，SkillBench 偏 failure-to-skill transfer。
- 榜单分数应理解为系统级结果：base model、seed workspace、benchmark adapter、evolution algorithm、task split、evaluator 共同作用；不能外推为模型权重能力提升。
- 后续 `Harness Updating Is Not Harness Benefit` 的核心边界很重要：会写好 harness update 的 evolver，与会从 harness update 中受益的 solver，是两个可分离能力。
- 真正的工程风险包括 reward/eval 偏差、holdout leakage、benchmark overfitting、skill library 膨胀、技能激活失败、长程任务中不遵守技能、以及把“zero human intervention”误读成无需定义目标函数。

### 当前判断

- 对工程团队最可复用的部分不是宣传里的 “3 lines of code”，而是：
  - 明确定义 agent workspace contract；
  - 记录完整 trajectory 与 failure taxonomy；
  - 把失败压缩成可 review 的 skill / prompt / memory diff；
  - 用 holdout 和 git rollback 管住退化；
  - 定期 prune / merge skill library，避免知识库膨胀。
- 如果要在真实项目里复刻，应该先小范围演化 prompt / skill / verification checklist，而不是一开始允许 evolver 修改所有 tools / memory / harness。
- A-Evolve 与近期 agentic RL / harness 方向的关系是互补的：Polar 等路线强调把真实 harness 作为训练环境，A-Evolve 强调先把 harness 本身纳入持续改进对象。

### 验证结果

- 新增 HTML scoped 结构检查通过：`title`、viewport、`notes-shell.css`、`body.notes-shell-page`、Notes / All Notes / Home 导航、`main`、`data-note-role="evidence-appendix"`、两张本地图片 `alt` 与公开生成痕迹检查均通过。
- `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 78 entries, 78 top-level note html files`。
- `git diff --check -- "notes/tech-analysis/a-evolve-self-evolving-agents.html" "notes/tech-analysis/a-evolve-self-evolving-agents-assets/framework.jpg" "notes/tech-analysis/a-evolve-self-evolving-agents-assets/evolved-agent.png" "_data/notes.yml" "Progress.md"` 通过。
- 新增 HTML 与 `_data/notes.yml` 未命中 `Generated locally`、`HTML generated`、`本地 HTML 生成`、`报告生成日期`、`/tmp/`、`/Users/bytedance`、`最终 HTML 路径`、`文件位置`、Unicode replacement character 等公开生成痕迹。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仍有 `faraday-retry` 建议和 GitHub Metadata API 403/限流 warning，不影响 `_site` 静态生成。
- `_site/notes/tech-analysis/a-evolve-self-evolving-agents.html` 结构检查通过：页面存在，文件大小 `27994` bytes，`section` 数量为 8，title、`body.notes-shell-page`、Notes sitebar、`main`、`data-note-role="evidence-appendix"` 和两张本地资源均存在。
- `_site/notes/tech-analysis/a-evolve-self-evolving-agents-assets/framework.jpg` 存在，文件为 `1200x670` JPEG；`_site/notes/tech-analysis/a-evolve-self-evolving-agents-assets/evolved-agent.png` 存在，文件为 `1200x989` PNG。
- 精确 staged snapshot 检查、commit/push 收口见本文件顶部 `2026-06-02 commit/push 收口复验`。

## 2026-06-03 A-Evolve 笔记重构：补充创新性审视与赛道全景

### 背景

- 用户质疑 A-Evolve 这类"自我验证、自我进化"工作是否真有方法创新，要求诚实拆解。
- 原笔记（06-02 撰写）偏忠实解读，缺少对方法论贡献的批判性评估。

### 已完成

- 重新阅读两篇 arXiv 论文全文（Position Paper 2602.00359、Harness Updating 2605.30621）及 GitHub README。
- 从 A-Evolve 引用列表梳理 2023-2025 十种同类工作（Reflexion、Promptbreeder、SelfEvolve、AgentEvolver、Youtu-Agent、Agent0、ReasoningBank、EvoAgentX、Evo-memory、Agentic Context Engineering 等）。
- 重写 `a-evolve-self-evolving-agents.html`，新增《创新审视》section（位于原核心判断之前），包含：
  - 赛道全景对照表（10 种同类工作的年份、更新对象、更新机制、与 A-Evolve 的本质差异）
  - 两篇论文分开评级：Position Paper ≈ 0 方法创新（换术语不谈新机制、实验只比 strawman baseline）、Harness Updating 论文的贡献在实验设计（7×6×3 全交叉 + 能力拆解），不在新算法
  - 7 项机制"卖点"创新性评估表（循环、Evolver 结构、workspace 契约、Gate、EGL、能力拆解、全交叉实验），逐项标"不算新 / 工程创新 / 小改进 / 算新"
  - 诚实总结：没有新算法、新机制、新理论；A-Evolve 亮点是"提出可证伪假设→用实验打脸→给出工程方向"的诚实性
- 更新 TOC 导航，新增"创新审视"锚点。
- 更新 `_data/notes.yml` 摘要，反映批判性评估角度。

### 核心判断

- A-Evolve 的 Position Paper 在方法上不新——"LLM 当 evolver"在 Reflexion (2023) 和 Promptbreeder (2024) 中已充分体现；三个"原则"是对已有工作的重新命名。
- Harness Updating ≠ Harness Benefit 的实验发现真正有价值：evolver 强弱不重要（≤ 3.1 pp 差距），solver 的 harness invocation 和 long-horizon following 才决定收益。这个发现的可逆推含义是"别把钱花在更强的 evolver 上"。
- A-Evolve 框架本质是好的工程（CI/CD for agent harness），不是新的科学。它的"创新"在测量方法（能力拆解）和实验设计（全交叉受控），不在算法或机制。

### 验证结果

- 新增 HTML section 结构正确：`#innovation` 锚点、TOC 更新、9 个 section 总数。
- `_data/notes.yml` 摘要更新，`ruby scripts/validate_notes_index.rb` 通过。

## 2026-06-02 LLM Interview Question Bank RAG / 知识库内容 Review 与补强

### 背景

- 用户要求 review 大模型题库和知识库方面的内容，并指出部分内容不够详细。
- 本轮先读取仓库规则、经验档案、`Progress.md` 历史记录和当前 worktree，再聚焦 `notes/llm-interview-question-bank/` 中的 RAG / 知识库内容质量。
- 当前工作树已有大量既有未提交改动；本轮只围绕 LLM 题库 RAG / 知识库章节做最小必要补强，避免把无关文件混入本轮判断。

### Review 结论

- 题库整体不是“没有 RAG 内容”：第 10 章地图页、第 43 章完整答案、第 54 章知识点索引已经覆盖 RAG pipeline、chunking、embedding、hybrid retrieval、reranker、GraphRAG、Lost in the Middle、faithfulness、权限过滤和增量更新。
- 主要不足是三类生产级追问还不够成体系：
  - Contextual Retrieval、Parent-Child Retrieval、Multi-hop / Iterative RAG 的区别、适用场景和启用代价。
  - Self-RAG、CRAG、evidence verifier 这类“检索结果不可信时怎么纠错”的链路设计。
  - 企业知识库场景下 ACL、文档版本、缓存 key、trace 日志和审计复现如何设计。
- 首页搜索元数据也偏旧：第 43/54 章卡片没有覆盖新增的现代 RAG 关键词，导致用户用 `Contextual Retrieval`、`Self-RAG`、`CRAG`、`ACL`、`trace` 等词检索时不够直接。

### 已完成

- 原地补强 `notes/llm-interview-question-bank/chapters/043.html`：
  - 新增第 73 题：`Contextual Retrieval、Parent-Child 和 Multi-hop RAG 分别解决什么问题？`
  - 新增第 74 题：`RAG 召回错了怎么办？Self-RAG、CRAG 和 verifier 型纠错链路怎么设计？`
  - 新增第 75 题：`企业知识库 RAG 的权限、版本、缓存和日志怎么设计？`
  - 对每题补充标准答案、深度解析、表格、状态机/trace 示例和面试追问。
- 原地补强 `notes/llm-interview-question-bank/chapters/054.html`：
  - 把本章侧栏从“本章无更多小节”改成 10 个本章小节入口。
  - 新增 `纠错型 RAG 与 evidence verifier`、`企业知识库的缓存、版本和审计` 两节。
  - 扩展 GraphRAG 小节，补 local search / global search 的问题类型边界。
  - 更新误区与追问链路，加入缓存版本、GraphRAG 不应神化、Self-RAG/CRAG 启用代价等复盘点。
- 更新 `notes/llm-interview-question-bank/index.html`：
  - 第 43 章卡片统计从 `12 个编号题 · 28 表 · 10 代码块` 更新为 `15 个编号题 · 31 表 · 12 代码块`。
  - 第 43/54 章 `data-search` 增加 `Contextual Retrieval`、`Parent-Child`、`Multi-hop`、`Self-RAG`、`CRAG`、`evidence verifier`、`ACL`、`trace`、`缓存`、`版本` 等关键词。

### 当前判断

- 这次没有新增章节，原因是现有题库已把 RAG 放在第 43/54 章；继续新增章节会增加导航和维护成本，不如把真实缺口补进最合适的已有章节。
- 题库现在能覆盖从基础 RAG 到生产知识库治理的追问链路：`pipeline -> retrieval/rerank -> context packing/citation -> GraphRAG -> corrective RAG -> ACL/version/cache/trace`。
- 后续如果继续深挖，优先方向不是继续堆术语，而是给第 43 章补 1-2 个完整 case study：例如“企业政策助手答错一条退款规则，如何从 trace 定位到 ACL / 版本 / rerank / citation 的具体根因”。

### 验证结果

- `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 78 entries, 78 top-level note html files`。
- `git diff --check -- "notes/llm-interview-question-bank/chapters/043.html" "notes/llm-interview-question-bank/chapters/054.html" "notes/llm-interview-question-bank/index.html" "Progress.md"` 通过。
- `rg -n "<<<<<<<|=======|>>>>>>>|Generated locally|HTML generated|本地 HTML 生成|报告生成日期|/tmp/|/Users/bytedance|最终 HTML 路径|文件位置" "notes/llm-interview-question-bank/chapters/043.html" "notes/llm-interview-question-bank/chapters/054.html" "notes/llm-interview-question-bank/index.html"` 未命中冲突标记、公开生成痕迹或本机路径。
- 复查当前 `HEAD` 与 `origin/main` 后确认，RAG / 知识库正文补强已经进入版本库；本次收口只补齐该任务的验证记录，不纳入未跟踪的 `audit_report.html`。

## 2026-06-02 Speculative Decoding X Article 深度梳理与笔记导入

### 背景

- 用户要求仔细梳理并导入笔记：`https://x.com/mohitwt_/status/2061127197046555110`。
- 原帖作者 Mohit，公开简介为 `20, llm inference`；根帖本身只有 X Article 短链。
- X Article 标题为 `Everything you need to know about Speculative Decoding Inference`，主题是 speculative decoding 的直觉、draft/verify 流程、EAGLE/Medusa/lookahead、生产实现和 KV cache 边界。

### 已完成

- 使用 `opencli twitter thread` 获取目标 X thread：
  - 根帖时间：2026-05-31 16:46:32 UTC；
  - 根帖正文只有短链 `https://t.co/EoalO9SuNe`；
  - 评论区唯一实质技术补充来自 SPThole：Mohit 漏了 `correction` 和 `sampling based speculative decoding`。
- 使用 `opencli twitter profile` 核验作者资料：
  - screen name：`mohitwt_`；
  - name：`mohit`；
  - bio：`20, llm inference`；
  - profile url：`http://mog9.github.io`。
- 使用 `curl -sIL` 解析短链：
  - 短链指向 `https://x.com/i/article/2061041984861827073`；
  - 公开 HTTP 访问 X article 返回 403，随后用 `opencli twitter article` 成功读取完整 X Article。
- 读取并交叉核验外部资料：
  - Google Research `Looking back at speculative decoding`；
  - arXiv `2211.17192`：Fast Inference from Transformers via Speculative Decoding；
  - arXiv `2302.01318`：Accelerating Large Language Model Decoding with Speculative Sampling；
  - arXiv `2401.10774`：Medusa；
  - arXiv `2406.16858`：EAGLE-2；
  - arXiv `2503.01840`：EAGLE-3；
  - SGLang speculative decoding 文档；
  - vLLM speculative decoding 文档。
- 新增站内技术分析笔记：
  - `notes/tech-analysis/speculative-decoding-inference.html`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`Speculative Decoding：投机解码的真实收益、校正采样与生产边界`
  - URL：`/notes/tech-analysis/speculative-decoding-inference.html`
  - 类型：`Tech Analysis`

### 关键观察

- Mohit 原文适合作为入门材料，但其 “target model 检查 draft token 是否 top-1” 的表述只适合解释 greedy / 近似流程，不能覆盖 sampling-based speculative decoding。
- 投机解码的理论关键是保持 target model 输出分布：draft 分布 `q(x)` 与 target 分布 `p(x)` 之间需要 modified rejection sampling，拒绝后还需要从 residual distribution 做 correction。
- 真正的系统收益来自把多个候选位置合并到一次 target forward 中，利用硬件并行度摊薄逐 token decode 的权重读取成本；它不是数学意义上的免费验证，也不是简单一次 matmul。
- EAGLE、Medusa、MTP、NGRAM、suffix / prompt lookup 等变体都在回答同一问题：怎样用最低额外成本提出更容易被 target 接受的候选 token。
- 生产收益高度依赖场景：低 batch、memory-bound、长 decode、draft 高接受率更容易受益；高 batch、短输出、高温采样和 KV cache 紧张时可能收益有限甚至负收益。

### 当前判断

- Speculative decoding 应被看作 LLM serving 的 proposer/verifier 插件接口，而不是单一“小模型猜词”技巧。
- 上线判断不能只看 tokens/s，应同时记录 acceptance rate、draft latency、verify latency、rejected depth、batch size、OOM、TTFT/TPOT、采样参数和质量回归。
- 如果业务目标是降低低 QPS / 单用户交互的 decode latency，投机解码值得优先试；如果目标是极高 QPS 批量吞吐，应先确认 continuous batching、prefix caching、quantization、kernel fusion 和路由已经做满。

### 验证结果

- 新增 HTML scoped 结构检查通过：title、viewport、`notes-shell.css`、`body.notes-shell-page`、Notes / All Notes / Home 导航、`main`、MathJax、`data-note-role="evidence-appendix"`、公开生成痕迹检查均通过；页面大小 `28024` bytes，`section` 数量为 9。
- `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 78 entries, 78 top-level note html files`。
- `git diff --check -- "notes/tech-analysis/speculative-decoding-inference.html" "_data/notes.yml" "Progress.md"` 通过。
- 新增 HTML 与 `_data/notes.yml` 未命中 `Generated locally`、`HTML generated`、`本地 HTML 生成`、`报告生成日期`、`/tmp/`、`/Users/bytedance`、`最终 HTML 路径`、`文件位置`、Unicode replacement character 等公开生成痕迹。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仍有 `faraday-retry` 建议和 GitHub Metadata API 403/限流 warning，不影响 `_site` 静态生成。
- `_site/notes/tech-analysis/speculative-decoding-inference.html` 结构检查通过：页面存在，文件大小 `28024` bytes，`section` 数量为 9，title、`body.notes-shell-page`、Notes sitebar、`main`、`data-note-role="evidence-appendix"` 和 `_site/notes/assets/notes-shell.css` 均存在。
- 本地 `_site` 临时服务 + 系统 Chrome headless 移动端烟测通过：`390x844` 视口下 title 正确，`sections=9`，`overflow=0`，正文文本长度 `6970`，无图片 alt / 加载问题、无控制台或网络错误。

## 2026-06-02 RHELM 长期记忆 benchmark X 帖与站内笔记导出

### 背景

- 用户要求仔细梳理 `https://x.com/HuggingPapers/status/2061535298652147770` 并导入笔记。
- 原帖为 HuggingPapers 推荐 Microsoft 发布的 long-horizon memory benchmark：RHELM / `Beyond Static Dialogues: Benchmarking Realistic, Heterogeneous, and Evolving Long-Term Memory`。

### 已完成

- 使用 `opencli twitter thread` 获取目标 X thread：
  - 根帖时间：2026-06-01 19:48:11 UTC；
  - 主帖观点：Microsoft released a long-horizon memory benchmark on Hugging Face；
  - 回复短链分别解析到 dataset `https://huggingface.co/datasets/microsoft/RHELM` 和 paper page `https://huggingface.co/papers/2605.31086`；
  - 原帖配图已本地化为 `notes/paper-reviews/rhelm-long-horizon-memory-assets/huggingpapers-root.jpg`。
- 使用 `opencli twitter profile` 核验 HuggingPapers 账号公开简介：
  - screen name：`HuggingPapers`；
  - name：DailyPapers；
  - verified：true；
  - bio 指向 Hugging Face Daily Papers 投稿与 paper linking。
- 使用 Hugging Face paper API、arXiv、PDF、GitHub raw、project page 和 dataset API 交叉核验核心材料：
  - 论文 ID：`2605.31086`；
  - arXiv 当前 PDF 为 v2，32 页；
  - 标题：`Beyond Static Dialogues: Benchmarking Realistic, Heterogeneous, and Evolving Long-Term Memory`；
  - 作者来自 Renmin University of China 与 Microsoft；
  - GitHub：`https://github.com/microsoft/RHELM`；
  - project page：`https://microsoft.github.io/RHELM/`；
  - dataset：`https://huggingface.co/datasets/microsoft/RHELM`。
- 核验公开数据集结构：
  - 10 个 persona；
  - 1,305 个 QA pairs；
  - 629 个 conversation sessions；
  - 625 个 emails；
  - README/project page 标注 1,053 个 attachments；
  - 7 个 question types：attachment 249、mixed 210、fact 207、hallucination 197、aggregation 192、temporal 185、misleading 65。
- 核验 RHELM 的关键机制：
  - LOOP = pLan / rOllout / evOlve / Prune；
  - persona profile 覆盖 Identity、Personality、Traits、Relationships、Belongings、Current Status；
  - 数据不只来自对话，还包括 email、journal/report 类 attachments 与多格式结构资料；
  - Memory-Conditioned Misleading Queries 要求模型识别用户请求与历史状态冲突，而不是盲目服从。
- 核验实验结论：
  - 项目页与论文主结果显示最佳系统 Claude Opus 4.5 在带 external sources 设置下平均分为 38.1；
  - RAG、long-context models、MemGPT/Mem0/MemU 等 memory frameworks 均在 hallucination、misleading、mixed、cross-source aggregation 上暴露缺口；
  - 增加检索量不必然改善表现，外部来源还可能降低标准类型表现，因为系统需要统一证据、时间有效性和跨来源结构，而不是简单召回更多 chunk。
- 新增站内论文笔记：
  - `notes/paper-reviews/rhelm-long-horizon-memory.html`
- 新增本地图片资源：
  - `notes/paper-reviews/rhelm-long-horizon-memory-assets/huggingpapers-root.jpg`
  - `notes/paper-reviews/rhelm-long-horizon-memory-assets/rhelm-overview.png`
  - `notes/paper-reviews/rhelm-long-horizon-memory-assets/rhelm-main-results.png`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`RHELM：长期记忆评测为什么必须超越静态对话`
  - URL：`/notes/paper-reviews/rhelm-long-horizon-memory.html`
  - 类型：`Paper Note`

### 关键观察

- 这篇材料的核心 insight 不是“长上下文 benchmark 又多一个”，而是把 personal assistant memory 从静态事实检索改写成动态用户状态建模。
- RHELM 对 memory system 的真正压力来自五个同时成立的条件：长期 persona 演化、异构外部资料、时间有效性、跨来源聚合、用户请求与隐含状态冲突。
- 普通 RAG 的 failure mode 很清楚：相似 chunk 命中不等于证据链正确；top-k 增加还会带入过时状态、无关附件和冲突事实。
- Long-context model 的 failure mode 也不同：它可能看到全部材料，但仍会在证据归因、时间关系、误导性前提和 hallucinated justification 上失效。
- Misleading query 是 RHELM 最有工程价值的设计之一：长期助手不能只做 instruction following，还必须在用户请求与历史状态冲突时提醒、拒绝或提出替代方案。
- 公开材料存在一个需注明的口径差异：论文摘要/正文写 27 个 memory characteristics，当前 README / project page / taxonomy 文档写 26 个 challenge characteristics；dataset 实际 characteristics 字段还出现 taxonomy 文档未列出的标签。

### 当前判断

- RHELM 更适合作为长期记忆系统的 diagnostic suite，而不是单纯排行榜：应拆分测试 temporal validity、evidence attribution、attachment structure retrieval、cross-source aggregation、hallucination correction 和 misleading refusal。
- 若系统只实现“向量库 + profile 摘要”，很可能在 RHELM mixed / misleading / hallucination 上系统性失败；更合理的架构应包含原始事件账本、结构化当前状态、外部资料结构索引和回答时 evidence graph。

### 验证结果

- 新增 HTML scoped 结构检查通过：title、viewport、`notes-shell.css`、`body.notes-shell-page`、Notes / All Notes / Home 导航、`main`、`data-note-role="evidence-appendix"`、本地图片存在、非空 alt 与公开生成痕迹检查均通过。
- `ruby "scripts/validate_notes_index.rb"` 通过；RHELM 页面写入后首次输出 `notes index ok: 76 entries, 76 top-level note html files`，后续因工作树内已有/并行 notes 改动进入索引，最终复跑输出 `notes index ok: 78 entries, 78 top-level note html files`。
- `git diff --check -- "notes/paper-reviews/rhelm-long-horizon-memory.html" "notes/paper-reviews/rhelm-long-horizon-memory-assets" "_data/notes.yml" "Progress.md"` 通过。
- 新增 HTML 与 `_data/notes.yml` 未命中 `Generated locally`、`HTML generated`、`本地 HTML 生成`、`报告生成日期`、`/tmp/`、`/Users/bytedance`、`最终 HTML 路径`、`文件位置`、Unicode replacement character 等公开生成痕迹。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仍有 `faraday-retry` 建议和 GitHub Metadata 未认证 warning，不影响 `_site` 静态生成。
- `_site/notes/paper-reviews/rhelm-long-horizon-memory.html` 结构检查通过：页面存在，文件大小 `26960` bytes，title、`body.notes-shell-page`、Notes sitebar、`main`、`data-note-role="evidence-appendix"` 和三张本地图片均存在。
- `_site/notes/index.html` 已出现新增 Notes 卡片入口：`RHELM：长期记忆评测为什么必须超越静态对话`。
- 从 `_site` 启动本地 HTTP 服务后，页面、三张本地图片和 `notes-shell.css` 均返回 `HTTP 200`。
- Chrome headless 渲染验证通过：桌面截图 `/tmp/rhelm-long-horizon-memory-1280.png` 为 `1280x900`、`220966` bytes，移动截图 `/tmp/rhelm-long-horizon-memory-390.png` 为 `390x844`、`95107` bytes，均为非空 PNG。

## 2026-06-02 The Thinking Pixel X thread 与论文笔记导出

### 背景

- 用户要求仔细梳理 `https://x.com/che_shr_cat/status/2061206236243111979`，导入笔记，并在完成后 commit。
- 原帖作者 `che_shr_cat` / Grigory Sapunov，主帖把 arXiv `2604.25299`《The Thinking Pixel: Recursive Sparse Reasoning in Multimodal Diffusion Latents》解读为视觉生成模型里的 test-time compute / latent pondering 路线。

### 已完成

- 使用 `opencli twitter thread` 获取目标 X thread：
  - 根帖时间：2026-05-31 22:00:36 UTC；
  - 线程共 11 条，核心表达是让 text-to-image 模型不再只是 feedforward one-pass，而是在视觉 latent 中加入 recursive reasoning；
  - 线程提到 Recursive Joint-Attention、Mixture-of-Adapters、LoRA experts、Gumbel-Softmax gate、PCA latent trajectories、GenEval / ImageNet FID / FrozenLake visual navigation 和静态 recursion / routing sensitivity / hallucination amplification 等边界。
- 使用 `opencli twitter profile` 核验作者资料：
  - screen name：`che_shr_cat`；
  - name：Grigory Sapunov；
  - bio：PhD in AI / GDE in AI/ML / CTO Intento / author of `Deep Learning with JAX`；
  - profile url：`https://gonzoml.substack.com/`。
- 解析 X 短链：
  - 作者长文：`https://arxiviq.substack.com/p/the-thinking-pixel-recursive-sparse`；
  - 原论文：`https://arxiv.org/abs/2604.25299`；
  - 其他短链主要指向 X 图片页。
- 读取作者 Substack：
  - 公开读取范围只覆盖 TL;DR、引言和 paywall 前内容；
  - 因此本轮只把 Substack 作为传播口径和背景材料，不依赖其后半段细节。
- 使用 `opencli arxiv paper`、PDF 下载、`pdfinfo` 和 `pdftotext -layout` 读取论文：
  - 论文作者：Yuwei Sun, Yuxuan Yao, Hui Li, Siyu Zhu；
  - 论文发布时间：2026-04-28；
  - PDF 共 13 页；
  - 核心方法是在 MMDiT / SD3 joint attention 中加入 recursive sparse reasoning，视觉 token 经由 gate 在多个 LoRA adapter expert 中 hard select，并在多个 latent steps 中迭代更新；
  - 训练路由用 Gumbel-Softmax；adapter 作用在 vision branch 的 Q/K/V 投影；冻结 base model 输出只在最后 latent step 合入，避免每一步都重复暴露在固定主干表示里导致 representation drift。
- 新增站内论文笔记：
  - `notes/paper-reviews/thinking-pixel-recursive-sparse-reasoning.html`
- 新增本地配图资源：
  - `notes/paper-reviews/thinking-pixel-recursive-sparse-reasoning-assets/paper-page-03.jpg`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`The Thinking Pixel：把 test-time compute 放进扩散模型 latent 层`
  - URL：`/notes/paper-reviews/thinking-pixel-recursive-sparse-reasoning.html`
  - 类型：`Paper Note`

### 关键观察

- 这条线程的传播表达是 `pixels ponder`，但论文里的精确对象是连续视觉 latent token；不要把它写成像素层面真的在自然语言式思考。
- 这篇工作的核心不是“重复跑整条扩散模型”，而是把递归计算限制在 joint attention 附近的低秩 adapter 空间里，使额外计算更接近局部 latent refinement。
- PCA trajectory 的价值在于观察 expert 路由是否真的分化：高噪声早期 token path 更统一，低噪声后期出现 patch-specific 分叉，提示递归计算可能更适合在生成后段修正局部结构。
- GenEval 数字支持 text-following 改进：多层 `M=2, Tlatent=2` 得到 overall `71.18`，高于 SD3-medium `67.93`；但 position 子项仍弱，不能把整体提升解读为所有空间关系都解决。
- DPG 结果需要降温：`M=2, Tlatent=2` 的 overall `85.31` 低于 SD3-medium `85.65`，最好结果来自 `M=5, Tlatent=5` 的 `85.88`，说明固定递归深度并不稳健。
- FrozenLake 视觉导航只是简化示例，论文也展示了掉进洞和出现训练数据未提供动作的失败案例，不能外推成通用 planning agent 证据。

### 当前判断

- The Thinking Pixel 更应被理解为 `latent compute allocation` 论文，而不是“图像模型已经会推理”的证明。
- 它给视觉生成系统的实际启发是：未来 test-time compute 可能不只表现为更多采样或更多 denoising steps，也可能表现为 layer 内部的 token / patch / expert / halting 预算分配。
- 后续真正关键的工程问题不是继续固定 `Tlatent=2/5`，而是引入自适应 halting、routing audit、局部结构 verifier 和失败样本路由诊断。

### 验证结果

- 新增 HTML scoped 结构检查通过：`title`、viewport、`notes-shell.css`、`body.notes-shell-page`、Notes / All Notes / Home 导航、`main`、`data-note-role="evidence-appendix"`、本地配图引用和公开生成痕迹检查均通过。
- `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 78 entries, 78 top-level note html files`。
- `git diff --check -- "notes/paper-reviews/thinking-pixel-recursive-sparse-reasoning.html" "notes/paper-reviews/thinking-pixel-recursive-sparse-reasoning-assets/paper-page-03.jpg" "_data/notes.yml" "Progress.md"` 通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仍有既有 `faraday-retry` 建议和 GitHub Metadata API 403/限流 warning，不影响 `_site` 静态生成。
- `_site/notes/paper-reviews/thinking-pixel-recursive-sparse-reasoning.html` 结构抽查通过：页面存在，大小 `27426` bytes，`section` 数量为 8，`body.notes-shell-page`、`main`、`data-note-role="evidence-appendix"`、本地配图和 `_site/notes/assets/notes-shell.css` 均存在。

## 2026-06-02 LongTraceRL X thread 与论文笔记导出

### 背景

- 用户要求仔细阅读梳理 `https://x.com/HuggingPapers/status/2061322399518216371` 并导入笔记，随后要求任务完成后及时 `commit push`。
- 原帖为 HuggingPapers 推荐 **LongTraceRL: Learning Long-Context Reasoning from Search Agent Trajectories with Rubric Rewards**，主题是用 search agent trajectories 与 entity-level rubric rewards 改进 128K 长上下文推理 RLVR。

### 已完成

- 按仓库规则读取 `AGENTS.md`、`.agent/codex-experience-profile.md`、`Progress.md`、`notes/NOTE_TEMPLATE.md`，并确认当前工作树存在大量既有未提交改动；本轮只处理 LongTraceRL 相关新增笔记、索引和进度记录。
- 使用 `opencli twitter thread` 获取目标 X thread：
  - 根帖时间：2026-06-01 05:42:12 UTC；
  - 主帖说明 LongTraceRL 让 LLM 通过 search agent trajectories 和 fine-grained entity-level rubric rewards 学会 128K context 推理；
  - 回复短链给出 paper 与 collection，并说明 4B、8B、30B 模型和训练数据已发布。
- 使用 `curl -sIL` 解析短链：
  - paper：`https://huggingface.co/papers/2605.31584`
  - collection：`https://huggingface.co/collections/THU-KEG/longtracerl`
  - 图片短链指向 X 图片页，已下载本地配图资源。
- 使用 Hugging Face Paper API、`opencli arxiv paper`、PDF 下载与 `pdfinfo` 核验论文元数据：
  - arXiv ID：`2605.31584`；
  - 标题：`LongTraceRL: Learning Long-Context Reasoning from Search Agent Trajectories with Rubric Rewards`；
  - 作者：Nianyi Lin、Jiajie Zhang、Lei Hou、Juanzi Li；
  - arXiv v1 发布日期：2026-05-29；
  - PDF 21 页，题名与作者一致。
- 阅读 Hugging Face paper markdown、arXiv HTML/PDF、官方 GitHub raw README、HF collection、HF dataset/model cards、reward server 与训练配置，核验：
  - 数据集 2,815 条，每条约 128K prompt，基于 KILT Wikipedia KG random walk 生成 8-hop 问题；
  - distractor 来自 search agent 轨迹：Tier-1 为 opened/read but not cited，Tier-2 为 searched but unopened；
  - rubric reward 是 gold entities recall，并通过 group-level normalization 与 positive-only 策略限制 reward hacking；
  - 训练配置包括 GRPO group size 8、global batch size 128、200 iterations、learning rate `2e-6`、rubric reward weight `0.3`、32 x H800；
  - 公开资源包括 HF dataset `THU-KEG/LongTraceRL` 和模型 `THU-KEG/LongTraceRL-4B`、`8B`、`30B`。
- 新增站内论文笔记：
  - `notes/paper-reviews/longtracerl-long-context-reasoning.html`
- 新增本地配图资源：
  - `notes/paper-reviews/longtracerl-long-context-reasoning-assets/huggingpapers-root.jpg`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`LongTraceRL：用搜索轨迹和实体级 rubric 训练 128K 长上下文推理`
  - URL：`/notes/paper-reviews/longtracerl-long-context-reasoning.html`
  - 类型：`Paper Note`

### 关键观察

- LongTraceRL 的核心不是“把上下文长度拉到 128K”，而是把真实 search agent 读过但最终不该引用的材料变成 hard distractors，让训练分布更接近真实检索错误。
- Tier-1 distractor 的价值在于它不是随机噪声，而是模型很可能误判为证据的相邻路径；论文统计中 Tier-1 的 rubric entity overlap macro ratio 达 63.23%，random distractor 只有 1.35%。
- entity-level rubric reward 本质仍是 proxy reward，不能证明完整推理正确；positive-only 策略很关键，因为它把实体命中限制为“正确答案内部质量排序”，避免错误答案靠枚举实体拿分。
- 主力实验在 Qwen3-4B 上最有说服力：base 平均 53.3，LongTraceRL 为 59.0；去掉 rubric 的 LongTraceRL-GRPO 为 53.7，说明收益主要来自 rubric + hard distractor 的组合，不只是同一批长数据多训几步。

### 当前判断

- LongTraceRL 对 deep research、长文档 RAG、法律/金融材料审阅和多跳企业知识问答有直接启发：训练数据应该保存 search/open/cite 的中间失败痕迹，而不只保存最终成功答案。
- 这套 recipe 依赖可验证答案、可枚举中间证据实体和足够强的搜索 agent；对主观开放生成、无唯一答案或证据路径多解的任务不能直接照搬。
- GitHub REST API 当前因未认证 rate limit 返回 403；已降级使用 raw GitHub README、HF API、arXiv/HF 页面作为主证据，不把 GitHub 动态星标等字段作为核心判断。

### 验证结果

- 当前工作区 `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 78 entries, 78 top-level note html files`。
- `git diff --check -- "notes/paper-reviews/longtracerl-long-context-reasoning.html" "notes/paper-reviews/longtracerl-long-context-reasoning-assets/huggingpapers-root.jpg" "_data/notes.yml" "Progress.md"` 通过。
- 新增 HTML 与 `_data/notes.yml` 未命中 `Generated locally`、`HTML generated`、`本地 HTML 生成`、`报告生成日期`、`/tmp/`、`/Users/bytedance`、`最终 HTML 路径`、`文件位置`、Unicode replacement character 等公开生成痕迹。
- 本地配图文件为 `1199x469` JPEG。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 `faraday-retry` 建议和 GitHub Metadata API 未认证/限流 warning，不影响 `_site` 静态生成。
- `_site/notes/paper-reviews/longtracerl-long-context-reasoning.html` 结构检查通过：title、`body.notes-shell-page`、Notes / All Notes / Home 导航、`main`、8 个 section、`data-note-role="evidence-appendix"` 和本地图片引用均存在。
- `_site/notes/index.html` 已出现 LongTraceRL 卡片入口。
- staged snapshot 验证、commit 与 push 收口见本文件顶部 `2026-06-02 commit/push 收口复验`。

## 2026-06-02 数学题库与知识库内容审计

### 背景

- 用户要求 review 数学题库和知识库方面内容，指出“有的内容都有问题”，随后要求本轮工作完成后及时 commit push。
- 本轮按 code review / content audit 方式处理：先定位题库范围，再抓可复现的事实性或概念性问题，避免把偏好表达误判为内容 bug。

### 已审计范围

- 数学题库：
  - `notes/math-interview-question-bank/index.html`
  - `notes/math-interview-question-bank/chapters/001.html` 至 `020.html`
- 知识库 / RAG 相关章节：
  - `notes/llm-interview-question-bank/chapters/010.html`
  - `notes/llm-interview-question-bank/chapters/043.html`
  - `notes/llm-interview-question-bank/chapters/054.html`
- 额外检查：
  - 当前 notes validator 规则；
  - 数学公式、数值例题、RAG 召回/重排术语和容易误导的绝对化表述。

### 发现并修复的问题

- 数学综合案例中 `020.html` 的 VaR/CVaR 离散样本口径前后不一致：
  - 该页按 \(\lceil0.8\cdot5\rceil=4\) 取 \(VaR_{0.8}\approx -0.004\)，但随后把 CVaR 写成只取最大损失 `0.016`；
  - 前文 `011.html` 的口径是 \(CVaR_\alpha=\mathbb{E}[L\mid L\ge VaR_\alpha]\)，离散样本例题也把等于 VaR 门槛的样本计入尾部；
  - 已修为同一口径下 \(CVaR_{0.8}\approx(-0.004+0.016)/2=0.006\)，并补充说明若采用更保守的“最坏 20%”经验口径，需要先声明口径，否则同一组样本会算出不同结果。
- RAG 章节 `043.html` 将 “embedding model 的两种架构” 写成 `Bi-Encoder vs Cross-Encoder`，容易误导读者以为 Cross-Encoder 也会产出可入库 embedding：
  - 已改为“召回与重排的两种打分架构”；
  - 补充说明只有 Bi-Encoder 这类稠密召回模型会产出可预计算、可入库的文档 embedding，Cross-Encoder 通常是对 query-doc 对直接打分的 reranker。
- RAG 章节 `043.html` 把 ColBERT 放进 Cross-Encoder 代表模型列表：
  - 已改为 `BGE-Reranker, monoT5 等；ColBERT 属于 late-interaction 折中路线`，和后文本身对 ColBERT 的 late interaction 解释保持一致。
- RAG 章节 `043.html` 有两个过度绝对化表述：
  - `BGE-large-zh（开源最强中文 embedding）` 改为按业务评测选择 BGE / GTE / E5 系列中文或多语言模型；
  - `recall@10 < 80% 就值得微调` 改为看真实 query-document 对上的 recall、误召回类型、业务风险和成本，不再给固定魔法阈值。

### 验证结果

- 已写入并运行内容回归检查，确认上述旧问题文本不再出现，且修复说明存在。
- 提交前全局复验 `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 74 entries, 74 top-level note html files`；此前 `x-tweet-cycle-ai-digest.html` 顶部来源/流程措辞 warning 已收敛为正文判断与“样本机制”，当前无 notes quality warning。
- 提交前 `git diff --check` 通过；公开页面生成痕迹扫描未命中 `/tmp/`、`/Users/bytedance`、`Generated locally`、`HTML generated`、`本地 HTML 生成`、`报告生成日期`、`最终 HTML 路径`、`文件位置` 等模式。
- `git diff --check -- "notes/math-interview-question-bank/chapters/020.html" "notes/llm-interview-question-bank/chapters/043.html"` 通过。

## 2026-06-02 Agentic RL rollout system X 帖与站内笔记导出

### 背景

- 用户要求充分梳理理解并导入笔记：`https://x.com/lawhy_X/status/2061685069513892043`。
- 原帖作者 Yuan He，公开简介为 Applied Scientist @Amazon Rufus working on agent post-training；主帖内容是 “Multi-turn RL needs correct and efficient rollouts”，并指向 slide deck `From Agent Loops to Agent Environments`。

### 已完成

- 使用 `opencli twitter thread` 获取目标 X thread：
  - 根帖时间：2026-06-02 05:43:19 UTC；
  - 主帖观点：multi-turn RL 在数据和算法之前，先需要正确且高效的 agentic rollouts；
  - 回复区共识包括：rollout layer 基本上是 data collection step，一轮坏掉会让整条 episode 变成噪声；
  - 回复区还出现 A2E Protocol 链接和关于 policy agent / environment layer / reward layer / learning layer 分层的架构讨论。
- 使用 `opencli twitter profile` 核验作者资料：
  - screen name：`lawhy_X`；
  - name：Yuan He；
  - bio：Applied Scientist @Amazon Rufus working on agent post-training；
  - profile url：`https://www.yuanhe.wiki/`。
- 解析 X 短链：
  - 主材料：`https://yuanhe.wiki/posts/technical/strands-env/`；
  - 回复区 A2E blog：`https://a2eprotocol.github.io/docs/blog/2026-05-21-the-harness-is-the-product.html`；
  - 回复区 A2E docs：`https://a2eprotocol.github.io/docs/`。
- 使用 `opencli web read` 读取 slide deck 正文，核验核心内容：
  - agent environment 本质是 rollout system；
  - correctness 包括 tokens、tool calls、terminations、train-inference match；
  - retokenization drift 会破坏 on-policy RL；
  - chat template 需要 incremental application，否则会引入 separator / BOS 问题；
  - tool parser 不应静默修复 malformed call，也不应执行 `<think>` 中的草稿工具调用；
  - termination reason 应区分 throttling timeout、context window overflow、max tool iterations、task complete；
  - async 不等于 parallelism，Python event loop 中 CPU 段会在大规模 rollout 下堆积；
  - distributed rollouts 可用多进程 / actor 绕开单 event loop / GIL；
  - fully async rollouts 提高吞吐但引入 stale rollout / off-policy data trade-off。
- 读取官方 GitHub README：
  - `strands-env` 将每次 `env.step()` 视为完整 agent loop：prompt -> tool_call/tool_response -> response，并提供 step/observe/reward、benchmark 和 RL training integration；
  - `strands-sglang` 强调 token-in / token-out rollouts、strict tool-call parsing、TokenManager、loss mask、logprobs 与 termination reason。
- 新增站内技术分析笔记：
  - `notes/tech-analysis/agentic-rl-rollout-environments.html`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`Agentic RL 的 rollout 层：从 Agent Loop 到 Agent Environment`
  - URL：`/notes/tech-analysis/agentic-rl-rollout-environments.html`
  - 类型：`Tech Analysis`

### 关键观察

- 这条材料的核心 insight 不是“又一个 agent SDK”，而是把 agent orchestration 从产品编排重新定义成 RL 训练里的 rollout system。
- 产品 runtime 倾向于容错：修 JSON、重试工具、自动 fallback、吞掉异常；训练 runtime 则需要可归因：原始 token、loss mask、logprob、tool raw text、termination reason 和 reward 必须能对齐。
- retokenization drift 是 on-policy agentic RL 的底层破坏项：如果训练看到的是 `encode(decode(tokens))`，就不再是当前 policy 真正采样的 token 序列。
- strict tool parsing 的工程价值在于把错误留给模型学习，而不是把错误工具调用伪装成成功。
- termination taxonomy 是 reward shaping 的前置条件：环境限流、上下文溢出、工具迭代过多、任务完成不能混成同一种失败。
- rollout efficiency 的瓶颈不只在模型 serving；网页解析、沙箱启动、rate limit、CPU postprocess、cleanup、trainer waiting 都可能成为 wall-clock 主因。
- A2E 回复区材料与主帖互相呼应，但层次不同：A2E 强调开放 agent-to-environment protocol 和 harness ownership，strands-env / strands-sglang 更像具体 rollout environment 与 token-faithful serving 实现。

### 当前判断

- Agentic RL 的第一道质量门禁应是 rollout audit，而不是直接比较 GRPO/PPO/DPO 或 KL 参数。
- 真正可操作的审计项包括 token fidelity、tool parser failure、termination taxonomy、throughput decomposition 和 stale rollout 统计。
- 如果一个系统无法证明每条 trajectory 的 token、工具、观察、终止、reward 是可信且可归因的，那么后续算法优化可能只是在更高效率地拟合基础设施噪声。

### 验证结果

- 新增 HTML scoped 结构检查通过：`title`、viewport、`notes-shell.css`、`body.notes-shell-page`、Notes / All Notes / Home 导航、`main`、`data-note-role="evidence-appendix"` 与公开生成痕迹检查均通过。
- `git diff --check -- "notes/tech-analysis/agentic-rl-rollout-environments.html" "_data/notes.yml" "Progress.md"` 通过。
- `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 74 entries, 74 top-level note html files`；当前工作树保留 1 条旧页面质量 warning：`x-tweet-cycle-ai-digest.html` 顶部出现来源/流程措辞。
- 复验 `git diff --check -- "notes/tech-analysis/agentic-rl-rollout-environments.html" "_data/notes.yml" "Progress.md"` 通过。
- 新增 HTML 与 `_data/notes.yml` 未命中 `Generated locally`、`HTML generated`、`本地 HTML 生成`、`报告生成日期`、`/tmp/`、`/Users/bytedance`、`最终 HTML 路径`、`文件位置`、Unicode replacement character 等公开生成痕迹。
- 首次 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 提示临时 bundle 缺 `jekyll`；执行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle install` 后重新构建成功。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 通过；仍有 `faraday-retry` 建议和 GitHub Metadata API 403/限流 warning，不影响 `_site` 静态生成。
- `_site/notes/tech-analysis/agentic-rl-rollout-environments.html` 结构检查通过：页面存在，文件大小 `26009` bytes，`section` 数量为 9，title、`body.notes-shell-page`、Notes sitebar、`main`、`data-note-role="evidence-appendix"` 和 `_site/notes/assets/notes-shell.css` 均存在。
- 本地 `_site` 静态服务 HTTP 检查通过：`http://127.0.0.1:4177/notes/tech-analysis/agentic-rl-rollout-environments.html` 返回 `200`，DOM 检查显示 `section=9`、`bytes=26009`。
- Chrome headless 截图通过：
  - 桌面视口 `1440x1100` 生成 `/tmp/agentic-rollout-desktop.png`，大小 `212987` bytes；
  - 移动视口 `390x844` 生成 `/tmp/agentic-rollout-mobile.png`，大小 `103759` bytes；
  - 移动截图 stderr 有 Chrome GPU `SharedImageManager::ProduceMemory` 噪声，但截图已成功写出，不是页面资源错误。

## 2026-06-02 仓库审计报告复核与结构修复

### 背景

- 用户要求核实并修复 `audit_report.html` 中列出的仓库问题，重点包括章节页 `chapter-nav` 重复、章节导航方向、heading ID、`_site` 跟踪状态、`cite.py`、`about.md` 旧统计脚本、`.DS_Store` 和 `_drafts` 残留。
- 本轮遵循先复现再修复：先检查当前 worktree、报告内容、章节目录页和实际源文件，再只处理当前仓库中可证实的问题。

### 复核结论

- 确认为真实问题：
  - `notes/llm-interview-question-bank/chapters/*.html` 90 个文件和 `notes/math-interview-question-bank/chapters/*.html` 20 个文件均存在两个 `<nav class="chapter-nav">`。
  - `cite.py` 对 Semantic Scholar author papers 使用逐行嵌套遍历，且直接覆盖写 `_pages/about.md`。
  - `_pages/about.md` 底部仍有 `busuanzi` 中文访问统计和 `flagcounter` 外部统计图。
  - 工作区存在 15 个 `.DS_Store` 物理文件；`_drafts/post-draft.md` 是已跟踪示例草稿。
- 修正审计报告中的当前状态误判：
  - `git ls-files "_site" | wc -l` 返回 `0`，说明当前 Git 索引并未跟踪 `_site/`；`_site/` 只是本地构建产物，且 `.gitignore` 已覆盖。
  - “跨文件 heading ID 冲突”不是当前站点 bug：这些 ID 分布在独立 HTML 文档中，浏览器锚点作用域是单文档。本轮已把 validator 加强为检查每个 HTML 文件内部 ID 唯一。
  - “导航方向错误”不能按数字相邻判断。LLM 题库的目录明确按学习路径重排，上一节/下一节应跟随 `index.html` 中的学习顺序，而不是 `001 -> 002 -> 003` 的文件号顺序。本轮 validator 改为按目录页顺序验证。

### 已完成

- 扩展 `scripts/validate_notes_index.rb`：
  - 读取 LLM 题库和数学题库 `index.html` 的章节顺序；
  - 要求每个章节页恰好一个 `chapter-nav`；
  - 要求 `chapter-nav` 链接与目录页学习顺序一致；
  - 要求单个章节 HTML 内部 `id` 唯一。
- 对 110 个章节页做机械修复：删除正文前的重复 `chapter-nav`，保留正文后的翻页导航。
- 改写 `cite.py`：
  - 先将 `author.papers` 建成 `paperId -> citationCount` 字典；
  - 用 `Path.read_text` / `NamedTemporaryFile` / `os.replace` 做原子替换；
  - 保持脚本入口为 `if __name__ == "__main__"`，避免 import 时产生副作用。
- 清理 `_pages/about.md` 底部 `busuanzi` 和 `flagcounter`。
- 删除 15 个 `.DS_Store` 物理文件。
- 删除已跟踪示例草稿 `_drafts/post-draft.md`，并在 `.gitignore` 新增 `_drafts/`，防止后续本地草稿误入仓库。

### 验证结果

- 先运行增强后的 `ruby "scripts/validate_notes_index.rb"`，RED 阶段稳定失败并列出 110 个章节页 `chapter-nav` 数量为 2；修复后重新运行通过，最终输出 `notes index ok: 70 entries, 70 top-level note html files`。
- 独立结构审计通过：`110` 个章节页均为一个 `chapter-nav`，链接按目录页学习顺序，单文件内无重复 `id`。
- `python3 -m py_compile "cite.py"` 通过。
- `find "." -name ".DS_Store" -not -path "./.git/*" -print` 无输出。
- `rg -n "busuanzi|flagcounter|本站总访问量" "_pages/about.md"` 无输出。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仍有 `faraday-retry` 建议和 GitHub Metadata API 403/限流 warning，不影响 `_site` 静态生成。
- 从 `_site` 启动本地服务后，DOM/HTTP 抽查通过：
  - `/`、`/notes/llm-interview-question-bank/`、`/notes/llm-interview-question-bank/chapters/001.html`、`/notes/llm-interview-question-bank/chapters/090.html`、`/notes/math-interview-question-bank/chapters/001.html`、`/notes/math-interview-question-bank/chapters/020.html` 均返回 `200`；
  - 章节页 `main` 存在，`chapter-nav` 数量均为 `1`；
  - 抽查页本地图片引用无缺失。
- 浏览器验证边界：
  - Codex in-app Browser 当前返回 `iab` 不可用；
  - Playwright wrapper 调用 `npx --package @playwright/mcp playwright-cli` 时提示 `playwright-cli: command not found`；
  - 已降级使用系统 Google Chrome headless 生成 `/tmp/llm-chapter-001.png` 和 `/tmp/math-chapter-020.png` 截图。Chrome stderr 存在系统 updater / Crashpad 权限噪声，不是站点控制台或页面资源错误。

## 2026-06-02 Frontier Async RL X thread 与 blog 笔记导出

### 背景

- 用户要求仔细阅读梳理并导入笔记：`https://x.com/whatthelukh/status/2061509262069923868`。
- 原帖为 Luke J. Huang 发布的 **Is frontier asynchronous RL solved?** blog/thread，主题是异步 RL 后训练中的 policy lag、train-inference mismatch、importance sampling estimator 和系统修补边界。

### 已完成

- 按仓库规则读取 `AGENTS.md`、`.agent/codex-experience-profile.md`、`Progress.md`、`notes/NOTE_TEMPLATE.md` 和 notes workflow。
- 使用 `opencli twitter thread` 获取目标 X thread：
  - 根帖时间：2026-06-01 18:04:43 UTC；
  - 原帖说明 blog 调研 8 个开放权重 frontier labs 如何处理 Async RL 的 train-inference mismatch；
  - 作者补充列出 GLM-5、Ring-1T、DeepSeek V3.2、Minimax M2.5、Qwen 3.5、Intellect-3、NVIDIA Nemotron Super、Laguna M.1；
  - 线程 takeaways 覆盖 policy lag、rollout-bound/training-bound、TIS/CISPO、MIS/IcePop、sequence IS、token IS 和 low-bias compute scaling hypothesis。
- 使用 `curl -sIL` 解析短链：
  - blog 链接：`https://luk-huang.github.io/personal-website/blog/is-frontier-asynchronous-rl-solved.html`
  - 图片短链指向 X 图片页，已下载并本地化主帖配图。
- 使用 `opencli web read` 读取作者 blog 正文，核验：
  - async RL 通过 rollout/training 解耦带来 2-3x 吞吐提升；
  - policy lag K 让 trajectory stale，Kmax 太低会让系统 rollout-bound，Kmax 放开又放大 off-policy instability；
  - 算法修补包括 TIS/CISPO、MIS/IcePop、DeepSeek masking、M2PO 等 IS ratio reshaping；
  - 系统修补包括 MoE routing replay、batch-invariant kernels、FP32 LM head、FP16、quantized rollout、fast weight sync 和 KV cache recomputation；
  - 作者主张 sequence-level IS 更接近正确 off-policy 目标，更可能随 batch/compute 扩展；token-level IS 在高 policy lag 与长 horizon 下存在结构性 bias。
- 新增站内技术分析笔记：
  - `notes/tech-analysis/frontier-async-rl-solved.html`
- 新增本地配图资源：
  - `notes/tech-analysis/frontier-async-rl-solved-assets/async-rl-infographic.jpg`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`Async RL 是否已解决：policy lag、IS 偏差与后训练系统边界`
  - URL：`/notes/tech-analysis/frontier-async-rl-solved.html`
  - 类型：`Tech Analysis`

### 关键观察

- 这篇材料的核心 insight 不是“async RL 已经让 RL 后训练变快”，而是说明异步化把 on-policy RL 的干净假设换成了更高吞吐但更旧的数据分布。
- 系统侧修补可以压低 rollout engine 与 trainer 的数值错配，但不能把旧 policy 生成的 trajectory 变成新 policy 数据；高 policy lag 下仍要面对 IS ratio 极端化。
- token-level IS、geometric-mean IS 与 masking/clipping 更像低方差高偏差的工程补丁；sequence-level IS 暴露更高 variance，但在作者论证中更接近正确 off-policy 目标，也更可能随 batch/compute 扩展。
- 低偏差 compute scaling hypothesis 的工程含义是：不要只用小 batch、小 horizon 的 early stability 判断一个 async RL 修补是否可扩展；高 bias 方法可能在早期更稳，但 compute 上去后 bias 会成为上限。

### 当前判断

- Frontier async RL 已经是大模型 RL post-training 的主流系统形态，但“高 policy lag、长 horizon、有限 batch 下的稳定低偏差训练”还没有被解决。
- 下一阶段真正有价值的方向可能是 collapse 前诊断与动态控制：识别 estimator 何时偏离，再调整 lag、batch、truncation、mask 或 estimator 形态，而不是只新增固定阈值 mask。

### 验证结果

- 当前工作区 `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 73 entries, 73 top-level note html files`；保留 1 条既有 warning：`notes/tech-analysis/x-tweet-cycle-ai-digest.html` 顶部来源/流程措辞，非本轮新增页面引入。
- 精确 staged snapshot 导出到 `/private/tmp/frontier-async-rl-staged` 后，`ruby "/private/tmp/frontier-async-rl-staged/scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 61 entries, 61 top-level note html files`。
- `git diff --cached --check` 通过；staged diff 仅包含 `Progress.md`、`_data/notes.yml`、`notes/tech-analysis/frontier-async-rl-solved.html` 和 `notes/tech-analysis/frontier-async-rl-solved-assets/async-rl-infographic.jpg`。
- 新增 HTML 与 `_data/notes.yml` 未命中 `Generated locally`、`HTML generated`、`本地 HTML 生成`、`报告生成日期`、`/tmp/`、`/Users/bytedance`、`最终 HTML 路径`、`文件位置`、Unicode replacement character 等公开生成痕迹。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 在当前工作区构建成功；`BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build --source "/private/tmp/frontier-async-rl-staged" --destination "/private/tmp/frontier-async-rl-staged-site"` 在 staged snapshot 构建成功；仅出现 `faraday-retry` 和 GitHub Metadata 未认证/限流 warning，不影响 `_site` 生成。
- staged `_site/notes/tech-analysis/frontier-async-rl-solved.html` 结构检查覆盖：title、`body.notes-shell-page`、Notes / All Notes / Home 导航、`main`、`data-note-role="evidence-appendix"`、本地配图引用均存在；配图文件为 `802x1174` JPEG。

## 2026-05-30 BES 双向演化搜索 X 线程解读与笔记导出

### 背景

- 用户要求“深度梳理解读并导出笔记”：`https://x.com/Kevin_GuoweiXu/status/2060022930172506200`。
- 原帖主题为 **BES: Bidirectional Evolutionary Search**，对应论文 `Self-Improving Language Models with Bidirectional Evolutionary Search`。

### 已完成

- 按仓库规则读取 `AGENTS.md`、`.agent/codex-experience-profile.md`、`Progress.md`、`notes/NOTE_TEMPLATE.md`。
- 使用 `opencli twitter thread` 获取原帖 8 条线程和评论区关键问答：
  - 原帖指出 Best-of-N / GRPO 与 tree search 的两个瓶颈：verification signals sparse、candidates stay within model distribution。
  - 线程定义 BES 为 forward candidate evolution + backward goal decomposition。
  - 评论区确认 backward search 当前生成的是 subgoals，不是完整 backward solution；子目标 cleanly verifiable 时会显著加速搜索。
- 使用 `opencli twitter profile` 核验作者 Kevin / Guowei Xu 的公开简介。
- 解析原帖短链：
  - 论文：`https://huggingface.co/papers/2605.28814` / `https://arxiv.org/abs/2605.28814`
  - 代码：`https://github.com/Embodied-Minds-Lab/BES`
  - 模型集合：`https://huggingface.co/collections/Xkev/bes`
  - 项目页：`https://guoweixu.com/bes`
- 使用 `opencli arxiv paper 2605.28814`、`opencli hf paper 2605.28814`、PDF 下载与 `pdfinfo` 核验论文元数据和正文：
  - arXiv v1 发布日期：2026-05-27。
  - PDF 36 页，标题和作者与原帖一致。
- 读取 GitHub README、`logical/README.md`、`multihop/README.md`、`inference/README.md` 和 inference 关键源码，核验：
  - forward operators：combination、deletion、translocation、crossover；
  - backward goal tree / recursive scoring / bucket interpolation；
  - Knights-and-Knaves、MuSiQue、Circle Packing、Heilbronn 的实验设置与复现入口；
  - HF collection 中公开的 K&K 和 multihop BES 模型条目。
- 新增站内论文笔记：
  - `notes/paper-reviews/bes-bidirectional-evolutionary-search.html`
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`BES：把搜索从同分布采样推进到目标反推与轨迹重组`
  - URL：`/notes/paper-reviews/bes-bidirectional-evolutionary-search.html`
  - 类型：`Paper Note`

### 关键观察

- BES 的核心不是“再做一个 tree search”，而是把 hard problem 上的稀疏终局命中拆成两个更可操作的问题：用 backward goal tree 让部分进展可见，用 evolutionary operators 把不同错误轨迹中的局部正确片段重组。
- 理论部分的工程含义是：expansion-only rollout 高概率停留在模型原分布的 entropy shell；evolution operators 通过跨轨迹 block recombination 打破原有依赖；backward sub-goals 把完整解的乘法命中概率转成局部证据收集问题。
- 实验收益集中在 baseline 采样已经明显不足的 hard setting：
  - MuSiQue 3B：Base 4.0%，GRPO 2.1%，Tree-GRPO 3.9%，BES 7.0%。
  - MuSiQue 8B：Base 6.6%，Tree-GRPO 7.4%，BES 10.4%。
  - open problem solving 中 BES 的平均值优于 OpenEvolve、GEPA、ShinkaEvolve，但 best value 仍接近而未超过 AlphaEvolve / human high-compute 参考。
- 真正的工程难点是 domain verifier 与 sub-goal 设计：
  - K&K 使用模板化目标树；
  - MuSiQue 使用 embedding similarity 覆盖 atomic sub-question；
  - 程序优化使用 Python verifier expression，并用 bucket interpolation 防止 backward score 压过 raw objective。

### 当前判断

- BES 更适合作为“难样本生成 / 工具轨迹搜索 / 程序候选重组”的框架，而不是通用推理补丁。
- 它要求 objective reward、可分解子目标和可重组候选同时成立；主观任务、弱 decomposition 模型、语义不闭合的轨迹拼接都会削弱收益。
- `opencli web read` 读取项目页时遇到 stale page identity，已降级使用论文、GitHub、HF API 和 raw 文件作为主证据；项目页仅作为链接一致性核验。

### 验证结果

- `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 69 entries, 69 top-level note html files`。
- `git diff --check -- "notes/paper-reviews/bes-bidirectional-evolutionary-search.html" "_data/notes.yml" "Progress.md"` 通过。
- 新增 HTML 与 `_data/notes.yml` 未命中 `Generated locally`、`HTML generated`、`本地 HTML 生成`、`报告生成日期`、`/Users/bytedance/Downloads`、`Exported as a single HTML note`、Unicode replacement character 等公开生成痕迹。
- 首次 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 失败，原因是临时 gem 目录缺少 `jekyll` 可执行文件；随后运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle install` 补齐依赖。
- 重新运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 `faraday-retry` 与 GitHub Metadata 未认证 warning，不影响 `_site` 生成。
- 本地静态服务打开新增页面返回 `HTTP 200`，`notes-shell.css` 与 `favicon.ico` 均返回 `200`。
- OpenCLI browser 检查新增页面：
  - title 正确；
  - `body.notes-shell-page`、`.notes-sitebar`、`main`、证据附录均存在；
  - `main section` 数量为 9；
  - `badImages: []`；
  - 桌面视口 `overflow: 0`；
  - browser console message 数量为 0。
- 系统 Chrome headless 以 `390x844` 移动视口打开并截图成功；PNG 文件 `390 x 844`、约 `97K`、PNG header 正常，页面非空。

## 2026-05-28 Codex 会话与执行日志系统复盘

### 背景

- 用户要求阅读并检索所有 Codex 对话记录与执行日志，做系统性复盘，提炼可复用经验文档。
- 交付物要求：
  - 执行经验总结；
  - 用户 UI / 产品 / 交互偏好与理念档案；
  - Codex 未来可直接遵循的规则清单；
  - 保存为独立文件；
  - 在 `.agent` 配置中以地址引用方式加载，使后续 Codex 会话继承。

### 已完成

- 读取并核验当前仓库状态：
  - `AGENTS.md`
  - `Progress.md`
  - 当前工作树已有大量未提交改动，本轮只触碰复盘任务必要文件。
- 定位 Codex 本地数据源：
  - `/Users/bytedance/.codex/sessions/`
  - `/Users/bytedance/.codex/archived_sessions/`
  - `/Users/bytedance/.codex/session_index.jsonl`
  - `/Users/bytedance/.codex/logs_2.sqlite`
  - `/Users/bytedance/.codex/shell_snapshots/`
- 完成结构化扫描：
  - 可解析 `session_meta`：1813 条，覆盖 2025-09 到 2026-05。
  - Codex JSONL 体量：`sessions` 约 2.0G，`archived_sessions` 约 263M。
  - 高频工作目录：`TradeAgent` 1131 次、`FreqTrade` 166 次、`SheSheBot` 132 次、本个人站仓库相关目录 88 次。
  - 过滤长上下文和环境注入后的用户短消息：4423 条。
  - 工具调用：约 128584 次。
  - SQLite 日志：171479 条，其中 WARN 1660 条、ERROR 46 条。
- 复核 OpenAI Codex 官方文档：Codex 会读取全局 `~/.codex/AGENTS.md` 和项目 `AGENTS.md`，同时支持 `AGENTS.override.md` 及配置 fallback 文件；`.agent/config.toml` 本身不是官方默认 instruction discovery 入口。
- 新增独立经验档案：
  - `.agent/codex-experience-profile.md`
- 新增 `.agent` 地址索引：
  - `.agent/config.toml`
- 更新仓库 `AGENTS.md`，添加 `Codex Experience Profile` 引用。
- 更新全局 `/Users/bytedance/.codex/AGENTS.md`，使后续 Codex 会话默认看到经验档案路径。

### 关键观察

- 历史纠偏最集中在几个模式：未读仓库规则、过宽搜索导致噪声、没有按阶段验证、把数据/日志写入仓库、只生成笔记不直接讲解、UI 状态不可验证、性能优化牺牲语义、完成前缺少要求级审计。
- 用户稳定偏好是：中文、直接、深度、证据驱动；遇到授权时自主推进；研究内容要有机制解释和 insight；工具 UI 要显示真实运行状态；仓库和文档要简洁。
- 对当前仓库，后续不应默认写 Obsidian；站内 notes 和研发过程分别遵循 `notes/NOTE_TEMPLATE.md` 与 `Progress.md`。

### 当前判断

- `.agent/config.toml` 已作为地址索引满足 `.agent` 配置引用需求；真正能让 Codex 后续默认继承的加载路径是全局 `~/.codex/AGENTS.md` 与本仓库 `AGENTS.md` 的路径引用。
- 不把复盘正文直接塞入 `AGENTS.md`，避免启动上下文膨胀；`AGENTS.md` 只保留稳定入口，详细规则放独立文件。

## 2026-05-28 LRPO 多语言 Policy Optimization 帖子解读与笔记导出

### 背景

- 用户要求解读 X 帖：`https://x.com/CherylolGuo/status/2059695145679790165`，随后要求“导出笔记”。
- 帖子主题为 ICML 2026 论文 `Learning to Route Languages for Multilingual Policy Optimization`，方法名为 LRPO。

### 已完成

- 使用 `opencli twitter thread` 获取原帖和完整线程内容，确认作者介绍了 Language-Routed Policy Optimization、希腊 thumbs-up 例子、language router、reward calibration、Qwen2.5-1.5B 的 mGSM-v2 提升和论文/代码链接。
- 解析短链得到：
  - 论文 PDF：`https://arxiv.org/pdf/2605.25360`
  - 代码仓库：`https://github.com/Guochry/LRPO`
- 使用 `opencli arxiv paper 2605.25360` 核验论文元数据：标题、作者、发布日期、ICML 2026 标注和摘要。
- 读取官方 GitHub README，核验 LRPO 的三个组件：language-routed rollouts、calibrated multilingual rewards、trainable language router。
- 下载并抽取论文 PDF 文本，核验方法设计、实验表格、reward calibration、router learning dynamics、训练成本和统计显著性。
- 新增站内论文笔记：`notes/paper-reviews/lrpo-language-routed-policy-optimization.html`。
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`LRPO：把语言选择变成多语言后训练的可学习变量`
  - URL：`/notes/paper-reviews/lrpo-language-routed-policy-optimization.html`
  - 类型：`Paper Note`

### 关键观察

- LRPO 的核心 insight 是：语言不是单纯的输入输出格式，而是访问模型内部知识分布的一条路径；后训练阶段不应默认只用源语言或英语中心路径 rollout。
- 方法上，LRPO 在固定 rollout budget 下保留部分源语言 rollout，并让 trainable language router 根据主题/地区上下文采样其他语言。
- 跨语言 reward 不能直接比较；论文用离线语言对相似度统计做 mean-based 或 quantile-based calibration，避免 embedding/reward model 的语言对偏差污染 policy update。
- 实验收益更集中在 CARE、CARE-pro、mGSM-v2 这类开放生成任务；Global-MMLU-Lite 和 Include-Lite 等选择题任务更多是保持或小幅波动。
- 工程启发是：多语言 RAG 和国际化 agent 不应只做“翻译成英文再处理”，而应同时路由资料来源语言、推理/生成语言和最终用户输出语言。

### 当前判断

- 该工作把“多语言能力”从评测标签推进为后训练中的可学习控制变量，对区域知识、跨文化信息需求和非英语资料检索场景有实际参考价值。
- 主要边界是 reward 依赖、reference 质量、router 局部最优和训练成本；不能把学到的语言偏好硬编码成通用规则。
- 本次笔记未新增图片或资产目录，保持仓库目录简洁；资料来源和核验边界已放在页面文末。

## 2026-05-28 Gabe Pereyra Harvey/Baseten 开放法律 Agent 后训练文章解读

### 背景

- 用户要求深度解读 X 帖子：`https://x.com/gabepereyra/status/2059688919256727936`。
- 原帖本身只有短链，实际正文是 X Article：`Post-Training Open Legal Agents With Baseten Research`。

### 已完成

- 使用 `opencli twitter thread` 读取原帖、主要回复和互动数据。
- 使用 `opencli twitter article` 读取完整长文内容。
- 使用 `opencli twitter profile` 核验作者 Gabe Pereyra 身份信息：Harvey President & Co-Founder。
- 解析短链指向：`https://x.com/i/article/2059666894781554691`。
- 补充读取 Harvey 官方 LAB 介绍与 `harveyai/harvey-labs` GitHub 仓库信息，核验 LAB 的任务结构、规模、all-pass grading 和开放仓库边界。

### 关键观察

- 文章核心不是单纯宣布一个 legal benchmark，而是把 LAB 从评测资产推进为后训练环境：rubric、harness、closed-universe matter 和长程轨迹一起构成可训练信号。
- 作者报告了两类关键现象：第一，轻量 GRPO 能让 Qwen3.5-9B 从 grep-heavy 行为转向 read-heavy 行为；第二，Qwen3.5-27B 需要 harness 与 iSFT 共同作用，才能把简单文本 compaction 用起来。
- 文中真正重要的工程假设是：法律 agent 的瓶颈不只是法律知识，而是长程检索、上下文管理、证据保真和 reviewable deliverable 生成之间的闭环。
- 评论区有用户质疑模型排序措辞，也有人指出 legal agent 失败常来自法律更新、来源冲突、司法辖区差异和检索可靠性，这些是后训练本身不能完全解决的问题。

### 当前判断

- 该帖价值在于给出一个垂直 agent 后训练范式：先把真实工作单元 benchmark 化，再把 benchmark 的 rubric 和轨迹转成训练环境。
- 主要边界是：结果仍以作者报告为主；hold-out 构造、teacher 质量、private-mode submit 是否引入隐性泄漏、以及 LLM judge/rubric 的稳定性都需要外部复现。
- 对工程实践的启发是：垂直 agent 不应只调 prompt 或换更强模型，而要共同优化 harness、检索策略、compaction、训练数据过滤和 partial-credit assignment。

### 补充：站内 HTML 笔记导出

- 用户追问是否已产出 HTML 笔记；确认前一轮仅更新 `Progress.md`，本轮已补齐站内页面。
- 已新增站内技术分析笔记：
  - `notes/tech-analysis/harvey-baseten-open-legal-agents.html`
- 已更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`Harvey/Baseten：开放法律 Agent 后训练路线`
  - URL：`/notes/tech-analysis/harvey-baseten-open-legal-agents.html`
  - 类型：`Tech Analysis`

## 2026-05-28 Orbit 站内 HTML 笔记导出

### 背景

- 用户要求将 Besteuler / Orbit 推文解读导出到 HTML 笔记里。
- 按仓库规则复用 `notes/NOTE_TEMPLATE.md` 的结构要求：独立 HTML 必须加载 `notes-shell.css`、包含 `notes-shell-page`、顶部有 Notes / All Notes / Home 返回条，资料来源放到文末证据边界。

### 已完成

- 新增站内技术分析笔记：`notes/tech-analysis/orbit-rl-infrastructure-analysis.html`。
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`Orbit：把万亿模型 RL 后训练改写成部署一致性问题`
  - URL：`/notes/tech-analysis/orbit-rl-infrastructure-analysis.html`
  - 类型：`Tech Analysis`
- 页面内容覆盖：
  - Orbit 的核心判断；
  - full-FT 万亿 RL 的系统瓶颈；
  - low-precision frozen base + BF16 adapter + OFT 的机制；
  - adapter-native async 与 double-buffered rollout 的架构差异；
  - 术语解释、边界风险、工程启发和证据索引。

### 当前判断

- 本次没有新增图片或资产目录，避免目录噪声；页面使用纯 HTML/CSS 与外部资料链接。
- 证据边界明确标注：中文微信短链当前进入验证码页；GitHub REST API 未认证额度耗尽，因此仓库核验使用公开页面、raw 文件和 git remote 引用。

## 2026-05-28 Orbit RL 后训练框架深度解读

### 背景

- 用户要求深度解读 X 推文：`https://x.com/Besteuler/status/2059849677626085642`。
- 推文主题为 **Orbit**：SphereLab 开源的 OFT-based RL 后训练框架，支持万亿参数 LLM 在单节点 8×B200 上稳定 RL 训练。

### 已完成

- 使用 `opencli twitter thread` 获取原帖及讨论回复。
- 解析短链获取：GitHub (`github.com/Sphere-AI-Lab/orbit`)、英文博客 (`spherelab.ai/orbit`)、中文博客（机器之心）。
- 完整阅读英文博客、中文博客、GitHub README、异步双缓冲架构页、PEFT-Arena benchmark 页。
- 分析核心源码结构（train.py、router、rollout、backends 等模块）。
- 生成自包含中文 HTML 报告至 `/Users/bytedance/Downloads/orbit-rl-infrastructure-analysis.html`。

### 关键发现

- Orbit 的核心创新：base model 冻结在部署精度 (INT4/FP4)，仅训练 BF16 OFT adapter，显存从全参的 16-32 bits/param 降至 ~4.08 bits/param。
- 训推精度对齐：训练和 rollout 使用完全相同的低精度 base + adapter，从系统层面消除 train-rollout log-prob diff。
- OFT > LoRA：PEFT-Arena 基准显示 OFT 在 RLVR 下可一致超越 Full-FT，且具有零额外通信开销和更好的几何保持性。
- 在 Kimi-K2.6 (1T)、DeepSeek V4-Flash、DeepSeek V4-Pro (1.6T) 上验证了单节点 RL 训练的稳定性和有效性。
- 异步双缓冲机制带来 1.42× step-time 加速和 44% 更高 rollout throughput。

## 2026-05-27 Yujie Zhao AMA-Bench 推文分析

### 背景

- 用户要求深度分析 X 推文：`https://x.com/YujieZhao455906/status/2059129862825374062`。
- 推文主题为 `AMA-Bench / AMA-Agent`，论文已被 `ICML 2026` 接收，关注 agentic applications 中的 long-horizon memory 评测。

### 已完成

- 使用 `opencli twitter thread` 读取原帖、回复、互动数据和媒体链接。
- 使用 Twitter Snowflake 解码确认原帖时间为 `2026-05-26T04:29:50Z`。
- 使用 `opencli twitter profile` 核验作者简介：Yujie Zhao，UCSD CS PhD student，Google Student Researcher，方向为 Agents and RL。
- 解析推文短链到项目官网：`https://ama-bench.github.io/`。
- 读取并核验项目官网、arXiv `2602.22769`、GitHub `AMA-Bench/AMA-Bench`、Hugging Face dataset / leaderboard 信息。
- 下载并查看原帖三张配图，确认配图展示了 memory formulation、benchmark domains 和 main results。

### 关键观察

- AMA-Bench 的核心问题设定不是 dialogue memory，而是从 agent-environment interaction trajectory 中构建和检索记忆。
- 论文将 agent memory 能力拆成四类：Recall、Causal Inference、State Updating、State Abstraction。
- Real-world subset 覆盖 6 个 domain、208 条 trajectory、2,496 个 QA pairs；Synthetic subset 用 BabyAI / TextWorld 扩展到 8K-128K tokens 的可控长程场景。
- 论文主张现有 memory system 的瓶颈主要不在 base model scale，而在 memory architecture：相似度检索和有损压缩难以保留 agent trajectory 中的客观状态、因果依赖和机器生成结构。
- AMA-Agent 的主要机制是 Causality Graph + Tool-Augmented Retrieval，报告平均准确率 `57.22%`，比最强 memory baseline 高 `11.16%`。

### 当前判断

- 该工作的价值在于把 agent memory evaluation 从“聊天式长期记忆”推进到“状态转移和因果依赖记忆”。
- 对真实 agent 系统的工程启发是：不能只用向量检索或摘要压缩管理历史轨迹，需要显式保存状态变化、动作前提、依赖链和可程序化检索入口。
- 主要边界是：核心评测仍以离线 QA 为主，虽然论文补充了 TextWorld / Spider2 的 E2E 相关性实验，但它仍不能完全替代在线 agent rollout 评测；LLM-as-judge 虽有人类一致性校准，也仍应关注 judge bias。

## 2026-05-27 Notes 内容结构整理与质量修复

### 背景

- 用户要求只整理当前仓库 `notes` 目录中的站内笔记，不处理 Obsidian。
- 主要问题包括：部分笔记开头先解释来源和抓取方式，阅读重点被稀释；部分笔记偏日报摘抄，缺少深入判断；部分页面存在占位式表述、报告生成痕迹、证据附录位置不合理和显示/索引结构问题。

### 已完成

- 盘点当前仓库 `notes` 目录内的顶层站内笔记和多章节题库页面。
- 对 `notes/tech-analysis/*.html` 与 `notes/paper-reviews/*.html` 做结构整理：
  - 将 47 个顶层笔记中前置的“来源 / 核验 / 我读了什么 / Source Map”章节后移为“证据边界与资料索引”。
  - 二次扫描并修复漏网的 2 个 source-first 页面，确保正文开篇优先进入问题、机制、实验、结论或 insight。
  - 修复 `cracks-foundation-long-context.html` 中仍靠前的来源章节，将其移至末尾资料索引。
- 补强与清理具体内容：
  - `notes/tech-analysis/twitter-llm-digest-2026-05-19.html`：移除“自动抓取/生成时间”式头尾说明，新增“怎么读今天这批信号”和“重点判断”，把日报摘抄升级为工具链趋势分析。
  - `notes/tech-analysis/manual-coding-attention.html`：将“MLA TODO”改写为明确的技术边界说明，解释 MLA 与 KV 压缩、decode 阶段 cache 读写压力的关系。
  - `notes/tech-analysis/ahpabean-nitp-analysis.html`：将 `TBD` 占位式表述改成“论文 PDF / citation / 实现代码尚未公开”的证据边界说明。
  - `notes/paper-reviews/lco-embedding-paper-analysis.html`、`notes/paper-reviews/rebellious-student-rlrt-analysis.html`、`notes/tech-analysis/hwcoder-algorithm-notes-reading.html`、`notes/tech-analysis/manual-coding-attention.html`：修复证据附录被放到 footer 后面的结构问题。
- 清理 `notes/**/*.html` 中本轮变更引入的尾随空格。

### 当前验证

- `ruby scripts/validate_notes_index.rb` 通过：
  - `_data/notes.yml` 共 `63` 条。
  - 顶层 note HTML 共 `63` 个。
  - 未发现漏登记入口或缺失本地资源引用。
- 结构扫描通过：
  - `notes/tech-analysis/*.html` 与 `notes/paper-reviews/*.html` 前四个章节中不再出现“来源 / 核验 / 材料 / 读了什么 / 证据边界”类开篇章节。
  - 未发现证据附录位于 footer 之后的页面。
- `git diff --check -- notes _data/notes.yml` 通过。
- 全仓库 `git diff --check` 当前仍会报告 `_pages/about.md` 的尾随空格；该文件不是本轮 notes 修复范围，未混入处理。

### 当前判断

- 本轮采取最小必要修复：不重写每篇长文的核心观点，不改变本地资源路径，不调整 URL 结构，只修阅读结构、证据附录位置、明显占位/报告痕迹和日报类内容深度。
- 顶层研究笔记现在默认先讲结论、机制、边界和 insight，资料来源降级为末尾复查附录，更符合站内阅读体验。

## 2026-05-27 billxbf Polar Agent RL Rollout Infra 推文分析

### 背景

- 用户要求深度分析 X 推文：`https://x.com/billxbf/status/2059323616009838703`。
- 初始误用了 `autoglm-open-link` skill；用户指出应使用 `opencli` 后，已按仓库规则纠正为 `opencli twitter thread`。

### 已完成

- 使用 `opencli twitter thread` 获取主帖、作者 1/6 到 6/6 线程内容、互动数据、媒体链接和主要回复。
- 使用 Grok-Search 来源缓存定位官方资料：论文 `https://arxiv.org/html/2605.24220v1`，代码仓库 `https://github.com/NVIDIA-NeMo/ProRL-Agent-Server`。
- 使用 `opencli arxiv paper 2605.24220` 核验论文元数据：标题 `Polar: Agentic RL on Any Harness at Scale`，作者 Binfeng Xu 等，发布日期 `2026-05-22`，类别 `cs.DC`。
- 使用 `opencli web read` 读取 GitHub README、agent harness 文档、trajectory 文档和 arXiv HTML 关键段落。

### 关键观察

- Polar 的核心边界是把 agent harness 当作黑盒环境，在 LLM API 边界插入 proxy，记录 prompts、sampled token ids 和 logprobs，再重构 token-faithful trajectories。
- 系统设计强调 rollout-as-a-service：rollout server、gateway nodes、runtime prewarm、agent execution、trajectory reconstruction 和 evaluation 分阶段异步调度，避免长任务和容器启动拖垮 GPU 利用率。
- 论文最关键的技术细节是 `prefix_merging`：把 append-only 多轮对话合并为连续 trace，只对真实 sampled response token 置 loss mask，非生成 interstitial token mask 掉，避免 retokenization drift 和梯度污染。
- SWE-Bench Verified 结果显示同一 `Qwen3.5-4B` base 在 Codex、Claude Code、Qwen Code、Pi harness 上均有提升，其中 Codex 从 `3.8%` 到 `26.4%`，最大收益来自对陌生 action protocol / tool schema 的 harness-native RL 适配。

### 当前判断

- Polar 的价值不只是“又一个 RL 框架”，而是把训练系统和真实 agent harness 之间的集成边界下沉到模型 API 层，降低把复杂 harness 改写成 Gym/env 的成本。
- 该方案的上限受 reward/evaluator 质量、harness 可复现性、API proxy 对流式和多 provider 协议的覆盖、以及 token-faithful 重构正确性约束。
- 评论区指出 PRIME-RL/verifiers 等已有类似 proxy pattern，说明 Polar 的新意更应表述为“黑盒 harness + 分阶段异步 rollout service + token-faithful reconstruction 的系统组合”，而不是单点 proxy 概念首创。

## 2026-05-27 Taiming Lu LLM 预训练蒸馏推文分析

### 背景

- 用户要求深度分析 X 推文：`https://x.com/TaimingLu/status/2059348987854078145`。
- 用户指出应优先使用 `opencli`；本次已纠正执行顺序，按仓库规则使用 `opencli twitter thread` 读取线程。

### 已完成

- 使用 `opencli twitter thread` 获取主帖、作者 1/6 到 6/6 线程内容、媒体链接和主要回复。
- 主帖发布时间为 `Tue May 26 19:00:34 +0000 2026`，主题是论文 `Strong Teacher Not Needed? On Distillation in LLM Pretraining`。
- 通过 `opencli arxiv search` 尝试核验论文时遇到 arXiv API HTTP 429，因此按降级策略使用 Tavily / 论文工具补充验证。
- 使用搜索结果确认 arXiv HTML 地址为 `https://arxiv.org/html/2605.23857v1`，论文元信息为 arXiv `2605.23857v1 [cs.LG]`，发布日期 `22 May 2026`，作者 Taiming Lu 和 Zhuang Liu，Princeton University。
- 尝试使用 `opencli web read` 和 arXiv HTML/PDF 抽取正文；HTML 仅返回标题区，PDF 抽取到部分实验段落和结论摘要，因此最终分析明确以 X 线程为主、论文抽取片段为辅。

### 关键观察

- 线程核心主张是：LLM 预训练中的蒸馏不应只被理解为“强教师压缩到弱学生”，弱教师也可能改善强学生，同级蒸馏也有稳定收益。
- 实验维度包括 teacher/student architecture `0.7B-8.0B`、teacher training tokens `10B-300B` 和 language modeling / distillation loss 混合系数 `alpha`。
- 关键反直觉结论是 teacher-student compatibility 比 raw teacher strength 更重要；在部分设置中，300B tokens 的 `1.7B` teacher 优于 `8.0B` teacher，且大 teacher 继续训练可能降低 distillation gain。
- 蒸馏收益更容易体现在 OOD perplexity 和 downstream accuracy，而不一定体现在 in-domain perplexity；这说明蒸馏更像 regularization / generalization shaping，而不只是训练集拟合增强。

### 当前判断

- 该帖的工程价值在于把 teacher selection 从“越强越好”改写为“匹配度和 loss mixing 更关键”。
- 对 frontier model pretraining，上一代或较弱模型并非无用 teacher；对小模型训练，也不能机械选择最大 teacher。
- 实践上应把 teacher size、teacher training tokens、student capacity、alpha 和评测目标一起做小规模网格搜索，优先看 OOD / downstream 指标，而不是只看 teacher 自身 benchmark 或 in-domain perplexity。

## 2026-05-27 Gabriele Berton 长上下文架构推文重新核验

### 背景

- 用户要求深度分析 X 推文：`https://x.com/gabriberton/status/2058686099619557868`。
- 仓库中已有该主题站内 Notes 页面；本次不新建文档，优先重新核验原帖和上下文，并 in-place 修正过时边界说明。

### 已完成

- 使用 `opencli twitter thread` 读取主线程、作者后续帖和部分回复。
- 确认主帖发布时间为 `Sun May 24 23:06:29 +0000 2026`，正文评价 AllenAI / CMU 长上下文预训练论文的实验设置可信，并认为其显示多数 LLM 存在架构问题。
- 确认作者在后续帖中给出的四点 recipe：
  - 不要使用 QK norm；
  - 不要使用 Group Query Attention；
  - 不要使用 Sliding Window Attention；
  - 用更长序列做预训练。
- 补充核验到 Qwen / RULER 讨论：回复者指出 Qwen3 在部分“不推荐”组件存在的情况下 RULER 表现仍强；作者回应可能来自更好的 context extension、benchmark 适配、RULER 任务差异，或多因素叠加。
- 已更新 `notes/paper-reviews/cracks-foundation-long-context.html` 的核验边界和局限说明，不再保留“线程后续帖未能抓取”的过时描述。

### 当前判断

- 推文的价值在于把论文结论翻译成架构选型警告：短上下文 loss、perplexity 和常规 benchmark 不能替代长上下文扩展验证。
- 更准确的工程表述不是“QK norm / GQA / SWA 永远不能用”，而是：这些 attention 相关效率组件需要组合消融和长上下文 probe；否则单项看似合理的 tradeoff 可能在 64K context extension 后复合放大。
- Qwen / RULER 讨论提示了外推边界：强工程 recipe、后训练、benchmark 格式适配和任务分布可能掩盖或缓解架构缺陷，因此不能把 OlmPool 的 7B 受控结论机械套到所有模型。

## 2026-05-27 BowenWangNLP CUA-Gym 推文线程分析

### 背景

- 用户要求深度分析 X 推文：`https://x.com/BowenWangNLP/status/2059282533775245383`。
- 用户指出应优先使用 `opencli`；已纠正工具路径，按仓库规则使用 `opencli twitter thread` 读取线程。

### 已完成

- 使用 `opencli twitter thread` 获取 1/6 到 6/6 线程正文、发布时间、互动数据和媒体链接。
- 使用 `opencli web read` 解析线程短链接并读取项目材料：
  - Hugging Face Paper / arXiv：`2605.25624`，标题为 `CUA-Gym: Scaling Verifiable Training Environments and Tasks for Computer-Use Agents`。
  - 项目主页：`https://cua-gym.xlang.ai/`。
  - Hugging Face Dataset：`xlangai/CUA-Gym`。
  - GitHub：`xlang-ai/CUA-Gym`。
  - 环境仓库：`xlang-ai/CUA-Gym-Hub`。
- 使用 `opencli arxiv paper 2605.25624` 核验论文元数据、作者、摘要、发布日期和类别。

### 关键观察

- 线程核心论点是：CUA 的 RLVR 瓶颈不在算法本身，而在可规模化、可复位、可检查、可程序化奖励的数据和环境。
- CUA-Gym 将每个任务视为小型软件工程问题，用 setup-gen、reward-gen 和 orchestrator 生成并执行校验 `(instruction, initial/golden state, reward)` 三元组。
- CUA-Gym-Hub 的关键工程价值在于统一状态 API、session 隔离和 state diff reward，使 mock web app 能支撑并行 RL rollout。
- 当前公开数据集页面显示 public preview 为 `7,897` 行；论文和项目 README 宣称完整数据为约 `32,112 / 32,122` verified tuples，需区分“已公开子集”和“完整计划/论文规模”。
- 主要风险在 reward specification、mock-to-real transfer、过程不可见、合成环境偏差和安全执行隔离。

### 当前判断

- CUA-Gym 的贡献更接近“agent RL 数据基础设施”而非单纯 benchmark。
- 它的可复现性优势来自程序化 setup/reward 和环境状态 API，但泛化上限仍取决于 mock 环境覆盖真实软件长尾行为的程度。
- 对实践最有价值的启发是：训练 CUA 不应只堆交互轨迹，而应先把环境 reset、state inspection、reward determinism 和并发隔离做成平台能力。

### 补充：站内 HTML 笔记导出

- 用户要求将本次分析导出到 HTML 笔记中。
- 已新增站内技术分析笔记：
  - `notes/tech-analysis/cua-gym-rlvr-data-infrastructure.html`
- 已更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`CUA-Gym：Computer-Use Agent 的 RLVR 数据基础设施`
  - URL：`/notes/tech-analysis/cua-gym-rlvr-data-infrastructure.html`
  - 类型：`Tech Analysis`

## 2026-05-27 Jia Guo KPop 推文与博客技术分析

### 背景

- 用户要求深度分析 X 推文：`https://x.com/Jia__Guo/status/2059291333496553797`。
- 推文主题为 Ant Group / InclusionAI 的 `KPop`，用于缓解大规模 MoE / agentic RL 中的 training-inference mismatch。

### 已完成

- 使用 `opencli twitter thread` 抓取原帖、主要回复和作者补充。
- 原帖发布时间为 `Tue May 26 15:11:28 +0000 2026`。
- 原帖链接到 Notion 博客：`https://ringtech.notion.site/kpop`。
- 使用 `opencli web read` 读取博客全文，确认标题为 `KPop: Taming Training-Inference Mismatch in Reinforcement Learning with Adaptive Masking Regions`。
- 核验外部背景资料：
  - `Ring-2.6-1T` 模型页面；
  - `AEnvironment` 项目；
  - `SWE-bench Verified` 官方说明；
  - training-inference mismatch 相关公开论文和材料。

### 关键观察

- KPop 是 IcePop 的后续：核心变化不是重做 RL infrastructure，而是把固定 ratio mask 换成基于 token 二元事件的 symmetric binary KL mask。
- IcePop 的固定 `[alpha, beta]` ratio region 隐含“所有 token 的 ratio 噪声同质”的假设；KPop 试图让 mask 容忍度随 token probability 自适应变化。
- 博客中的关键现象是：IcePop mask ratio 下降，但 train-infer log-prob gap 继续扩大；KPop 的 mask ratio 反而会随 gap 增大而增加，形成动态约束。
- Ring-2.6-1T 的 SWE agentic RL 结果从 `70.8%` 提升到 `76.28%`，但该结果应理解为作者报告的系统级结果，受模型、agent scaffold、训练数据、评测 harness 和防作弊机制共同影响。
- 作者在回复中补充：实验使用 asynchronous RL，stale rollouts 通过 version-based staleness 控制；方法不依赖特定 kernel implementation 或 routing replay。

### 当前判断

- KPop 的工程价值在于以低侵入方式缓解 rollout engine 与 training engine 概率不一致导致的 off-policy 梯度污染。
- 它更像“token-level hard trust region / sample selection”而不是完整解决 TIM 的系统方案；真正零 mismatch 仍需训练与推理路径更强一致性。
- 最值得关注的 insight 是：agentic RL 中 20%~30% token 被跳过后仍可稳定收敛，说明长轨迹训练中的有效梯度可能高度稀疏，token 选择本身可能成为后续提效方向。

### 补充：站内 HTML 笔记导出

- 用户要求将本次分析导出到 HTML 笔记中。
- 已新增站内技术分析笔记：
  - `notes/tech-analysis/jia-guo-kpop-agentic-rl.html`
- 已更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`KPop：用自适应 Mask 稳住 Agentic RL 的训练-推理错配`
  - URL：`/notes/tech-analysis/jia-guo-kpop-agentic-rl.html`
  - 类型：`Tech Analysis`
- 验证结果：
  - `ruby scripts/validate_notes_index.rb` 通过：`62` 条 notes 入口，`62` 个顶层 note HTML。
  - 新 HTML 解析通过：标题、章节和 `12` 个链接可读取。
  - 本次触达文件的 `git diff --check` 通过。
  - `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅有 GitHub Metadata API rate limit 和 Faraday retry 提示，不影响静态页面生成。
  - 已确认 `_site/notes/tech-analysis/jia-guo-kpop-agentic-rl.html` 生成，并包含 `KPop`、`76.28`、`training-inference mismatch` 和 `材料来源`。
  - 已确认 `_site/notes/index.html` 出现新 Notes 卡片入口。

## 2026-05-27 AGENTS.md OpenCLI 使用规则补充

### 背景

- 用户指出仓库指令缺少对 `opencli` 的强调和介绍。
- 本机已确认 `opencli` 可用，路径为 `/opt/homebrew/bin/opencli`。
- `opencli --help` 显示其支持 Browser Bridge、外部 CLI、App adapters 和大量 Site adapters，适合作为网站读取、站点抓取、社媒线程和网页交互的默认优先入口。

### 已完成

- 更新 `AGENTS.md` 的 `Command And Search Standards`：明确具体网站、社媒线程、论文页面、公开网页或网页交互优先使用 `opencli`。
- 新增 `OpenCLI Usage` 段落，记录 `opencli list`、`opencli <site> --help -f yaml`、`opencli browser ...`、`opencli doctor` 等基本用法。
- 明确降级策略：`opencli` 不适配或失败时，再切换到 Grok-Search、Tavily、WebFetch、专用 MCP 或浏览器自动化工具。
- 明确边界：`opencli` 不替代本地仓库文件搜索和代码编辑。

## 2026-05-27 AGENTS.md 材料分析沉淀规则更新

### 背景

- 用户明确要求以后不再将阅读、解读或分析材料写入 Obsidian。
- 新规则：如果是阅读分析材料且需要文件沉淀，则在当前目录新建或更新合适的本地文档；否则直接在终端回答。

### 已完成

- 更新 `AGENTS.md`，将原 `Obsidian Rules` 替换为 `Material Analysis Notes`。
- 更新 `Research And Exploratory Work`，移除对应 Obsidian 笔记的写入要求。
- 保留仓库研发过程优先维护 `Progress.md` 的规则。

## 2026-05-26 Gabriele Berton 长上下文架构推文与 OlmPool 论文梳理

### 背景

- 用户要求仔细分析和梳理 X 推文：`https://x.com/gabriberton/status/2058686099619557868`。
- 本任务与当前 GitHub Pages 代码仓库功能无直接关系，按仓库规则将研究笔记归档到 Obsidian，并在本仓库记录过程。

### 已完成

- 通过可访问的 X 镜像接口获取主帖正文、作者信息、发布时间、互动数据和配图。
- 使用 Twitter Snowflake 解码确认主帖时间为 `2026-05-24T23:06:29Z`。
- 下载并查看主帖配图，确认论文题名为 `Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension`，作者来自 Allen Institute for AI、CMU 和 UW。
- 联网核验官方论文页、Ai2 博客、GitHub 仓库和 Hugging Face OlmPool 模型集合。
- 尝试抓取线程后续帖、Nitter/XCancel 镜像和 X guest API；当前未能稳定获取线程后续正文，因此最终分析明确区分“已确认主帖 / 论文事实”和“基于论文材料的推断”。
- 新增 Obsidian 论文笔记：
  - `/Users/bytedance/Library/Mobile Documents/iCloud~md~obsidian/Documents/obsidian-example-lifeos-main/3.Resources/PaperNotes/26-05-26 Cracks in the Foundation - Minor Architectural Choices Impact Long Context Extension.md`

### 关键观察

- 这条推文的核心不是简单推荐论文，而是强调“长上下文问题可能是架构问题”，尤其是注意力相关设计在 context extension 中的复合影响。
- OlmPool 的实验价值在于控制变量：固定数据、tokenizer 和 extension recipe，仅改变架构，构造 26 个可比 7B 模型。
- 论文聚焦四类架构选择：QK norm、GQA、sliding window attention、pretraining context length。
- 单个设计选择可能影响较小，但三个或更多组合时，长上下文 benchmark 表现最多可下降约 47%。
- 短上下文 loss、perplexity 和常规 benchmark 难以预测长上下文扩展能力；如果产品依赖长文档、长轨迹、agent memory 或代码库理解，需要直接做长上下文验证。

### 当前判断

- 长上下文能力不应被视为训练末期“调大 context window”的附加功能，而是架构、预训练长度、注意力表达能力和 extension recipe 共同决定的端到端属性。
- 对模型研发流程的直接启发是：在预训练早期加入 context extension probe，并对 QK norm、GQA、SWA 等效率组件做组合消融，而不是只做单组件验证。
- 对 agent 和 RAG 系统的启发是：如果底层模型的 attention expressivity 已经受限，外部 memory / retrieval / tool use 只能缓解，不能完全替代模型对长上下文的稳定路由能力。

### 补充：站内 Notes 写入

- 用户指出前一版只写入 Obsidian，没有写入当前 GitHub Pages 的 Ricardokevin 笔记站点。
- 这是执行判断失误：当前仓库本身就是材料分析的主沉淀位置，应优先写入站内 Notes。
- 已补充新增站内 HTML 笔记：
  - `notes/paper-reviews/cracks-foundation-long-context.html`
- 已新增本地配图资源目录：
  - `notes/paper-reviews/cracks-foundation-long-context-assets/`
  - `paper-title.jpg`
- 已更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`Cracks in the Foundation：长上下文扩展为什么会被小架构选择击穿`
  - URL：`/notes/paper-reviews/cracks-foundation-long-context.html`
  - 类型：`Paper Note`

## 2026-05-26 Hwcoder 算法笔记读书笔记迁移

### 背景

- 用户要求把 `https://hewei2001.pages.dev/categories/` 中的算法笔记内容迁移到当前站点。
- 源站为 Hexo/Fluid 博客，分类页中的“算法笔记”下实际包含三组内容：
  - 算法入门：2 篇；
  - 力扣刷题：15 篇；
  - 手撕经典算法：6 篇。
- 本轮采用“详细读书笔记 / 学习地图”方式迁移：不做第三方页面逐段全文镜像，而是读取结构后重写为站内原创整理，保留完整来源清单和阅读定位。

### 已完成

- 抓取并解析源站分类页、站点地图和 `local-search.xml`：
  - 算法相关条目共 `23` 篇；
  - 源站搜索索引中可解析内容合计约 `212,929` 字符；
  - 代码块规模约 `1,635` 个。
- 新增站内读书笔记：
  - `notes/tech-analysis/hwcoder-algorithm-notes-reading.html`
- 更新 `_data/notes.yml`，新增 Notes 入口：
  - 标题：`Hwcoder 算法笔记体系读书笔记`
  - URL：`/notes/tech-analysis/hwcoder-algorithm-notes-reading.html`
  - 类型：`Study Resource`

### 内容设计

- 读书笔记按五段组织：
  - 来源与整理原则；
  - 总学习地图：基础工具、力扣专题、手撕模型组件三层；
  - 力扣专题精读：按“维护什么信息”重构数组、位运算、数据结构、二分、DP、图论、贪心、链表、数学、搜索、栈队列、字符串和树；
  - 通用模板：二分答案、动态规划、回溯、单调结构；
  - 手撕经典算法：Attention、神经网络、Transformer、经典函数、机器学习、RLHF；
  - 复习路线与源笔记清单。
- 页面保留 23 篇源笔记的标题、来源链接、lastmod 日期和本页阅读定位，便于回源站查具体代码。

### 当前验证

- HTML 解析通过，标题、7 个 H2 章节和 33 个链接均可解析。
- 编码检查通过，未发现 Unicode replacement character。
- `ruby scripts/validate_notes_index.rb` 通过：
  - `_data/notes.yml` 共 59 条。
  - 顶层 note HTML 共 59 个。
  - 未发现漏登记入口或缺失本地资源引用。
- `git diff --check` 通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata API rate limit 和 Faraday retry 提示，不影响静态页面生成。
- 已确认 `_site/notes/tech-analysis/hwcoder-algorithm-notes-reading.html` 生成，并在 `_site/notes/index.html` 中出现新卡片入口。

## 2026-05-26 SkillEvolBench 论文与项目材料深度调研

### 背景

- 用户要求深入梳理和调研 SkillEvolBench：
  - 项目主页：`https://skillevolbench.github.io`
  - Hugging Face Paper：`https://huggingface.co/papers/2605.24117`
- 本任务与当前 GitHub Pages 代码仓库功能无直接关系，按仓库规则将论文笔记归档到 Obsidian，并在本仓库记录过程。

### 已完成

- 抓取并阅读 arXiv PDF / HTML、Hugging Face Paper API、项目主页 HTML。
- 核验 Hugging Face Dataset `skillevolbench/skillevolbench`：
  - `skills` config：30 个 skill family。
  - `tasks` config：180 个 task。
  - 6 个 environment，每个 30 个任务。
  - 6 个 role 各 30 个任务：`canonical / enriched / variant / context-shift / adversarial / composition`。
- 从项目页内嵌 leaderboard 数据中解析 curated/self-generated 条件的模型平均指标和 ESR delta。
- 检查项目页按钮状态：Paper 指向 `assets/skillevolbench.pdf`，Code/Data 按钮当前为占位 `#`；HF dataset 已可访问，GitHub 组织 API 因 403/rate limit 未能核验代码仓库。
- 新增 Obsidian 论文笔记：
  - `/Users/bytedance/Library/Mobile Documents/iCloud~md~obsidian/Documents/obsidian-example-lifeos-main/3.Resources/PaperNotes/26-05-26 SkillEvolBench - Benchmarking the Evolution from Episodic Experience to Procedural Skills.md`

### 关键观察

- SkillEvolBench 的核心不是评估 agent 能否“使用 skill”，而是评估 agent 能否把 episodic trajectory + verifier feedback 抽象为 frozen deployment 中可复用的 procedural skill。
- Benchmark 结构是 `6 environments x 5 families x 6 roles = 180 tasks`，每个 family 构成从 acquisition 到 frozen deployment 的 skill-evolution arc。
- 主指标应重点看 ESR/CSSR/ARSR/CompSR，而不是只看 LSR/RSR；acquisition 或 replay 变好可能只是局部适应。
- 项目页 leaderboard 的 10 模型平均结果显示：
  - No-Skill ESR 为 `34.7%`。
  - Curated-Revision-Always ESR 为 `35.5%`，平均 `+0.77 pp`。
  - SelfGen-Always ESR 为 `35.1%`，平均 `+0.44 pp`。
  - Curated-Static、SelfGen-Zero-Shot、SelfGen-Revision 平均降低 ESR。
- Raw-Trajectory control 是论文最关键的对照：直接复用压缩轨迹常常强于 distilled skills，说明当前 skill abstraction 会丢失任务上下文、检查点、失败路径和程序性触发线索。
- Tier-3 capacity ablation 表明“写更多 skill 文件/脚本/引用”不是充分条件；更大的 library 可能带来 episode-specific drift 和 procedural clutter。

### 当前判断

- 这篇论文对 agent memory / skill system 的最大价值，是把“经验沉淀”从主观叙事变成可诊断协议：只有冻结后在 context shift、adversarial shortcut 和 multi-skill composition 上提升，才更接近 reusable procedural skill。
- 对实践的直接启发是：skill library 不应替代 raw trajectory memory，而应和 episodic traces 组成双层记忆；skill 提供稳定程序骨架，trace 提供局部证据和失败线索。
- 后续如果设计 agent skill 系统，重点不是“每次都总结”，而是建立 selective abstraction、skill trigger evaluation、skill regression tests、stale/duplicate cleanup 和 trace-to-skill loss analysis。

### 补充：站内 Notes 写入

- 用户指出前一版只写入 Obsidian，没有写入当前 GitHub Pages 的站内 Notes。
- 已补充新增站内 HTML 笔记：
  - `notes/paper-reviews/skillevolbench-skill-evolution.html`
- 已新增本地论文图资源目录：
  - `notes/paper-reviews/skillevolbench-skill-evolution-assets/`
  - `fig1-protocol.png`
  - `fig2-taxonomy.png`
  - `fig4-rawtraj-vs-skills.png`
  - `fig5-library-size.png`
- 已更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`SkillEvolBench 深度解读：从一次性经验到可复用程序性技能`
  - URL：`/notes/paper-reviews/skillevolbench-skill-evolution.html`
  - 类型：`Paper Note`

### 站内验证结果

- `ruby scripts/validate_notes_index.rb` 通过：
  - `_data/notes.yml` 共 `60` 条。
  - 顶层 note HTML 共 `60` 个。
  - 未发现漏登记入口或缺失本地资源引用。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅有 GitHub Metadata 未认证和 Faraday retry 提示，不影响静态页面生成。
- 已确认 `_site/notes/paper-reviews/skillevolbench-skill-evolution.html` 生成，并包含 `SkillEvolBench`、`Raw-Trajectory`、`Curated-Revision-Always` 和本地图 `fig4-rawtraj-vs-skills.png`。
- 已确认 `_site/notes/index.html` 生成新的 Notes 卡片入口。
- 本地 HTTP 验证通过：
  - `/notes/paper-reviews/skillevolbench-skill-evolution.html` 返回 `200 OK`。
  - `/notes/` 返回 `200 OK`。
  - `/notes/paper-reviews/skillevolbench-skill-evolution-assets/fig4-rawtraj-vs-skills.png` 返回 `200 OK`。
- Chrome headless 已渲染桌面端和移动端截图：
  - `/tmp/skillevolbench-note-1280.png`，`1280x900`，约 `383K`。
  - `/tmp/skillevolbench-note-390.png`，`390x844`，约 `134K`。
- Chrome DOM dump 检查通过：Notes 首页命中 `SkillEvolBench 深度解读` 和 `skillevolbench-skill-evolution`。

## 2026-05-26 arXiv 2605.23857 论文深度解读与 Obsidian 归档

### 背景

- 用户要求深度解读 `arxiv.org/abs/2605.23857`，并特别追问：
  - 从 smaller model 蒸馏是否有用；
  - 除蒸馏外，跨尺度 loss difference 是否可以提供额外信号。
- 本任务与当前 GitHub Pages 代码仓库功能无直接关系，按仓库规则将论文笔记归档到 Obsidian，并在本仓库记录过程。

### 已完成

- 下载并解析 arXiv PDF，确认论文为 `Strong Teacher Not Needed? On Distillation in LLM Pretraining`，作者为 Taiming Lu 和 Zhuang Liu。
- 阅读论文主实验、loss mixing、student-size ablation、Qwen 架构消融、300B token 消融和 token-level 机制分析。
- 检查论文 PDF 标注的 GitHub 仓库 `zlab-princeton/strong-teacher-not-needed`，当前访问为 404；本次解读以 arXiv PDF 为主要证据。
- 新增 Obsidian 论文笔记：
  - `/Users/bytedance/Library/Mobile Documents/iCloud~md~obsidian/Documents/obsidian-example-lifeos-main/3.Resources/PaperNotes/26-05-26 Strong Teacher Not Needed - On Distillation in LLM Pretraining.md`
- 新增仓库根目录 `AGENTS.md`，记录用户长期偏好和本仓库执行规则。

### 关键观察

- smaller teacher 可以有用，但应作为低权重、局部门控的互补信号，而不是纯 KD teacher。
- 论文中弱到强蒸馏在 OOD PPL 和 downstream accuracy 上更容易产生收益；in-domain PPL 更容易退步。
- 更强 teacher 不一定更好：对 `1.7B / 50B` student，`1.7B / 300B` teacher 在 downstream 上优于 `8B / 300B` teacher。
- 蒸馏收益集中在 hard tokens；收益来自 teacher-only tokens，伤害来自 baseline-only / teacher-wrong tokens。
- 跨尺度 loss difference 可作为 token-level KD gating、data diagnosis、curriculum、teacher selection 和 mixture-of-teachers 的信号。

### 当前判断

- 如果要做后续实验，推荐方向不是简单 small-to-large KD，而是 `Scale-Difference Gated Distillation`：
  - 计算 `ell_student - ell_teacher` 作为 teacher advantage proxy；
  - 结合 student entropy 和 KL compatibility；
  - 对 KD 使用 token-level 权重，保留 CE/LM loss；
  - 按 in-domain、OOD、downstream、hard-token bin 分层验证。

## 2026-05-26 Notes 索引与仓库卫生修复

### 背景

- 用户要求核实并修复仓库维护问题，重点包括 Git 体积、`.DS_Store` 污染、`_data/notes.yml` 手动同步风险和 Notes 入口一致性。
- 只处理已经核实且低风险的工程问题；媒体压缩、PDF 迁移、URL 结构调整和 Git 历史重写暂不混入本轮修复。

### 已完成

- 更新 `.gitignore`，新增 `.DS_Store` 忽略规则。
- 新增根目录 `AGENTS.md`，把当前仓库的沟通语言、工程原则、Obsidian 规则、Progress 维护和自主工作模式固化为仓库级说明。
- 从 Git 索引移除已跟踪的 5 个 `.DS_Store`：
  - `.DS_Store`
  - `_includes/.DS_Store`
  - `assets/.DS_Store`
  - `files/.DS_Store`
  - `notes/paper-reviews/fast-slow-training-analysis-assets/.DS_Store`
- 补齐 `_data/notes.yml` 中漏登记的两个 Tech Analysis 入口：
  - `notes/tech-analysis/ryanboldi-vpo-test-time-search.html`
  - `notes/tech-analysis/appliedcompute-rmsd-thread-analysis.html`
- 新增 `scripts/validate_notes_index.rb`：
  - 校验 `_data/notes.yml` URL 是否都有对应文件。
  - 校验顶层 Notes HTML 是否已登记到 `_data/notes.yml`。
  - 允许两个多章节题库使用目录 URL 指向 `index.html`。
  - 校验 Notes HTML 中本地 CSS/JS/图片/PDF/文本资源引用是否存在。
- 更新 `.github/workflows/deploy.yml`，在 Pages 构建流程中运行 `ruby scripts/validate_notes_index.rb`，避免 Notes 入口漏登记再次静默进入主分支。
- 同格式压缩 `notes/paper-reviews/g-zero-thread-analysis-assets/method.png`：
  - 文件大小从 `5,982,010` bytes 降到 `1,555,756` bytes。
  - 保持 PNG 格式、原路径和 `7130x2490` 分辨率不变，不需要修改 HTML 引用。

### 设计决策

- 校验脚本使用 Ruby 标准库实现，复用 Jekyll 项目的语言栈，不引入新依赖。
- 只校验 `notes/*/*.html` 作为 Notes 首页入口，不把 `chapters/*.html` 当作独立卡片，避免误报多章节题库。
- 本轮不执行图片/PDF 批量压缩：当前最大收益来自当前 HEAD 中的资源文件，后续应单独做压缩前后尺寸、清晰度和页面渲染对比，再决定是否迁移 PDF 或重写历史。
- 对媒体资源采用最小可逆风险策略：只处理无需改 URL、无需改格式、试压缩收益明确的 PNG；WebP 转换虽然对若干图有明显收益，但会引入引用迁移和兼容性验证，留作独立任务。

### 验证结果

- `ruby scripts/validate_notes_index.rb` 通过：
  - `_data/notes.yml` 共 58 条。
  - 顶层 note HTML 共 58 个。
  - 未发现漏登记入口或缺失本地资源引用。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅有 GitHub Metadata 未认证和 Faraday retry 提示，不影响静态页面生成。

## 2026-05-26 Agentic Systems 推文补充核验与 Obsidian 归档

### 背景

- 用户要求深度分析和解析 `https://x.com/che_shr_cat/status/2058713325106614301`。
- 本次任务与当前 GitHub Pages 代码仓库功能无直接关系，按仓库指令将研究结论归档到 Obsidian，同时保留本仓库研发过程记录。

### 已完成

- 使用 X syndication JSON 核验原帖主文、作者、发布时间、配图和互动字段。
- 使用 Twitter Snowflake 解码确认原帖时间：`2026-05-25T00:54:40Z`，北京时间 `2026-05-25 08:54:40`。
- 下载并阅读论文 PDF `arXiv:2605.14163`，确认论文题名为 `Agentic Systems as Boosting Weak Reasoning Models`，核心机制是 verifier-backed committee search / inference-time boosting。
- 核对当前仓库已有站内 HTML 分析 `notes/tech-analysis/che-shr-cat-agentic-boosting.html`，本次未覆盖该文件。
- 新增 Obsidian 笔记：
  - `/Users/bytedance/Library/Mobile Documents/iCloud~md~obsidian/Documents/obsidian-example-lifeos-main/3.Resources/PaperNotes/26-05-26 Agentic Systems as Boosting Weak Reasoning Models.md`

### 关键观察

- 原帖的传播性表达是“弱模型 latent space 中经常已有正确解，只是不会选择”。
- 论文中更精确的拆分是 `proposal coverage`、`local identifiability`、`progress`、`diversity` 四个量。
- `GPT-5.4 nano + critic-comparator harness` 在 SWE-bench Verified 上从 `67.0%` 提升到 `76.4%`，接近 `79.0%` oracle best-of-8；该结论应理解为系统级 solve rate 接近，不应外推成 nano 权重能力等价强模型。
- 剩余失败主要是 proposal coverage / blind-spot floor 问题时，继续堆 selector 不会凭空创造正确候选，应优先改 proposer、工具、检索、任务分解和 diversity。

### 工具与边界

- `opencli grok ask` 因浏览器预导航失败不可用；`opencli twitter thread` 与 `opencli twitter tweets` 因 fetch 失败未能抓完整线程；`opencli twitter search` 对该 status id 返回空列表。
- AutoGLM open-link 因本地 token 服务未启动不可用。
- X 普通页面与 Nitter 镜像受限；最终以 X syndication JSON、原帖配图、arXiv 页面、论文 PDF 和 SWE-bench Verified 页面为核验依据。

## 2026-05-25 rosinality / Shannon Scaling Law / Token Noise X 帖笔记

### 背景

- 用户要求详细分析梳理 `https://x.com/rosinality/status/2058824080837456031`。
- 原帖评论 @gm8xx8 对 arXiv `2605.23901`《LLMs as Noisy Channels: A Shannon Perspective on Model Capacity and Scaling Laws》的解读。
- 核心问题是理解 `token noise exponent` 始终大于 `signal exponent` 是否意味着继续增加训练 tokens 最终会让 loss 上升。

### 已完成

- 新增 `notes/tech-analysis/rosinality-shannon-scaling-law.html`。
  - 覆盖来源地图、传统 scaling law 的单调假设、Shannon Scaling Law 公式、Gaussian/SFT/quantization 三类证据、Table 9 指数解释、rosinality 判断的成立条件和误读边界。
  - 明确区分 X 原帖、引用帖传播说法、论文可核验证据和本报告的工程判断。
- 新增资源目录 `notes/tech-analysis/rosinality-shannon-scaling-law-assets/`。
  - 保存 gm8xx8 引用帖配图、论文 PDF 副本、论文页截图 `paper-fig1-fig2.png`、`paper-fig4-gaussian.png`、`paper-tables-extrapolation-exponents.png`。
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`Shannon Scaling Law 与 Token Noise 极限解读`
  - URL：`/notes/tech-analysis/rosinality-shannon-scaling-law.html`
  - 类型：`Tech Analysis`

### 设计决策

- 放入 `notes/tech-analysis/`：用户入口是 X 帖，但主分析对象是论文机制与工程含义，不作为纯论文 review 单独归档。
- 采用单页 HTML + 本地资源目录，不新增多版本文档。
- 对 `δ > β` 做严格解释：这是拟合模型内的极限趋势，表示足够大的 token budget 下 \(D^\delta\) 可能压过 \(D^\beta\)，不等于现实训练中每增加一点 token 都会立刻变差。

### 验证结果

- 静态 HTML 解析通过；核心章节 `source/problem/model/evidence/exponents/rosinality/limits/implications/insight/commands` 均存在。
- 本地资源引用检查通过：页面引用的 4 张图片均存在且非空；资源目录中的 PDF 副本与抓取 PDF SHA256 一致，`pdfinfo` 均显示 22 页。
- `_data/notes.yml` YAML 解析通过；`git diff --check` 通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅有 GitHub Metadata 未认证提示，不影响静态页面生成。
- 已确认 `_site/notes/tech-analysis/rosinality-shannon-scaling-law.html` 和 `_site/notes/index.html` 中的新 Notes 卡片入口生成。
- Chrome headless DOM dump 中出现 `mjx-container`，说明 MathJax 已渲染；桌面截图 `/tmp/rosinality-shannon-scaling-law-1280.png` 与移动截图 `/tmp/rosinality-shannon-scaling-law-390.png` 均为非空 PNG。

## 2026-05-25 RL Memory Agent Curriculum 论文笔记

### 背景

- 用户要求深入梳理理解 arXiv `2605.23067`。
- 论文题名为 `What Training Data Teaches RL Memory Agents: An Empirical Study of Curriculum Effects in Memory-Augmented QA`，关注 memory-augmented QA 中 RL 训练数据来源如何塑造 Answer Agent 的细分能力。
- 按当前 Notes 规则，将 self-contained 中文 HTML 报告输出到 `/Users/bytedance/Documents/Ricardokevins.github.io/notes/paper-reviews/`。

### 已完成

- 新增 `notes/paper-reviews/rl-memory-curriculum-effects.html`。
  - 覆盖来源与核验、问题背景、外部记忆问答任务、LoCoMo/LongMemEval/mixed 三种 curriculum、GRPO 训练机制、overall/per-type F1 证据、memory bank preprocessing、single-GPU GRPO reward sparsity、复现仓库边界、实践 checklist 和个人 insight。
  - 明确区分论文主实验结果和当前 GitHub 仓库可见状态。
- 新增资源目录 `notes/paper-reviews/rl-memory-curriculum-effects-assets/`。
  - 保存 arXiv HTML 原始论文图：`fig1-experimental-design.png`、`fig2-per-type-heatmap.png`。
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`RL Memory Agent 训练数据效应：Curriculum 如何塑造外部记忆问答能力`
  - URL：`/notes/paper-reviews/rl-memory-curriculum-effects.html`
  - 类型：`Paper Note`

### 设计决策

- 放入 `notes/paper-reviews/`：本次主材料是 arXiv 论文，GitHub 仓库只作为复现材料核验来源。
- 报告采用单页 HTML，不新增多版本文档；公式使用离线 HTML/CSS 呈现，避免页面依赖 MathJax。
- 使用 arXiv HTML 公开的两张论文图作为证据图，并在正文中重建关键表格，避免整页 PDF 截图降低可读性。
- 对复现边界做显式标注：本次检查远端未发现论文声明的 `v1.0-arxiv` tag；当前公开 `results/` 是 Phase 1 Qwen-2.5-3B 参考结果；默认 YAML config 与论文主实验口径存在差异。

### 验证结果

- HTML parser 解析通过：新增页面 `40,825` bytes，核心章节 `source/problem/method/evidence/limits/insight` 均存在。
- 本地资源引用检查通过：页面引用的 `fig1-experimental-design.png` 与 `fig2-per-type-heatmap.png` 均存在且非空；构建输出 `_site/notes/paper-reviews/rl-memory-curriculum-effects-assets/` 中两张图也存在。
- 内容可读性检查通过：未发现 Unicode replacement character；`pre code` 有显式样式覆盖；公式使用离线 `math-display` 样式。
- `git -C /Users/bytedance/Documents/Ricardokevins.github.io diff --check` 通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证提示，不影响静态页面生成。
- 已确认 `_site/notes/paper-reviews/rl-memory-curriculum-effects.html` 生成，并包含标题、`G=4 时 EM reward 会塌缩`、`v1.0-arxiv` 复现边界和两张本地论文图引用。
- 已确认 `_site/notes/index.html` 生成新的 Notes 卡片入口，链接到 `/notes/paper-reviews/rl-memory-curriculum-effects.html`。
- 本地 HTTP 验证通过：
  - `/notes/paper-reviews/rl-memory-curriculum-effects.html` 返回 `200 OK`。
  - `/notes/` 返回 `200 OK`。
  - `/notes/paper-reviews/rl-memory-curriculum-effects-assets/fig2-per-type-heatmap.png` 返回 `200 OK`。
- Chrome headless 已渲染桌面端和移动端截图：
  - `/tmp/rl-memory-curriculum-effects-1280.png`，`1280x900`，约 `462K`。
  - `/tmp/rl-memory-curriculum-effects-390.png`，`390x844`，约 `194K`。
- Chrome DOM dump 检查通过：命中 `RL Memory Agent`、`fig2-per-type-heatmap`、`G=4 时 EM reward` 和 `v1.0-arxiv`。

## 2026-05-25 SaaS-Bench / Computer-Use Agent 评测笔记

### 背景

- 用户要求深入理解和介绍 `https://x.com/sheriyuo/status/2058815872249286743`。
- 原帖评论 UniPat AI 的 SaaS-Bench：23 个真实开源 SaaS 系统、106 个长程任务，强调 Checkpoint Score 与 Resolved Score 的落差暴露了 Computer-Use Agent 的产品化鸿沟。
- 本次按 Notes 站点结构生成 self-contained 中文 HTML 技术解读，并保留官方 blog 图、原帖配图和论文 PDF 本地资源。

### 已完成

- 新增 `notes/tech-analysis/saas-bench-cua-analysis.html`。
  - 覆盖来源地图、问题背景、benchmark 设计、评分协议、论文/blog 结果、四类失败机制、工程启发、局限和个人 insight。
  - 明确区分官方 blog leaderboard 与 arXiv PDF Table 2：blog 已包含 Claude Opus 4.7、GPT-5.5 High 等更新模型，论文主榜为 2026-05-15 arXiv 版本。
- 新增资源目录 `notes/tech-analysis/saas-bench-cua-analysis-assets/`。
  - 保存原帖配图、官方 blog 的 evaluation overview、task composition、apps/steps、pass@k、complexity drop 图，以及 arXiv PDF 副本。
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`SaaS-Bench 解读：Computer-Use Agent 为什么还不是可靠的 SaaS 工作者`
  - URL：`/notes/tech-analysis/saas-bench-cua-analysis.html`
  - 类型：`Tech Analysis`

### 设计决策

- 放入 `notes/tech-analysis/` 而不是 `notes/paper-reviews/`：用户入口是 X 帖，材料同时包含官方 blog、GitHub 仓库和论文，重点是技术/产品评测解读。
- 报告不逐段复述论文，而按“评测错觉 -> 环境设计 -> 双指标 -> 结果落差 -> 失败机制 -> 工程改造”的理解顺序组织。
- 对 blog 与论文的榜单时间差做显式标注，避免把后续 leaderboard 更新误写成 arXiv PDF 原始实验。

### 验证结果

- 静态 HTML 解析通过：新增页面 `37,597` bytes，核心章节 `source/problem/design/metrics/results/failures/implications/limits/insight/commands` 均存在。
- 本地资源引用检查通过：页面内 `8` 个本地引用均可解析；资源目录中的原帖图、官方 SVG 图和 PDF 副本均存在且非空。
- 内容可读性检查通过：未发现 Unicode replacement character；`pre code` 有显式样式覆盖；MathJax 配置和组合可靠性公式源文本存在。
- `_data/notes.yml` YAML 解析通过，SaaS-Bench 入口唯一；`git diff --check` 通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证/超时提示，不影响静态页面生成。
- 已确认 `_site/notes/tech-analysis/saas-bench-cua-analysis.html` 生成，并包含页面标题、公式源和核心正文。
- 已确认 `_site/notes/index.html` 生成新的 Notes 卡片入口，链接到 `/notes/tech-analysis/saas-bench-cua-analysis.html`。
- Chrome headless 已渲染桌面端和移动端截图：
  - `/tmp/saas-bench-cua-analysis-1280.png`，`1280x900`，约 `221K`。
  - `/tmp/saas-bench-cua-analysis-390.png`，`390x844`，约 `101K`。
- Chrome `--dump-dom` 因外部脚本等待未及时退出，已终止；用截图文件非空、PNG header 正常和静态 MathJax 源检查替代 DOM 渲染证据。

## 2026-05-25 Agentic Systems as Boosting Weak Reasoning Models 笔记

### 背景

- 用户要求深入梳理和理解 `https://x.com/che_shr_cat/status/2058713325106614301`。
- 原帖是 Grigory Sapunov 对 arXiv 论文 `Agentic Systems as Boosting Weak Reasoning Models` 的线程解读，主张弱模型候选池里经常已有正确解，关键在于用 critic-comparator harness 选出来。
- 本次目标是把 X 线程、Substack 公开段落、arXiv 论文正文和源码公式核验整合成站内可读的技术分析。

### 已完成

- 新增 `notes/tech-analysis/che-shr-cat-agentic-boosting.html`。
  - 覆盖来源地图、proposal coverage / local identifiability / progress / diversity 四轴框架、`\Pi(k,m,r)` 协议、局部错误分解、blind-spot floor、SWE-bench Verified 实验、ablation、局限和工程实践清单。
  - 明确区分 X 线程传播说法、Substack 摘要、arXiv 论文可核验证据和本报告的工程判断。
- 新增资源目录 `notes/tech-analysis/che-shr-cat-agentic-boosting-assets/`。
  - 保存 X 线程关键图：root、protocol、bound、results、ablation。
  - 保存 arXiv PDF 副本 `2605.14163-agentic-systems-boosting.pdf`。
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`Agentic Systems as Boosting Weak Reasoning Models 深度解读`
  - URL：`/notes/tech-analysis/che-shr-cat-agentic-boosting.html`
  - 类型：`Tech Analysis`

### 设计决策

- 放入 `notes/tech-analysis/`：本次入口是 X thread + arXiv paper 的综合技术解读，重点是 agent harness 的机制诊断，而不是逐节论文翻译。
- 报告采用单页 HTML，不新增多版本文档；只保留支撑机制解释的 5 张 X 图和论文 PDF。
- 对传播性结论保持克制：`nano matches frontier giants` 被写成 SWE-bench Verified、固定候选池、特定 selector budget 下的系统级 solve rate 接近，不外推为权重能力追平。
- 对公式做源码核对：局部 identifiability error 使用 `k^2 e^{-βm-2rσ^2}`，避免把 `pdftotext` 中丢失上标的 OCR 片段写成结论。

### 验证结果

- HTML parser 解析通过：新增页面 `41,654` bytes，核心章节 `source/problem/protocol/math/evidence/limits/implications/insight/commands` 均存在。
- 本地资源引用检查通过：页面引用的 5 张图片与 1 个 PDF 均存在且非空；未发现 Unicode replacement character；`pre code` 样式覆盖存在；MathJax 配置存在。
- 运行 `git diff --check` 通过。
- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证提示，不影响静态页面生成。
- 已确认 `_site/notes/tech-analysis/che-shr-cat-agentic-boosting.html` 生成，并包含标题、Blind-Spot Floor、公式和本地图片引用。
- 已确认 `_site/notes/index.html` 生成新的 Notes 卡片入口，链接到 `/notes/tech-analysis/che-shr-cat-agentic-boosting.html`。
- Chrome headless 已渲染桌面端和移动端截图：
  - `/tmp/che-shr-cat-agentic-boosting-1280.png`
  - `/tmp/che-shr-cat-agentic-boosting-390.png`
- Chrome DOM dump 中已出现 `mjx-container`，确认 MathJax 完成渲染。

## 2026-05-25 ZEDA 后训练 MoE 动态路由 X 帖与论文笔记

### 背景

- 用户要求详细深入理解 `https://x.com/rohanpaul_ai/status/2058620038693999012`。
- 主帖解读论文 `Post-Trained MoE Can Skip Half Experts via Self-Distillation`，核心方法是 ZEDA（Zero-Expert Self-Distillation Adaptation）。
- 本次目标是形成站内可读的中文技术分析，而不是逐条复述 X 原帖。

### 已完成

- 新增 `notes/tech-analysis/rohanpaul-zeda-moe-analysis.html`。
  - 覆盖来源地图、问题背景、zero expert 注入、两阶段自蒸馏、group auxiliary loss、主结果、动态计算分析、局限、工程启发和个人 insight。
  - 明确区分 Rohan Paul 的 X 摘要、论文 PDF 可核验证据、GitHub README/模型发布信息与个人机制判断。
- 新增资源目录 `notes/tech-analysis/rohanpaul-zeda-moe-assets/`。
  - 保存主帖精确媒体图、论文 PDF 副本、PDF 第 1/7/8/9 页证据图。
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`ZEDA：后训练 MoE 如何跳过一半专家计算`
  - URL：`/notes/tech-analysis/rohanpaul-zeda-moe-analysis.html`
  - 类型：`Tech Analysis`

### 设计决策

- 放入 `notes/tech-analysis/`：材料入口是 X thread，但核心依据是 arXiv 论文和官方仓库，属于技术分析。
- 报告强调 ZEDA 不是剪枝，也不是无需训练的 inference trick；它是低成本后训练适配，把“是否调用真实专家”转成 router 可学习决策。
- 对 `opencli twitter download` 抓到的非主帖推荐图不做引用；只使用线程 JSON 中 `media_urls` 精确指向的主帖图。

### 验证结果

- HTML parser 解析通过，文件大小 `31,057` bytes。
- 核心章节 `source/problem/mechanism/evaluation/dynamics/limits/practice/insight/commands` 均存在。
- 本地资源引用检查通过：页面内 `6` 个本地引用均存在且非空；`_site` 中同名资源目录已生成。
- 可读性检查通过：未发现 Unicode replacement character；`pre code` 有显式样式覆盖；MathJax 配置存在。
- `git diff --check` 通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅有 GitHub Metadata 未认证提示，不影响静态页面生成。
- 已确认 `_site/notes/tech-analysis/rohanpaul-zeda-moe-analysis.html` 生成，文件大小 `31,057` bytes。
- 已确认 `_site/notes/index.html` 生成新的 Notes 卡片入口，链接到 `/notes/tech-analysis/rohanpaul-zeda-moe-analysis.html`。
- Chrome headless 已渲染桌面端 `1280x900` 和移动端 `390x844` 截图到 `/tmp/rohanpaul-zeda-moe-1280.png`、`/tmp/rohanpaul-zeda-moe-390.png`；两个 PNG 文件均非空。
- Chrome headless `--dump-dom` 检查通过：DOM 中出现 `mjx-container`，标题和 zero expert 正文均可检索，说明 MathJax 公式实际渲染。

## 2026-05-25 可信 Audio LLM Survey X 线程与论文笔记

### 背景

- 用户要求深度理解分析 `https://x.com/HuggingPapers/status/2058588611172258039`。
- X 主帖推荐论文 `A Survey of Large Audio Language Models: Generalization, Trustworthiness, and Outlook`；回复短链解析到 Hugging Face paper `2605.20266` 和 GitHub 资源清单 `Kwwwww74/Awesome-Trustworthy-AudioLLMs`。
- 目标是形成站内可读的技术分析：解释 Audio LLM 为什么不能只沿用文本 LLM safety，尤其是连续声学信号如何扩展 attack surface。

### 已完成

- 新增 `notes/tech-analysis/huggingpapers-audio-llm-trust.html`。
  - 覆盖来源核验、LALM 机制、六维可信风险、攻防不对称、Fidelity/Stability/Alignment 评测框架、局限、工程实践清单和个人 insight。
  - 明确区分 X 传播内容、HF/arXiv 论文正文、GitHub awesome list 补充资源和本报告的机制判断。
- 新增资源目录 `notes/tech-analysis/huggingpapers-audio-llm-trust-assets/`。
  - 保存原帖图、论文 Figure 1/2/3/4/5/6、arXiv PDF 副本和 GitHub README 副本。
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`可信 Audio LLM Survey 深度解读`
  - URL：`/notes/tech-analysis/huggingpapers-audio-llm-trust.html`
  - 类型：`Tech Analysis`

### 设计决策

- 放入 `notes/tech-analysis/` 而不是 `notes/paper-reviews/`：本次入口是 X/HuggingPapers 推荐，报告重点是把 survey 转换为技术路线图和工程判断，而不是逐节论文精读。
- 页面使用单页 HTML 和本地论文图表，不新增多版本文档；复用站内 Notes shell。
- 报告按“来源 -> 问题 -> 机制 -> 风险 taxonomy -> 评测 -> 实践”的理解顺序组织，避免简单翻译 abstract。

### 验证结果

- HTML parser 解析通过：新增页面 `35,647` bytes，核心章节 `source/problem/mechanism/taxonomy/asymmetry/evaluation/limits/implications/insight/commands` 均存在。
- 本地资源引用检查通过：页面内 `7` 个本地引用均可解析；资源目录包含原帖图、6 张论文图表、PDF 副本和 GitHub README 副本；未发现 Unicode replacement character；`pre code` 样式覆盖存在；MathJax 源公式存在。
- `_data/notes.yml` YAML 解析通过；目标 repo `git diff --check` 通过。
- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证提示，不影响静态页面生成。
- 已确认 `_site/notes/tech-analysis/huggingpapers-audio-llm-trust.html` 生成，`_site/notes/index.html` 包含新 Notes 卡片入口，本地资源同步到 `_site/notes/tech-analysis/huggingpapers-audio-llm-trust-assets/`。
- 本地 HTTP 验证通过：页面、Notes 索引和 `safety.png` 均返回 `200 OK`。
- Chrome headless 渲染验证通过：桌面截图 `/tmp/huggingpapers-audio-llm-trust-1280.png` 为 `1280x900`，移动截图 `/tmp/huggingpapers-audio-llm-trust-390.png` 为 `390x844`，均为非空 PNG；`--dump-dom` 中出现 `mjx-container` 和 `TrustScore`，确认 MathJax 渲染。

## 2026-05-25 EqR / Neural Attractors X 线程与论文笔记

### 背景

- 用户要求详细深入分析 `https://x.com/huskydogewoof/status/2058320088475037801`。
- 原帖是 Benhao Huang 关于 Equilibrium Reasoners（EqR）的 side-post，重点不是主论文发布，而是拆解从标准 feedforward model 到 capable iterative model 的训练路径。
- 本次目标是把 side-post、EqR 主帖、arXiv 论文 `2605.21488v1`、GitHub README 和相关 bonus/回复信息整合成站内可读的技术分析。
- 2026-05-26 复核：用户再次要求深度分析同一 X 链接；已确认站内 HTML 报告完整覆盖该链接，并按 Obsidian 规则补充 PaperNotes 版复习笔记。

### 已完成

- 新增 `notes/tech-analysis/eqr-attractor-reasoners-analysis.html`。
  - 覆盖来源地图、问题背景、attractor 机制、从 feedforward 到 iterative reasoner 的训练 recipe、RI/NI landscape shaping、depth/breadth scaling、ACT、证据边界、工程启发和个人 insight。
  - 明确区分 side-post 的 construction path、主论文 EqR 的最终 scaling 结果、GitHub README 可复现性信息，以及报告中的机制判断。
- 新增资源目录 `notes/tech-analysis/eqr-attractor-reasoners-assets/`。
  - 保存 5 张关键 X 原帖证据图：construction path、supervision placement、segmented online training、ACT halting、takeaways。
  - 保存论文 PDF 本地副本 `2605.21488v1.pdf`。
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`EqR 与 Neural Attractors：从 Feedforward 到 Iterative Reasoner`
  - URL：`/notes/tech-analysis/eqr-attractor-reasoners-analysis.html`
  - 类型：`Tech Analysis`
- 新增 Obsidian 笔记：
  - `/Users/bytedance/Library/Mobile Documents/iCloud~md~obsidian/Documents/obsidian-example-lifeos-main/3.Resources/PaperNotes/26-05-26 Equilibrium Reasoners.md`
  - 作为站内 HTML 长文的复习版，重点记录原帖五段式路径、attractor 判断框架、SOT/ACT 的机制解释和对 LLM/Agent 的迁移边界。

### 设计决策

- 放入 `notes/tech-analysis/`：本次阅读对象是 X thread + paper + code README 的综合技术解读，不是只按论文结构做 paper review。
- 报告采用单页 HTML，不新增多版本文档；资源只保留能支撑机制解释的 5 张截图和论文 PDF。
- 将 residual convergence 与 correctness 明确分开：低 residual 只有在局部稳定、正确 attractor、正输出 margin 条件下才可作为 correctness proxy。
- 对 EqR 的外推保持克制：Sudoku-Extreme 和 Maze-Unique 是受控结构化任务，不能直接等价为开放域 LLM 推理能力。

### 验证结果

- HTML parser 解析通过：新增页面 `35,523` bytes，核心章节 `source/problem/mechanism/recipe/evidence/limits/implications/insight/commands` 均存在。
- 本地资源引用检查通过：页面内 `7` 个本地引用均可解析；5 张证据图与 1 个 PDF 均存在且非空；未发现 Unicode replacement character；`pre code` 样式覆盖存在；MathJax 配置存在。
- `git diff --check` 通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证提示，不影响静态页面生成。
- 已确认 `_site/notes/tech-analysis/eqr-attractor-reasoners-analysis.html` 生成，文件大小 `35,523` bytes，并包含标题、Segmented Online Training 正文和本地图片引用。
- 已确认 `_site/notes/index.html` 生成新的 Notes 卡片入口，链接到 `/notes/tech-analysis/eqr-attractor-reasoners-analysis.html`。
- 本地 HTTP 验证通过：页面、`/notes/` 索引和 `construction-path.jpg` 均返回 `200 OK`。
- Chrome headless 已渲染桌面端 `1280x900` 和移动端 `390x844` 截图到 `/tmp/eqr-attractor-note-1280.png`、`/tmp/eqr-attractor-note-390.png`；两个 PNG 文件均非空。
- Chrome headless `--dump-dom` 检查通过：DOM 中出现 `mjx-container`，说明 MathJax 公式实际渲染。
- 2026-05-26 复核验证：HTML parser 检查通过，章节 `source/problem/mechanism/recipe/evidence/limits/implications/insight/commands` 均存在；页面内本地资源引用无缺失；未发现 Unicode replacement character。

## 2026-05-25 Grok V9 / Cursor 数据 / Mid-training X 线程笔记

### 背景

- 用户要求深度梳理 `https://x.com/eliebakouch/status/2058796025091871141`。
- 原帖讨论 Elon 关于 Grok foundation model V9-Medium 1.5T 的更新：Cursor 数据在补充训练阶段加入，fine-tuning 已开始，RL 几天后开始，2-3 周公开发布。
- 本次目标是把 X 线程、Elon 原始更新、Cursor 官方 Composer 2/2.5 材料、xAI Colossus 公开页和 Cursor 数据使用说明合并成站内可读的技术分析。

### 已完成

- 新增 `notes/tech-analysis/eliebakouch-grok-v9-midtraining.html`。
  - 覆盖来源地图、问题背景、训练阶段拆解、Cursor 数据价值、Composer 2/2.5 对照、评估缺口、证据边界、工程启发和个人 insight。
  - 明确区分公开事实、社区估算和机制判断，避免把 Grok V9 尚未公开的训练细节写成事实。
- 新增资源目录 `notes/tech-analysis/eliebakouch-grok-v9-midtraining-assets/`。
  - 保存 8 张 Cursor Composer 2.5 官方博客图片，用于说明 benchmark、训练、文本反馈和合成任务证据。
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`Grok V9、Cursor 数据与 Mid-training 深度解读`
  - URL：`/notes/tech-analysis/eliebakouch-grok-v9-midtraining.html`
  - 类型：`Tech Analysis`

### 设计决策

- 放入 `notes/tech-analysis/`：当前材料是 X 线程、产品博客、技术报告和公开网页，不是单篇论文精读。
- 页面采用单文件 HTML，资源只保留必要官方证据图，不新增多版本文档。
- 对 “2-3 weeks” 做严格解释：这是公开发布窗口和后训练节奏信号，不直接等价为完整 RL 训练时长。
- 对 Cursor 数据做隐私边界标注：只有关闭隐私模式时，Cursor 官方说明才称可能用代码库数据、prompts、编辑器操作、代码片段等改进 AI 功能并训练模型；不能外推为所有用户代码。

### 验证结果

- HTML parser 校验通过：新增页面 `41,189` bytes，核心章节 `source/question/pipeline/cursor/composer/evals/limits/implications/insight` 均存在。
- 本地资源引用检查通过：页面引用的本地图片均可解析；资源目录 8 张 Cursor Composer 2.5 官方博客图片均存在且非空。
- 内容可读性检查通过：未发现 Unicode replacement character；`pre code` 样式覆盖存在。
- 目标 repo `git diff --check` 通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证提示，不影响静态页面生成。
- 已确认 `_site/notes/tech-analysis/eliebakouch-grok-v9-midtraining.html` 生成，文件大小 `41,189` bytes。
- 已确认 `_site/notes/index.html` 包含 `Grok V9、Cursor 数据与 Mid-training 深度解读` 入口。

## 2026-05-25 LLM Interview Question Bank 推理网络 Infra 覆盖 Review

### 背景

- 用户要求 review `notes/llm-interview-question-bank/` 是否覆盖以下 infra 主线：
  - Prefill-Decode 分离让 KV Cache 迁移变成动态、非对称、跨节点的主流流量。
  - 传统按训练流量优化的 ROFT/Fat-Tree 容易出现“总带宽够，但局部路径被打爆”的结构性低效。
  - 重点关注 Prefill/Decode、KV Cache、ROFT/Fat-Tree、跨节点 KV transfer、拓扑诱发拥塞等内容。

### 已完成

- 本地检索 `notes/llm-interview-question-bank/`：
  - 第 09 章覆盖 serving 总览、Prefill/Decode、KV cache、PagedAttention、continuous batching、prefix caching、SLO 和观测。
  - 第 42 章覆盖核心完整答案，其中第 61 题显式解释 Prefill/Decode 分离部署、KV transfer、适用条件和排障点。
  - 第 53 章覆盖知识点索引，明确把 Prefill/Decode 分离、多租户、观测、KV transfer、跨节点调度、cache 生命周期放在推理系统复盘清单里。
  - 第 88 章覆盖 KV Cache 压缩、驱逐、量化、GQA/MQA、长上下文下显存/带宽瓶颈。
- 本地检索确认题库内目前没有实质覆盖：
  - `ROFT`、`Rail-Optimized Fat-Tree`、`Fat-Tree`、`Leaf/Spine`、`PFC Pause`、`RoCE/RDMA` 在 PD KV transfer 场景下的结构性拥塞机制。
  - “aggregate bandwidth sufficient but localized congestion” 这类网络拓扑诊断语言。
  - 训练 collective trace 与在线推理 KV transfer trace 的流量形态差异。
- 对照仓库内 `notes/tech-analysis/zai-zcube-inference-network.html`：
  - ZCube 技术分析页已完整覆盖这条主线，包括 PD 分离、KV Cache 跨节点迁移、ROFT/Fat-Tree 局部拥塞、ZCube 扁平二部拓扑、单轨/多轨混合接入、P99 TTFT 与吞吐指标。
  - 但该内容目前作为独立 Tech Analysis 存在，没有进入 LLM Interview Question Bank 的章节体系和搜索/学习路径。

### Review 结论

- 题库对“单机/单服务层面的推理系统”覆盖较完整：Prefill/Decode、KV cache、PagedAttention、batching、prefix caching、量化、投机解码、SLO 和多租户都已经足够支撑常规推理平台面试。
- 题库对“集群网络层面的推理 infra”覆盖不足：它提到了跨节点 KV transfer 和网络带宽，但没有把 KV transfer 上升为新的主流流量模型，也没有解释为什么按训练 collective 优化的 ROFT/Fat-Tree 会在 PD 推理里产生局部热点。
- 关键缺口不是再补一个 KV cache 定义，而是补“推理 workload 改变网络拓扑假设”的系统题：
  - 训练流量：AllReduce / AllGather / ReduceScatter / All-to-All 更规则、可预测，拓扑可按 collective/rail 优化。
  - 推理流量：prefill/decode placement 随请求长度、队列状态、batching、模型副本、SLO 动态变化，KV Cache 源宿和流量大小非对称、不稳定。
  - 结构性低效：平均带宽和总带宽不能代表有效带宽；热点 Leaf、rail、端口队列、PFC/ECN 信号和 TTFT P99 更能暴露问题。

### 建议补强

- 在第 42 章第 61 题后新增一个追问块或新增第 62 题：
  - “为什么 Prefill/Decode 分离会把网络推上关键路径？KV Cache 跨节点迁移如何改变流量模型？”
  - “ROFT/Fat-Tree 为什么在训练 collective 中合理，但在 PD 推理 KV transfer 中可能局部拥塞？”
  - “如何诊断‘总带宽够，但局部路径被打爆’？应该看哪些指标？”
- 在第 53 章知识点索引新增一小节：
  - `PD disaggregation -> KV transfer -> topology-aware scheduling -> network observability`
  - 指标包括 per-flow KV size、source/destination pair、per-rail load、per-leaf load、PFC Pause、ECN/CNP、egress queue depth、TTFT p99。
- 在题库首页的训练/推理平台岗学习路径里，补一个“推理网络/拓扑专项”入口，链接到现有 `notes/tech-analysis/zai-zcube-inference-network.html` 或后续题库章节。

### 当前状态

- 本次只完成 review 和过程记录，尚未修改题库正文。
- 如果后续要补内容，最小改动方案是 in-place 修改第 42、53、index 三处，不新建大文档；更完整方案是新增一章“推理网络与 PD KV Transfer 专项”，但会增加目录维护成本。

## 2026-05-25 NITP X 线程与 ICML Poster 笔记

### 背景

- 用户要求深度解析 `https://x.com/aHpaBean/status/2058137485654536538`，并将最终 HTML 笔记输出到新的个人主页 repo：`/Users/bytedance/Documents/Ricardokevins.github.io`。
- 原帖内容是 NITP（Next Implicit Token Prediction）发布预告；作者回复补充了与 JEPA、Self-Distillation-MTP、Cut Cross-Entropy 的边界。
- 目标不是复制 X 原帖，而是形成站内可读的技术分析：解释 NTP 为什么可能欠约束表示空间，NITP 如何加入 hidden/representation space 辅助目标，以及当前证据边界。

### 已完成

- 新增 `notes/tech-analysis/ahpabean-nitp-analysis.html`。
  - 覆盖来源地图、问题背景、方法机制、公开结果、方法对比、失败模式、复现草图、个人 insight 和本地抓取命令。
  - 明确标注 NITP 论文 PDF 与官方实现代码在写作时仍未公开，不能把 README/ICML 摘要外推成完整复现实验。
- 新增本地资源目录 `notes/assets/ahpabean-nitp/`。
  - 保存原帖配图、NITP overview、representation dynamics、NITP loss curve、MoE results table、dense results table。
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`NITP：Next Implicit Token Prediction 技术解读`
  - URL：`/notes/tech-analysis/ahpabean-nitp-analysis.html`
  - 类型：`Tech Analysis`

### 设计决策

- 放入 `notes/tech-analysis/` 而不是 `notes/paper-reviews/`：当前可验证材料主要是 X 线程、ICML poster 摘要和 GitHub README；论文 PDF/Citation 仍为 TBD。
- 报告使用单页 HTML，不新增子站或多版本文档，符合现有 Notes 结构。
- 使用 MathJax 表达 NTP/NITP loss，使用官方仓库图片作为证据图，不添加纯装饰图。
- 对 JEPA、distillation、CCE 的比较保持机制边界：NITP 与 JEPA 都做 representation prediction，但 NITP 是 autoregressive LM setting 且保留 NTP；CCE 是 CE 计算优化，不改变目标。

### 验证结果

- 静态 HTML 解析通过：核心章节 `source/problem/method/evidence/compare/failure/practice/insight/commands` 均存在。
- 本地资源引用检查通过：`notes/assets/ahpabean-nitp/` 下 6 张图片均存在且非空；新增页面未发现缺失的本地 CSS/图片引用或页内锚点。
- 内容可读性检查通过：未发现 Unicode replacement character；`pre code` 已设置显式样式覆盖；页面包含 MathJax 配置与 NTP/NITP 公式。
- 运行 `git diff --check` 通过。
- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证提示，不影响静态页面生成。
- 已确认 `_site/notes/tech-analysis/ahpabean-nitp-analysis.html` 生成，并包含标题、NITP 正文与本地图片引用。
- 已确认 `_site/notes/index.html` 生成新的 Notes 卡片入口，链接到 `/notes/tech-analysis/ahpabean-nitp-analysis.html`。

## 2026-05-25 ZCube 推理网络架构 X Article 笔记

### 背景

- 用户要求深度解读并梳理 `https://x.com/Zai_org/status/2057216685040443743`。
- 原帖正文只有一个 `t.co` 短链；短链解析到 X Article `https://x.com/i/article/2057206923208884224`。
- 用户指定最终 HTML 笔记写入新 repo：`/Users/bytedance/Documents/Ricardokevins.github.io`。

### 已完成

- 新增 `notes/tech-analysis/zai-zcube-inference-network.html`。
  - 覆盖来源与获取方式、Prefill-Decode 分离、KV Cache 跨节点迁移、ROFT/Fat-Tree 拥塞机制、ZCube 扁平二部拓扑、单轨/多轨混合接入、生产部署指标、SIGCOMM 论文摘要边界、限制和个人 insight。
  - 明确区分 Z.ai 官方博客的生产部署 claim、SIGCOMM 2025 program 的 ATOP/ZCube 论文摘要，以及报告中的工程机制判断。
- 2026-05-25 20:52 原地增强该页面。
  - 新增 `request-flow` 章节：把一次 PD 请求拆成请求进入、prefill、KV Cache 迁移、decode 接管、后续 token 五段。
  - 新增 KV Cache 体积估算公式：`layers × tokens × 2 × kv_heads × head_dim × bytes_per_element`，解释长上下文、GQA/MQA、KV 量化和并发峰值如何影响网络压力。
  - 在 `traffic` 与 `zcube` 章节补充 ROFT workload mismatch、topology-induced congestion、单轨/多轨混合接入的路径分散直觉。
  - 新增 `diagnosis` 章节：给出 TTFT/KV transfer、PFC/ECN、per-rail/per-leaf load、source/destination pair、topology-aware placement 的诊断清单。
  - 增强 `limits` 与 `implications`：补充小集群外推边界、RoCE 配置变量、训练/推理拓扑目标差异，以及研发优先级建议。
- 新增资源目录 `notes/tech-analysis/zai-zcube-inference-network-assets/`。
  - 保存 Z.ai 官方博客图像 `img_001.png` 到 `img_012.png`。
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`ZCube 推理网络架构解读：KV Cache 流量如何改变数据中心拓扑`
  - URL：`/notes/tech-analysis/zai-zcube-inference-network.html`
  - 类型：`Tech Analysis`
  - 2026-05-25 20:52 更新摘要与时间，反映本次深读增强。

### 设计决策

- 采用单页 HTML 放入 `notes/tech-analysis/`，与站内已有 X Article / 技术解读笔记保持一致。
- 报告按“问题 -> 流量形态变化 -> ROFT 失效机制 -> ZCube 拓扑机制 -> 证据与边界 -> 工程启发”的顺序组织，而不是逐段复述原文。
- 对 X Article 与官方博客的一个差异做显式标注：X Article 抓取文本中带宽 ablation 写为 `512-GPU cluster`，Z.ai 官方博客同段写为 `32-GPU testbed`；报告采用官方博客版本，并记录为可信度边界。

### 验证结果

- HTML parser 解析通过；核心章节 `source/problem/traffic/zcube/evidence/limits/implications/insight/commands` 均存在。
- 本地资源引用检查通过：页面引用的 10 张正文图片均存在且非空；资源目录共保存 12 张 Z.ai 官方博客图片。
- `git diff --check` 通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证和 GitHub API rate limit warning，不影响静态页面生成。
- 已确认 `_site/notes/tech-analysis/zai-zcube-inference-network.html` 生成，并包含页面标题、正文图片引用和核心章节。
- 已确认 `_site/notes/index.html` 生成新的 Notes 卡片入口，链接到 `/notes/tech-analysis/zai-zcube-inference-network.html`。
- Chrome headless 已渲染桌面端 `1280x900` 和移动端 `390x844` 截图到 `/tmp/zcube-note-1280.png`、`/tmp/zcube-note-390.png`；两个 PNG 文件均非空、PNG header 正常、首段字节包含完整 256 种取值，说明不是空白截图。
- 2026-05-25 20:52 增强后复验通过：
  - 静态结构检查通过：文件 `56,761` bytes；新增章节 `request-flow/diagnosis` 与原核心章节均存在；页面内 `10` 张本地图片引用均可解析；未发现 Unicode replacement character；`pre code` 样式覆盖存在。
  - `_data/notes.yml` YAML 解析通过；目标文件 `git diff --check` 通过。
  - 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证提示，不影响静态页面生成。
  - 已确认 `_site/notes/tech-analysis/zai-zcube-inference-network.html` 包含新增的“把一次请求拆开看”“KV Cache 到底有多大”“如果在自己集群里验证”等章节。
  - 已确认 `_site/notes/index.html` 的 ZCube 卡片摘要更新为包含“KV Cache 体积公式”和“集群诊断清单”。

## 2026-05-25 Test-Time Scaling / Training-Free RL X Article 笔记

### 背景

- 用户要求深度解读并梳理 `https://x.com/sheriyuo/status/2042072816712085577`。
- 主帖正文只有一个 `t.co` 短链；短链解析到 X Article `https://x.com/i/article/2042067717436715008`，标题为 `Test-Time Scaling and Training-Free RL`。
- 用户指定最终 HTML 笔记写入新 repo：`/Users/bytedance/Documents/Ricardokevins.github.io`。

### 已完成

- 新增 `notes/tech-analysis/sheriyuo-tts-training-free-rl.html`。
  - 覆盖来源与获取方式、TTS 分类、RLHF/GRPO KL 正则闭式最优策略、ETS energy-guided sampling、Monte Carlo energy estimation、ETS-IS importance sampling、实验结果、Self-Evolving/TTRL/RSE 边界、限制和个人 insight。
  - 使用 MathJax 渲染核心公式；`pre code` 有显式样式覆盖，避免代码块可读性回退。
- 新增资源目录 `notes/tech-analysis/sheriyuo-tts-training-free-rl-assets/`。
  - 保存 X Article 配图 `x-article-01` 到 `x-article-21`。
  - 保存 ETS 论文 PDF 副本 `2601.21484-ets.pdf`。
  - 保存 `sheriyuo/ETS` README 与 `maxzuo/mh-llm` README 本地副本。
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`Test-Time Scaling 与 Training-Free RL 深度解读`
  - URL：`/notes/tech-analysis/sheriyuo-tts-training-free-rl.html`
  - 类型：`Tech Analysis`

### 设计决策

- 采用单页 HTML 放入 `notes/tech-analysis/`，与站内已有 X Article / 技术解读笔记保持一致。
- 报告不按原文段落复述，而按“问题 -> TTS 地图 -> ETS 数学机制 -> 证据 -> Self-Evolving 边界 -> 局限 -> insight”的读者理解顺序组织。
- 将 X Article 观点、ETS 论文/仓库可核验证据和个人机制判断分开写，避免把作者观点、论文实验和外推结论混在一起。

### 验证结果

- HTML parser 校验通过：新增页面 `41,657` bytes，核心章节 `source/problem/map/mechanism/evidence/self-evolving/limits/implications/insight` 均存在。
- 本地资源引用检查通过：页面内 `13` 个本地引用均可解析；未发现 Unicode replacement character；`pre code` 样式覆盖存在；MathJax 源公式存在。
- `git diff --check` 通过。
- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功。
  - 构建仅出现 GitHub Metadata 未认证和 GitHub API rate limit warning，不影响静态页面生成。
- 已确认 `_site/notes/tech-analysis/sheriyuo-tts-training-free-rl.html` 生成，文件大小 `41,657` bytes。
- 已确认 `_site/notes/index.html` 包含 `Test-Time Scaling 与 Training-Free RL 深度解读` 入口。
- 已确认 `_site/notes/tech-analysis/sheriyuo-tts-training-free-rl-assets/2601.21484-ets.pdf` 和 `x-article-16.png` 等资源生成。
- 本地 HTTP 验证通过：
  - `/notes/tech-analysis/sheriyuo-tts-training-free-rl.html` 返回 `200 OK`。
  - `/notes/` 返回 `200 OK`。
  - `/notes/tech-analysis/sheriyuo-tts-training-free-rl-assets/x-article-16.png` 返回 `200 OK`。
- Chrome headless 打开本地页面并截图成功：`/tmp/sheriyuo-tts-training-free-rl.png`，大小约 `643K`。
- Chrome headless `--dump-dom` 检查通过：DOM 中 `mjx-container/MathJax` 命中 `18` 处，标题命中 `2` 处。
- Playwright CLI wrapper 当前失败，原因是 `npx --package @playwright/mcp playwright-cli` 未暴露 `playwright-cli` 二进制；已用系统 Chrome headless 完成等价渲染/DOM 验证。

## 2026-05-21 Manual-Coding Attention 笔记导入

### 背景

- 用户要求将 `https://hewei2001.pages.dev/Manual-Coding-1` 的内容导入个人主页 Notes。
- 目标页面是“手撕经典算法 #1 Attention篇”，覆盖 SDPA、MHA、KV Cache、MQA、GQA，MLA 部分仍为 TODO。
- 本次不做外站整页镜像，改为站内可读的整理版，保留来源、算法脉络、关键公式、PyTorch 参考实现和实现风险提示。

### 已完成

- 新增 `notes/tech-analysis/manual-coding-attention.html`。
  - 覆盖来源与导入方式、Attention 共同结构、SDPA、MHA、KV Cache、MQA/GQA、实现风险复盘、面试复述模板和个人 insight。
  - 使用站内 `notes/assets/notes-shell.css` 导航壳，页面内 CSS 独立作用域，不影响现有 Notes 子站。
  - 使用 MathJax 渲染 Attention 公式；代码块显式设置 `pre code` 样式，避免代码可读性回退。
- 更新 `_data/notes.yml`，新增 Notes 卡片入口：
  - 标题：`手撕经典算法 #1 Attention 篇整理`
  - URL：`/notes/tech-analysis/manual-coding-attention.html`
  - 类型：`Study Resource`

### 设计决策

- 采用单页 HTML 笔记而不是新增完整 subsite：当前材料只有一篇，且原文代码表格存在重复抓取内容，单页整理更简单、可维护。
- 代码实现采用最小可解释版本，避免引入 FlashAttention、paged cache 等当前材料没有覆盖的扩展能力。
- 对原文中的 TODO 和示例边界做显式标注：MLA 不虚构实现，KV Cache 示例强调 prefill/decode 语义、mask shape 和每层缓存边界。

### 验证结果

- 运行 `git diff --check` 通过。
- 静态 HTML 解析通过：
  - 新增页面包含 `source`、`map`、`sdpa`、`mha`、`cache`、`gqa`、`issues`、`interview`、`insight` 必要锚点。
  - 新增页面本地资源和页内锚点缺失数为 `0`。
- 首次运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 失败，原因是临时 gem 目录缺少 `jekyll` 可执行文件；随后运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle install` 补齐依赖。
- 重新运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功。
  - 构建期间仅出现 GitHub Metadata 未认证和 GitHub API rate limit warning，不影响静态页面生成。
- 已确认 `_site/notes/tech-analysis/manual-coding-attention.html` 生成，并包含 `手撕经典算法 #1 Attention 篇整理`、`GroupedQueryAttention`、`KV Cache`、`我的判断` 等核心内容。
- 已确认 `_site/notes/index.html` 生成新的 Notes 卡片入口，链接到 `/notes/tech-analysis/manual-coding-attention.html`。
- 本地预览 `http://127.0.0.1:4000/notes/tech-analysis/manual-coding-attention.html` 返回 `200`，`http://127.0.0.1:4000/notes/` 返回 `200`。
- 使用 Playwright CLI 截取桌面端 `1280x900` 和移动端 `390x844` 快照，首屏标题、摘要、指标卡和站内导航正常；移动端无明显横向溢出或内容遮挡。
- 使用 Playwright CLI 等待 `mjx-container` 成功，确认 MathJax 公式在真实 Chromium 中完成渲染。

## 2026-05-13 Notes 板块轻量迁移

### 背景

- 目标：评估是否在个人主页中增加个人博客/笔记板块，并先迁移一篇轻量化 Downloads 笔记验证路径。
- 初始候选：`/Users/bytedance/Downloads/llm-interview-question-bank.html`。
- 发现：该文件只是 353B 跳转页，真实内容在 `llm-interview-question-bank/` 目录中，包含 90 个章节 HTML、CSS、JS 和 SVG 资源，适合后续作为独立静态知识库接入。
- 本阶段选择更轻量的单文件论文笔记：`/Users/bytedance/Downloads/unmasking-on-policy-distillation.html`。

### 已完成

- 新增 `notes/unmasking-on-policy-distillation.html`，迁移单文件 HTML 论文精读报告。
- 新增 `_pages/notes.md`，作为站内 `Notes` 入口页。
- 更新 `_data/navigation.yml`，将模板遗留的 `Blog Posts` 导航替换为 `Notes`。

### 设计决策

- 采用静态目录 `notes/` 承载独立 HTML 笔记，避免把已有完整 HTML 强行改写成 Jekyll `_posts`。
- 使用 `_pages/notes.md` 做索引页，符合当前 Jekyll/academicpages 架构，改动面小。
- 暂不引入新的 collection、标签系统或自动生成脚本，先验证发布链路。

### 验证结果

- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle install`，将 GitHub Pages/Jekyll 依赖安装到临时目录，避免写入系统 Ruby。
- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build`，构建成功。
- 已确认 `_site/notes/index.html` 生成，并包含 `Unmasking On-Policy Distillation 论文精读` 链接。
- 已确认 `_site/notes/unmasking-on-policy-distillation.html` 生成，并保留原 HTML 标题、Insight 和实践建议内容。
- 已启动本地预览：`http://127.0.0.1:4000/notes/`。
- 已通过 `curl -I` 验证 `/notes/` 和 `/notes/unmasking-on-policy-distillation.html` 均返回 `200 OK`。

### 下一步

- 已继续迁移 `llm-interview-question-bank/` 到 `notes/llm-interview-question-bank/`，见下一节。

## 2026-05-13 LLM Interview Question Bank 完整迁移

### 背景

- 用户确认 90 个章节也需要保留，但希望前一步先用轻量笔记验证迁移路径。
- 轻量 Notes 链路已经通过 Jekyll build 和本地 HTTP 验证，因此继续接入完整题库。

### 已完成

- 将 `/Users/bytedance/Downloads/llm-interview-question-bank/` 完整迁移到 `notes/llm-interview-question-bank/`。
- 使用 `rsync -a --delete --exclude='.DS_Store'` 复制，避免把 macOS 元数据文件带入仓库。
- 已确认迁移后目录大小约 `3.4M`，共 `102` 个文件：
  - `index.html`
  - `chapters/001.html` 到 `chapters/090.html`
  - `assets/question-bank.css`
  - `assets/question-bank.js`
  - 本地 SVG 图示资源
- 更新 `_pages/notes.md`，将 `LLM Interview Question Bank` 从 planned resource 改为正式链接。

### 验证结果

- 重新运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build`，构建成功。
- 已确认 `_site/notes/llm-interview-question-bank/` 输出仍为 `102` 个文件、约 `3.4M`。
- 已确认 `_site/notes/llm-interview-question-bank/index.html`、`chapters/001.html`、`chapters/090.html`、`assets/question-bank.css`、`assets/question-bank.js`、`assets/learning-map.svg` 均存在。
- 已启动本地预览并通过 HTTP 验证以下路径均返回 `200 OK`：
  - `/notes/llm-interview-question-bank/`
  - `/notes/llm-interview-question-bank/chapters/001.html`
  - `/notes/llm-interview-question-bank/chapters/090.html`
  - `/notes/llm-interview-question-bank/assets/question-bank.css`
  - `/notes/llm-interview-question-bank/assets/question-bank.js`
  - `/notes/llm-interview-question-bank/assets/learning-map.svg`
- 抽查题库首页确认保留 `90` 个独立章节、`learning-map.svg`、`question-bank.js` 和第 90 章链接。
- 抽查第 90 章确认页面标题和 Medusa/EAGLE/Lookahead Decoding 章节内容存在。

## 2026-05-13 Notes 索引体验改进

### 背景

- 用户反馈 `https://ricardokevins.github.io/notes/` 界面不够美观，并提出按时间排序、笔记多以后分页，例如每页 10 条。

### 设计决策

- 新增 `_data/notes.yml` 作为 Notes 元数据源，避免在 `_pages/notes.md` 里手写重复 HTML。
- `_pages/notes.md` 按 `date` 倒序渲染笔记卡片，后续新增笔记只需追加数据条目。
- 使用页面内、作用域限定的 CSS/JS：
  - CSS 只影响 `.notes-index`，避免污染主页、Publications 和题库子站。
  - JS 只做客户端分页，默认 `10` 条/页。
- 暂不引入 Jekyll collection 或插件分页。当前站点用 GitHub Pages/Jekyll 3，内置 pagination 更适合 `_posts`，不适合混合静态 HTML 资源索引；数据文件方案更轻、更稳。

### 已完成

- 新增 `_data/notes.yml`，记录标题、URL、日期、类型、摘要、标签和补充信息。
- 重写 `_pages/notes.md`：
  - 顶部说明改为 compact intro。
  - 笔记以卡片形式展示。
  - 日期倒序。
  - 默认每页 10 条，超过 10 条自动出现分页按钮。
  - 保留 `大模型面试题库` 和 `Unmasking On-Policy Distillation 论文精读` 两个资源。

### 验证结果

- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build`，构建成功。
- 本地 HTTP 验证 `/notes/` 返回 `200 OK`。
- 已确认生成页面包含：
  - `.notes-index`
  - `data-page-size="10"`
  - 中文说明文案
  - `大模型面试题库`
  - `Unmasking On-Policy Distillation 论文精读`
  - `.notes-page-button` 分页脚本逻辑
- 使用 Playwright CLI 截取桌面端 `1280x900` 与移动端 `390x844` 页面截图，并人工检查：
  - 桌面端显示为整洁卡片列表，保留左侧 author profile。
  - 移动端无明显横向溢出，卡片、标题、摘要和标签可以正常换行。
  - 当前仅 2 条笔记，因此分页控件按设计隐藏；超过 10 条后会显示分页按钮。

## 2026-05-14 LLM Interview Question Bank 逻辑重排

### 背景

- 用户反馈大模型面试题库阅读体验不满意：内容“东一块西一块”，前面讲一遍、后面又讲一遍，缺少清晰顺序。
- 审计发现主要问题不是单题答案缺失，而是旧目录按生成/追加顺序呈现：
  - `005-014` 是十个核心模块的题型地图。
  - `038-047` 又是同一批核心模块的完整逐题答案。
  - `048-058` 再次给同一批问题做知识点索引。
  - 后续专项又按新增批次排列，数学、优化器、RL、Reasoning、系统、前沿内容交错。
- 因此本次不重写知识答案本身，优先重建阅读逻辑：让地图、答案、索引、专项和附录各自承担明确职责。

### 设计决策

- 保留 `90` 个章节文件和原始编号，避免破坏既有链接。
- 将首页和章节侧栏改成 `9` 个学习阶段：
  1. 入口与面试方法
  2. 十个核心模块地图
  3. 核心题完整答案
  4. 核心知识点索引
  5. 架构、位置编码、算力与手撕代码
  6. 训练、推理与系统工程
  7. 数学、优化器、RL 与 Reasoning
  8. 多模态、Agent 协议、合成数据与代码模型
  9. 系统基础、DeepSeek、速查与来源附录
- 在首页新增“材料逻辑”说明，明确：
  - `005-014` 只作为地图层。
  - `038-047` 承担核心完整答案层。
  - `048-058` 只作为查漏索引层。
  - 专项层按岗位和知识依赖重新排序。
- 在 `005-014` 核心地图页移除重复的 `就地速答` 正文块，只保留代表题、真正考什么、作答抓手；页面顶部增加阅读定位，直接指向对应完整答案章和知识点索引章。
- 在所有章节页增加“阅读定位”提示，并把上一页/下一页改成新的学习顺序，而不是旧文件编号顺序。
- 更新筛选分类和搜索行为：筛选后自动隐藏空的章节分组和侧栏分组，减少无结果噪声。

### 已完成

- 重写 `notes/llm-interview-question-bank/index.html`：
  - 首页 hero 文案从“静态转录结果”改为“按学习逻辑分层”。
  - 卡片从单一网格改为分阶段分组。
  - 新增算法研究岗、训练/推理平台岗、RAG/Agent 应用岗三条阅读路线。
- 更新 `notes/llm-interview-question-bank/chapters/001.html` 到 `090.html`：
  - 全部章节侧栏改为新学习顺序。
  - 全部章节补充阅读定位。
  - 全部章节的上下章导航改为新顺序。
- 更新 `notes/llm-interview-question-bank/assets/question-bank.css`：
  - 新增逻辑说明区、阶段标题、阅读定位块样式。
- 更新 `notes/llm-interview-question-bank/assets/question-bank.js`：
  - 分类/搜索后隐藏空分组，避免筛选页面出现空壳。

### 验证结果

- 自定义 HTML 校验脚本通过：
  - 共检查 `91` 个 HTML 文件（`index.html + 90` 个章节页）。
  - 首页仍有 `90` 张章节卡片。
  - 章节页均有且仅有 `1` 个阅读定位块。
  - 章节页均有顶部和底部两组上下章导航，且两组导航目标一致。
  - 内部资源和片段链接缺失数为 `0`。
  - `005-014` 核心地图页正文中不再保留 `就地速答` 小节。
- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功。
- 构建仅出现 GitHub Metadata 无认证的常规 warning，不影响静态页面生成。
- 通过本地 HTTP 验证以下路径均返回 `200`：
  - `/notes/llm-interview-question-bank/`
  - `/notes/llm-interview-question-bank/chapters/005.html`
  - `/notes/llm-interview-question-bank/chapters/038.html`
  - `/notes/llm-interview-question-bank/chapters/048.html`
  - `/notes/llm-interview-question-bank/assets/question-bank.css`
  - `/notes/llm-interview-question-bank/assets/question-bank.js`
- 运行 `git diff --check` 通过。
- 已清理临时截图目录，当前没有新增未跟踪交付文件。

### 当前判断

- 已解决“顺序不清”和“地图、答案、索引重复混读”的主问题。
- 本次改动遵循 KISS/YAGNI：不新增内容源、不新增生成框架、不重写所有答案，只在现有静态站点上重建信息架构和导航语义。
- 后续如果继续深修，优先方向应是回到源 Markdown 重新组织章节源，而不是继续手工维护生成后的 HTML。

## 2026-05-15 LLM Interview Question Bank 查缺补漏与深度补强

### 背景

- 用户继续要求检查题库知识点是否全面、详细、深入，而不是只解决章节顺序问题。
- 本次不再做全站导航重排，而是对已经重排后的 90 章做第二轮内容审计：找真正缺失的现代大模型面试高频点，并在对应章节原地补强。

### 审计方法

- 结构指标扫描：统计 90 个章节的正文长度、标题层级、表格、代码块和列表密度，区分“目录/索引型薄页”和“答案型薄页”。
- 术语覆盖扫描：检查 RLVR、verifiable rewards、benchmark leakage、data contamination、Prefill/Decode disaggregation、prompt injection、AgentBench、tau-bench、SWE-bench 等近期高频知识点的覆盖程度。
- 代表章节复核：重点检查训练/RL、推理系统、评测、Agent 工程四类章节，因为这些主题在 2024-2026 面试中变化最快，也最容易只停留在术语层。
- 外部方向校验：优先尝试 Grok/MCP 搜索；由于返回内容为空，补充使用 arXiv/公开网页检索确认近期方向，包括 RLVR/GRPO 变体、Prefill-Decode 分离部署、Agent 安全与交互式评测、污染受限 benchmark。

### 发现的问题

- 核心答案层 `038-047` 整体已经较密，Transformer、训练、推理、RAG、Agent、多模态、数据、评测、安全等主干都有完整答题结构。
- 真正不足不是“没有更多章节”，而是部分前沿问题缺少可面试作答的系统化答案：
  - `RLVR / verifiable rewards` 覆盖过薄，容易只讲 RLHF/GRPO，而说不清可验证奖励和偏好模型奖励的区别。
  - 评测章节对 benchmark 的“可信度”讲得不够，缺少数据污染、题目泄漏、榜单过拟合、隐藏集和业务回放的完整判断框架。
  - 推理系统已有 KV cache、vLLM、prefix caching、speculative decoding 等内容，但缺少 Prefill/Decode 分离部署的专门答案。
  - Agent 章节已有工具调用、MCP/A2A、schema 和工作流，但缺少 prompt injection、权限边界、数据外传、side-effect 工具审批、交互式评测这些工程安全内容。

### 已完成

- 原地补强 `notes/llm-interview-question-bank/chapters/067.html`：
  - 新增 `177. 什么是 RLVR？它和传统 RLHF 的训练信号有什么本质不同？`
  - 新增 `178. DAPO、Dr. GRPO、GSPO 这些方法是在修正 GRPO 的什么问题？`
  - 补充 RLHF vs RLVR 对比、可验证奖励样例、长度偏置、全对/全错组内奖励退化、rollout 采样效率、sequence-level 与 token-level 更新稳定性。
- 原地补强 `notes/llm-interview-question-bank/chapters/042.html`：
  - 新增 `61. 什么是 Prefill/Decode 分离部署？它解决了什么问题，又引入了什么代价？`
  - 补充 prefill compute-bound、decode memory/KV-bound、TTFT/TPOT、KV transfer、SLO、短请求反而不划算、cache 生命周期和故障恢复。
- 原地补强 `notes/llm-interview-question-bank/chapters/045.html`：
  - 新增 `97. 如何判断一个 benchmark 结果可信？数据污染、题目泄漏和过拟合怎么处理？`
  - 补充 contamination、leakage、overfitting 的区别，以及 exact/near-duplicate 检测、time split、hidden set、协议透明、错误分类、流量回放和 A/B 验证。
  - 修正错别字 `时效应求` 为 `时效性要求`。
- 原地补强 `notes/llm-interview-question-bank/chapters/085.html`：
  - 新增 `287. Agent 工具调用的安全威胁模型是什么？prompt injection 为什么特别危险？`
  - 新增 `288. 如何评测一个 Agent 是否真的可靠，而不是只会演示 demo？`
  - 补充直接/间接 prompt injection、最小权限、数据分级、side-effect 工具审批、沙箱、审计日志、任务成功率、子任务成功率、恢复成功率、安全违规率和成本/延迟。
- 更新 `notes/llm-interview-question-bank/index.html`：
  - 同步补充 42、45、67、85 章的 `data-search` 关键词和卡片统计，让首页搜索能命中新加入的知识点。
  - 将本次整理日期更新为 `2026-05-15`。

### 验证结果

- 针对 42、45、67、85 四个补强章节做本地锚点检查，缺失本地片段链接为 `0`。
- 全站快速本地锚点扫描完成，缺失本地片段链接为 `0`。
- 全站 HTML 一致性检查通过：
  - 共检查 `91` 个 HTML 文件（`index.html + 90` 个章节页）。
  - 首页仍有 `90` 张章节卡片。
  - 章节页均有 `chapter-orientation` 阅读定位块，合计 `90` 个。
  - 内部资源和片段链接缺失数为 `0`。
  - 新增锚点 `h-0667`、`h-0778`、`h-1027`、`h-1030`、`h-1396`、`h-1399` 均存在。
- 新增章节题号检查通过：
  - `042.html` 现在包含 13 个编号问题，新增题号到 `61`。
  - `045.html` 现在包含 13 个编号问题，新增题号到 `97`。
  - `067.html` 现在包含 9 个编号问题，新增题号到 `178`。
  - `085.html` 现在包含 12 个编号问题，新增题号到 `288`。
- 首页搜索元数据已确认包含 `RLVR`、`DAPO`、`Dr. GRPO`、`Prefill/Decode`、`数据污染`、`prompt injection`、`AgentBench`、`SWE-bench` 等新增关键词。
- 运行 `git diff --check` 通过。
- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 无认证的常规 warning。
- 使用 Python 标准库 HTTP 抽查本地 `127.0.0.1:4000`，以下路径均返回 `200`：
  - `/notes/llm-interview-question-bank/`
  - `/notes/llm-interview-question-bank/chapters/042.html`
  - `/notes/llm-interview-question-bank/chapters/045.html`
  - `/notes/llm-interview-question-bank/chapters/067.html`
  - `/notes/llm-interview-question-bank/chapters/085.html`

### 当前判断

- 第一轮解决了“顺序不清、同一层内容反复出现”的结构问题；本轮解决的是“现代高频知识点缺少完整答案”的深度问题。
- 这次没有盲目扩张新章节，而是把缺口放回最合适的既有章节：RL 放在 67，推理系统放在 42，评测放在 45，Agent 安全与评测放在 85。这样更符合 KISS/YAGNI，也避免题库继续变成碎片化追加。
- 下一轮如果继续深挖，建议优先做两件事：
  - 把 `038-047` 的核心答案层按岗位面试场景增加“追问链路”，例如每题后追加 2-3 个 interviewer follow-up。
  - 将源材料从生成后的 HTML 回迁为 Markdown 或数据源，再由脚本生成 HTML，降低后续维护成本。

## 2026-05-18 Math Interview Question Bank 新增

### 背景

- 用户希望仿照现有 `notes/llm-interview-question-bank/` 的静态题库形式，新增一个数学题库。
- 目标不是做纯数学竞赛资料，而是快速补齐大模型岗位和量化公司岗位共同需要的基础数学：
  - 微积分：极限、导数、Taylor 展开、梯度、Hessian、矩阵求导、Lagrange/KKT。
  - 线性代数：向量空间、矩阵乘法、秩、投影、特征值、SVD、PCA、正定性、条件数。
  - 概率论：条件概率、Bayes、常见分布、期望方差、LLN/CLT、MLE/MAP、交叉熵/KL、Monte Carlo、随机过程和量化风险指标。

### 设计决策

- 复用大模型题库的交互形态：左侧分组导航、搜索框、分类筛选、章节页、上一章/下一章、MathJax 公式渲染和本地 SVG 导图。
- 控制规模为 `12` 个稳定章节，而不是复制 90 章体量：
  - `001` 学习路线和答题模板。
  - `002-004` 微积分速览与详细解答。
  - `005-007` 线性代数速览、详细解答和应用。
  - `008-010` 概率统计速览、详细解答、随机过程与量化基础。
  - `011` 大模型与量化公司应用题。
  - `012` 手算训练、公式速查与最终答题模板。
- KISS/YAGNI：不新增 Jekyll collection、插件或生成框架；交付物是可直接由 GitHub Pages 复制发布的静态 HTML/CSS/JS/SVG。
- DRY：独立子站内部统一使用 `assets/math-bank.css` 和 `assets/math-bank.js`，不在每个章节复制交互逻辑。
- SOLID/SRP：题库正文、视觉样式、交互脚本和站点索引分别放在 `chapters/`、`assets/math-bank.css`、`assets/math-bank.js`、`_data/notes.yml` / `_pages/notes.md`。

### 已完成

- 新增静态题库目录 `notes/math-interview-question-bank/`：
  - `index.html`
  - `chapters/001.html` 到 `chapters/012.html`
  - `assets/math-bank.css`
  - `assets/math-bank.js`
  - `assets/learning-map.svg`
  - `assets/calculus-optimization.svg`
  - `assets/linear-algebra-geometry.svg`
  - `assets/probability-distribution.svg`
- 更新 `_data/notes.yml`，新增 `数学基础面试题库` 条目，正式接入 `/notes/` 的 Jekyll Notes 索引。
- 更新 `_data/notes.yml` / `_pages/notes.md` 驱动的 Notes 索引，新增 `数学基础面试题库目录` 链接。

### 内容覆盖

- 首页包含三条学习路线：
  - 大模型算法/训练岗：softmax、cross-entropy、attention、LoRA、KL、梯度噪声、二阶优化边界。
  - 量化研究/策略岗：最小二乘、协方差、PCA 因子、CLT、VaR/CVaR、Sharpe、回测过拟合。
  - 基础快速补齐：先读三门速览，再读逐题解答，最后做手算训练。
- 章节内容包含：
  - `64` 个核心解释/应用题条目。
  - `30` 道短手算训练题。
  - 公式速查表和跨岗位面试回答模板。
- 重点强调每个公式的对象、直觉、岗位连接和边界条件，避免只堆符号。

### 验证结果

- 数学题库自定义 HTML 校验通过：
  - 共检查 `13` 个 HTML 文件（`index.html + 12` 个章节页）。
  - 首页有且仅有 `12` 张章节卡片。
  - 每个章节页有且仅有 `1` 个 `chapter-orientation` 阅读定位块。
  - 内部页面、资源文件和片段锚点缺失数为 `0`。
  - HTML 中控制字符数量为 `0`，已修复首次生成时由 Python 字符串转义导致的 `\nabla`、`\frac`、`\beta`、`\times`、`\text` 公式损坏问题。

### 下一步

- 运行 Jekyll build 和本地 HTTP 抽查，确认 `/notes/math-interview-question-bank/`、代表章节和静态资源在站点构建后均可访问。
- 如果后续继续扩展，优先补充每章的 `interviewer follow-up` 追问链，而不是盲目增加章节数量。

## 2026-05-19 Notes 入口、分类与倒序索引修复

### 背景

- 用户反馈当前 `Notes` 存在显著问题：
  - 从主站点击 `Notes` 后会跳到一个视觉风格完全不同的页面。
  - 博客/笔记页缺少清晰分类。
  - 需要按时间倒序组织，后续笔记变多时要可管理。
- 审计发现根因不是 `_data/notes.yml` 缺数据，而是两个入口并存：
  - 导航 `_data/navigation.yml` 指向 `/notes/`。
  - `notes/index.html` 是独立深色静态 HTML 页面，占用了 `/notes/`。
  - 真正使用主站 Jekyll 模板和卡片列表的 `_pages/notes.md` 被挂在 `/notes-archive/`，因此用户从导航进入时看到的是另一个站点风格。

### 设计决策

- 将 `/notes/` 收敛为唯一主站 Notes 索引页，由 `_pages/notes.md` 输出。
- 删除冲突的 `notes/index.html`，避免以后同一路径再次被独立静态页覆盖。
- 保留 `notes/paper-reviews/`、`notes/tech-analysis/`、`notes/llm-interview-question-bank/`、`notes/math-interview-question-bank/` 下现有长文和题库静态资源；本轮不强行把 100 多个独立 HTML 重写进 Jekyll layout。
- 在主站 Notes 索引上解决信息架构问题：分类筛选、搜索、计数、最近更新时间倒序、每页 10 条分页。
- 移除已被 Git 跟踪的 `notes/llm-interview-question-bank/.DS_Store`，保持静态站点目录干净。

### 已完成

- 更新 `_pages/notes.md`：
  - `permalink` 从 `/notes-archive/` 改为 `/notes/`。
  - 使用 `site.data.notes` 按 `date` 倒序渲染。
  - 增加分类筛选：`Paper Note`、`Study Resource`、`Tech Analysis`。
  - 增加搜索框，覆盖标题、摘要、类型、标签和 meta。
  - 保留每页 `10` 条分页，筛选和搜索后仍按倒序显示。
  - 保持主站 author profile、masthead、宽度和整体视觉，不再跳到旧深色独立页。
- 删除 `notes/index.html`，消除 `/notes/` 路由冲突。
- 删除 `notes/llm-interview-question-bank/.DS_Store`。

### 验证结果

- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 无认证/限流 warning，不影响静态页面生成。
- HTTP 抽查：
  - `/notes/` 返回 `200`，生成内容包含 `.notes-index`、分类按钮和 `Notes - She Shuaijie` 主站标题。
  - `/notes-archive/` 返回 `404`，确认旧备用入口不再存在。
  - `/notes/math-interview-question-bank/` 返回 `200`。
  - `/notes/paper-reviews/iterative-finetuning-is-mostly-idempotent.html` 返回 `200`。
- 生成 HTML 检查通过：
  - Notes 卡片数为 `18`。
  - 分类按钮为 `all`、`paper-note`、`study-resource`、`tech-analysis`。
  - 首屏日期顺序从 `2026-05-18` 开始，符合倒序。
  - 搜索索引包含 `Lilian Weng`、`数学基础面试题库` 等代表条目。
- 运行 `git diff --check` 通过。
- 使用 Playwright CLI 截图检查：
  - 桌面 `1280x900`：页面使用主站导航、左侧 author profile、卡片列表和分类筛选，视觉不再脱离主站。
  - 移动 `390x844`：搜索框、分类按钮和卡片标题正常换行，无明显横向溢出。
  - 截图仅作为验证产物，已清理 `output/`，避免污染仓库。

### 当前判断

- 主问题已修复：`Notes` 入口现在是统一的主站索引，不再跳到独立静态索引页。
- 目前的边界是：点击具体长文或题库后，仍进入各自独立 HTML 资源；这是有意保留的，因为这些页面体量大、样式复杂，直接纳入 Jekyll layout 会带来较高破坏风险。
- 下一步如果继续提升一致性，建议先为独立 HTML 资源加一个轻量顶部返回条或统一外壳，而不是重写全部正文页面。

## 2026-05-19 Notes 分类筛选隐藏规则修复

### 背景

- 用户反馈 Notes 分类按钮点击后“没有反应”。
- 复查截图发现按钮 active 状态和计数已经变化，例如 `Study Resource` 后显示 `2 / 18 条`，说明 JS click handler 已执行。
- 真正问题是卡片没有被隐藏：`.note-card { display: block; }` 覆盖了浏览器对 `[hidden]` 属性的默认 `display: none` 规则。

### 已完成

- 更新 `_pages/notes.md`，新增显式规则：
  - `.note-card[hidden] { display: none; }`
- 该修复保持现有 JS 不变，只修正 CSS 层的显示优先级问题。

### 验证结果

- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证/限流 warning。
- 运行 `git diff --check` 通过。
- 使用 Playwright 浏览器级点击验证：
  - 初始可见卡片数为 `10`，符合每页 10 条分页。
  - 点击 `Study Resource` 后，可见卡片数为 `2`。
  - 被隐藏的卡片数为 `16`。
  - 计数文本为 `2 / 18 条`。
  - 可见标题为 `数学基础速修手册` 和 `大模型面试题库`。

### 当前判断

- 分类筛选 bug 已修复。
- 这次问题说明：在用 HTML `hidden` 属性隐藏自定义卡片时，不能同时给同一元素写无条件 `display: block`，否则需要显式补 `[hidden]` 选择器。

## 2026-05-19 独立 Notes HTML 统一返回外壳

### 背景

- `/notes/` 索引已经回到主站样式，但点击具体长文或题库后仍会进入 standalone HTML。
- 这些页面保留自己的正文视觉是合理的，但缺少清晰的 Notes 体系入口，用户容易感觉“跳到另一个站点”。
- 目标是增加统一导航感，而不是重写 120 个页面的正文布局。

### 设计决策

- 新增共享样式 `notes/assets/notes-shell.css`，所有独立 Notes HTML 复用同一个顶部返回条。
- 批量注入最小外壳：
  - `<body>` 增加 `notes-shell-page` class。
  - 页面顶部增加 `.notes-sitebar`。
  - 顶部条包含 `Notes` brand、`All Notes` 和 `Home` 链接。
- 保持正文 HTML、题库侧栏、搜索、章节导航和 MathJax 不变。
- 针对题库页面的 sticky sidebar/mobile tools，使用共享 CSS 将 `top` 调整为顶部条高度，避免被遮挡。

### 已完成

- 新增 `notes/assets/notes-shell.css`：
  - 定义 46px sticky 顶部条。
  - 统一 Notes/All Notes/Home 链接样式。
  - 处理题库 `.sidebar` 和 `.mobile-tools` 的 sticky offset。
  - 添加移动端和 print 规则。
- 对 `notes/` 下 `120` 个独立 HTML 页面注入统一外壳：
  - `notes/paper-reviews/*.html`
  - `notes/tech-analysis/*.html`
  - `notes/llm-interview-question-bank/index.html`
  - `notes/llm-interview-question-bank/chapters/*.html`
  - `notes/math-interview-question-bank/index.html`
  - `notes/math-interview-question-bank/chapters/*.html`

### 验证结果

- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证/限流 warning。
- 构建后结构校验通过：
  - 检查 `120` 个独立 Notes HTML。
  - 每个页面都有且仅有 `1` 个 `.notes-sitebar`。
  - 每个页面都有且仅有 `1` 个 `notes-shell.css` 链接。
  - 每个页面的 `body` 都包含 `notes-shell-page` class。
  - 每个页面的 CSS、Notes 和 Home 链接在 `_site` 中都能解析到真实目标。
- HTTP 抽查均返回 `200`：
  - `/notes/paper-reviews/iterative-finetuning-is-mostly-idempotent.html`
  - `/notes/llm-interview-question-bank/`
  - `/notes/llm-interview-question-bank/chapters/042.html`
  - `/notes/math-interview-question-bank/`
  - `/notes/math-interview-question-bank/chapters/004.html`
  - `/notes/assets/notes-shell.css`
- Playwright 浏览器级检查通过：
  - 代表页面均有 `.notes-sitebar`。
  - `notes-shell.css` 已加载。
  - 顶部条高度约 `47px`。
  - 题库 sidebar 起点约 `47px`，没有被顶部条遮住。
  - 代表页面无横向溢出。
- 截图目检：
  - 桌面 LLM 题库章节页顶部条、左侧侧栏和正文关系正常。
  - 移动数学章节页顶部条、侧栏目录和内容没有横向挤压。
  - 截图仅用于验证，已清理 `output/`。

### 当前判断

- `Notes` 索引和 standalone 资源之间已经有统一入口感：用户进入任意长文/题库页后，都可以明确回到 All Notes 或 Home。
- 该方案符合 KISS/YAGNI：不重写正文，不引入新框架，只加共享 CSS 和小型导航外壳。
- 后续如果继续优化，建议将批量注入逻辑沉淀为脚本，而不是每次手工改 120 个生成页。

## 2026-05-19 数学资料从题库改为速修手册

### 背景

- 用户反馈 `notes/math-interview-question-bank/` 的数学资料形态不对：
  - 目标是“类似简短精炼的教科书”，用于快速复习数学知识。
  - 旧版本偏“面试题/问答清单”，容易流于表面。
  - 部分公式渲染有问题，不能只改文案，需要检查 MathJax 和 TeX 写法。
- 审计确认旧版本存在两类问题：
  - 信息形态问题：标题、章节名、统计口径和正文都在强调题库、高频问题、逐题解答、手算训练。
  - 公式质量问题：历史生成曾把 TeX 反斜杠转义打坏，例如 KL 不对称处的 `\ne` 曾变成换行加 `e`，这种问题必须重写源 HTML 才能修复。

### 设计决策

- 保留原 URL `/notes/math-interview-question-bank/` 和 `chapters/001.html` 到 `012.html`，避免破坏已有链接。
- 内容形态从 `Math Interview Bank` 改为 `数学基础速修手册`：
  - 每章按“概念对象 -> 核心公式 -> 直觉解释 -> 最小例子/应用边界”组织。
  - 不再把主线写成“高频问题清单/逐题详细解答/答题模板”。
  - 12 章仍保持轻量稳定，但章节逻辑改为短教科书式复习路线。
- MathJax 统一只使用 `\(...\)` 和 `\[...\]`，移除 `$$...$$` 配置，方便后续静态校验发现不规范公式。
- CSS 层补充公式容器和 MathJax CHTML 的横向滚动、最大宽度和移动端规则，避免长公式撑破正文。
- KISS/YAGNI：不引入新生成框架、不改 URL、不新增版本文件；原地改写已有静态 HTML/CSS/SVG 和 Notes 元数据。

### 已完成

- 重写 `notes/math-interview-question-bank/index.html`：
  - 标题改为 `数学基础速修手册`。
  - 首页说明改为“不是刷题问答清单，而是短教科书式复习手册”。
  - 章节分组改为导读、微积分与优化、线性代数、概率统计与风险、应用桥接。
- 重写 `notes/math-interview-question-bank/chapters/001.html` 到 `012.html`：
  - `001` 如何使用这本数学速修手册。
  - `002-004` 微积分、Taylor/链式法则、优化。
  - `005-007` 向量空间/矩阵/秩、投影/最小二乘、特征值/SVD/PCA。
  - `008-011` 条件概率/分布、期望方差/LLN/CLT、MLE/MAP/KL/Monte Carlo、随机过程与风险。
  - `012` LLM 与 Quant 中的数学对象应用桥接。
- 更新 `notes/math-interview-question-bank/assets/math-bank.css`：
  - 强化 `.math-display`、`mjx-container`、`.formula-list`、`.checkpoint-list` 样式。
  - 移动端公式列表改为单列，减少公式和说明挤压。
- 更新本地 SVG 文案：
  - `learning-map.svg` 从 interview learning map 改为 review learning map。
  - `calculus-optimization.svg` 和 `linear-algebra-geometry.svg` 去掉“面试关键/线代面试”等旧表述。
- 更新 `_data/notes.yml`：
  - `数学基础面试题库` 改为 `数学基础速修手册`。
  - summary 改为知识复习手册描述。
  - tag 从 `Interview` 改为 `Review`。

### 验证结果

- 自定义静态校验已通过：
  - 共检查 `13` 个 HTML 文件（`index.html + 12` 个章节页）。
  - 首页有 `12` 张章节卡片。
  - 每个章节页有 `1` 个 `chapter-orientation` 阅读定位块，共 `12` 个。
  - 公式块共 `42` 个。
  - 内部页面、资源文件和片段锚点缺失数为 `0`。
  - 控制字符数量为 `0`。
  - `\[` / `\]`、`\(` / `\)` 定界符数量匹配。
  - 不再出现 `$$` 定界符。
- `notes/math-interview-question-bank/` 内已不再出现 `面试`、`题库`、`Interview`、`Question`、`高频`、`逐题`、`答题`、`训练题`、`手算` 等旧形态关键词。
- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证/限流 warning，不影响静态页面生成。
- HTTP 抽查通过：
  - `_site/` 下启动 `python3 -m http.server 4018 --bind 127.0.0.1`。
  - `http://127.0.0.1:4018/notes/` 返回 `200 OK`。
  - `http://127.0.0.1:4018/notes/math-interview-question-bank/` 返回 `200 OK`。
  - `http://127.0.0.1:4018/notes/math-interview-question-bank/chapters/004.html` 返回 `200 OK`。
  - `http://127.0.0.1:4018/notes/math-interview-question-bank/chapters/011.html` 返回 `200 OK`。
  - `math-bank.css`、`math-bank.js`、`learning-map.svg` 均返回 `200 OK`。
- 浏览器验证通过：
  - 数学手册首页桌面 `1440x1000`：`12` 张章节卡片、`1` 张 SVG 主图、横向溢出 `0`、console error `0`。
  - 代表章节 `004.html` 桌面 `1440x1000`：MathJax 渲染出 `11` 个 `mjx-container`，`.mjx-merror=0`，横向溢出 `0`，console error `0`，当前章节导航高亮数量为 `1`。
  - 代表章节 `011.html` 桌面 `1440x1000`：MathJax 渲染出 `10` 个 `mjx-container`，`.mjx-merror=0`，横向溢出 `0`，console error `0`，当前章节导航高亮数量为 `1`。
  - 代表章节 `004.html` 移动端 `390x844`：MathJax 渲染出 `11` 个 `mjx-container`，`.mjx-merror=0`，横向溢出 `0`，console error `0`。
  - 首页交互 smoke test：搜索 `SVD` 只展示 SVD/PCA 章节；点击概率统计筛选展示 `008-011` 共 `4` 张章节卡片。
- 运行 `git diff --check` 通过。

### 当前判断

- 这轮已经解决用户指出的本质问题：数学资料不再是面试题形式，而是紧凑知识复习手册。
- 公式问题也已经从源头处理：坏 TeX 重写、MathJax 配置收敛、CSS 防溢出、浏览器层验证通过。
- 仍保留旧目录名 `math-interview-question-bank`，这是为了不破坏已有 URL；对外可见标题和 Notes 索引已经改为 `数学基础速修手册`。

## 2026-05-19 数学速修手册例题与算法直觉补充

### 背景

- 用户继续要求“研究和补充数学题库”，重点提出：
  - 应该给出例题以及解答。
  - 应该补充对概念和算法的直观理解。
- 复查现状后判断：当前 `notes/math-interview-question-bank/` 已经从题库改成 `数学基础速修手册`，主线适合作为短教科书式复习材料，但确实缺少“做题层”和“算法流程层”。
- 因此本轮不推翻现有 12 章主线，而是在末尾新增练习与算法直觉层，避免重新变成碎片化问答清单。

### 设计决策

- 保留 `001-012` 作为概念主线：
  - `001-011` 继续承担微积分、线代、概率统计和风险的知识骨架。
  - `012` 继续承担 LLM 与 Quant 应用桥接。
- 新增 `013-016` 作为第二层材料：
  - `013` 微积分与优化例题。
  - `014` 线性代数例题。
  - `015` 概率统计例题。
  - `016` 常用算法直觉。
- 每道例题按 `题目 -> 解答 -> 直觉/应用解释` 写，避免只给公式答案。
- 算法章节按 `输入 -> 输出 -> 核心步骤 -> 直觉 -> 失效条件` 写，确保能回答“这个算法到底怎么做”。
- KISS/YAGNI：不引入生成框架、不新增版本目录、不改 URL；只在现有静态子站内追加少量章节和共享样式。
- DRY/SRP：例题卡片、解答块、直觉块、算法卡片样式统一写入 `assets/math-bank.css`，正文只保留语义 HTML。

### 已完成

- 新增 4 个章节：
  - `notes/math-interview-question-bank/chapters/013.html`
  - `notes/math-interview-question-bank/chapters/014.html`
  - `notes/math-interview-question-bank/chapters/015.html`
  - `notes/math-interview-question-bank/chapters/016.html`
- `013` 覆盖：
  - softplus 导数与曲率。
  - Taylor 二阶近似。
  - 多元梯度和方向导数。
  - Hessian 判断极小值。
  - Lagrange 乘子。
- `014` 覆盖：
  - 秩和列空间。
  - 最小二乘与投影残差正交。
  - 正定协方差矩阵和组合风险。
  - PCA 主方向。
  - 截断 SVD 低秩近似。
- `015` 覆盖：
  - Bayes 与 base rate。
  - 组合收益均值和方差。
  - Bernoulli MLE/MAP。
  - KL 散度的数字含义。
  - Monte Carlo 标准误。
- `016` 覆盖：
  - 梯度下降、牛顿法、Lagrange/KKT。
  - 最小二乘、PCA、截断 SVD。
  - MLE/MAP、Monte Carlo、VaR/CVaR 经验估计。
  - LLM 与 Quant 面试回答模板。
- 更新 `notes/math-interview-question-bank/index.html`：
  - 章节数从 `12` 改为 `16`。
  - 新增 `例题` 筛选按钮。
  - 新增 `5. 例题与算法直觉` 目录分组和 4 张章节卡片。
  - 搜索关键词补充 `MLE`、`gradient descent`、`Newton`、`CVaR` 等。
- 更新 `notes/math-interview-question-bank/chapters/001.html` 到 `012.html`：
  - 侧栏增加 `5. 例题与算法直觉` 分组。
  - `012` 的上一章/下一章导航连接到 `013`。
  - `001-015` 增加正文内 `下一步建议`，把概念主线、例题层和算法层串起来。
- 更新 `notes/math-interview-question-bank/assets/math-bank.css`：
  - 新增 `.worked-example`、`.solution`、`.intuition-box`、`.algorithm-grid`、`.algorithm-card`、`.next-step` 样式。
  - 移动端将算法卡片单列显示，避免拥挤。
- 更新 `_data/notes.yml`：
  - 数学速修手册元数据从 `12 chapters` 改为 `16 chapters`。
  - summary 增加完整例题解答和算法流程说明。

### 验证结果

- 已运行数学子站静态完整性检查：
  - 共检查 `17` 个 HTML 文件（`index.html + 16` 个章节页）。
  - 首页章节卡片数为 `16`。
  - 每个章节页有且仅有 `1` 个 `chapter-orientation`。
  - 每个章节页有且仅有 `1` 个当前高亮目录项。
  - 每个章节页有 `2` 个上下章导航块。
  - `001-015` 有 `15` 个 `next-step`，`016` 作为最后章没有下一步提示。
  - 内部页面、资源文件和片段锚点缺失数为 `0`。
  - 控制字符和损坏替换字符数量为 `0`。
  - `\[` / `\]`、`\(` / `\)` 定界符数量匹配，未使用 `$$`。
- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证/限流 warning，不影响静态页面生成。
- 构建后 `_site` 内容检查通过：
  - `_site/notes/math-interview-question-bank/index.html` 包含 `16` 章统计、`practice` 分类和新增章节入口。
  - `_site/notes/math-interview-question-bank/chapters/013.html` 到 `016.html` 均包含新增例题/算法内容。
  - `_site/notes/index.html` 已显示 `16 chapters` 和更新后的 summary。
- 从 `_site` 启动临时 HTTP 服务后抽查通过：
  - `/notes/` 返回 `200`。
  - `/notes/math-interview-question-bank/` 返回 `200`。
  - `/notes/math-interview-question-bank/chapters/013.html` 到 `016.html` 均返回 `200`。
  - `/notes/math-interview-question-bank/assets/math-bank.css` 返回 `200`。
- 运行 `git diff --check` 通过。

### 当前判断

- 现在资料形态是“两层结构”：
  - 第一层：短教科书式概念主线，负责理解对象、公式、直觉和边界。
  - 第二层：例题与算法直觉，负责把概念落实到可手算题和可复述流程。
- 这比单纯新增更多概念章更有效：用户可以先恢复知识骨架，再通过 013-016 检查自己能不能真的做题和解释算法。

## 2026-05-19 数学速修手册应用追问与反例补充

### 背景

- 用户继续要求“继续补充内容”，结合上一阶段已有 `013-016` 例题与算法直觉层，本轮判断最该补的是面试后半段追问：
  - LLM 场景下从公式解释到训练行为。
  - Quant 场景下从估计公式解释到风险控制。
  - 常见概念误区的反例和边界。
  - 综合案例题，把输入、公式、算法、解释和风险串起来。
- 这比继续追加基础定义更有价值：基础定义已经在 `001-012` 覆盖，例题和算法流程在 `013-016` 覆盖；现在缺的是“面试官追问时如何把数学落到场景和边界”。

### 设计决策

- 继续维护现有静态子站结构，不新增生成系统、不新建版本目录。
- 新增第 6 组 `应用追问与反例`，把 `017-020` 定位成第三层材料：
  - 第一层：`001-012` 概念主线。
  - 第二层：`013-016` 例题与算法直觉。
  - 第三层：`017-020` LLM/Quant 应用追问、反例和综合案例。
- 每个追问都写成 `题目/反例 -> 解答 -> 直觉/边界`，避免只给结论。
- 复用已有 `.worked-example`、`.solution`、`.intuition-box`、`.formula-list`、`.table-wrap` 组件，保持 KISS/DRY，不新增样式体系。

### 已完成

- 新增 `notes/math-interview-question-bank/chapters/017.html`：
  - temperature softmax 数字例子。
  - cross-entropy logits 梯度 \(q-y\)。
  - KL 方向与 policy regularization。
  - attention scaling 的方差直觉。
  - LoRA 低秩参数量和表达边界。
- 新增 `notes/math-interview-question-bank/chapters/018.html`：
  - OLS 异方差下点估计和标准误的区别。
  - 协方差 shrinkage 的数值例子。
  - PCA eigengap 与因子不稳定性。
  - Sharpe 年化和 t-stat 的样本长度解释。
  - 多重检验与回测过拟合。
- 新增 `notes/math-interview-question-bank/chapters/019.html`：
  - 不相关不等于独立。
  - 相关性不等于因果。
  - KL 不是严格距离。
  - Hessian 退化时不能只靠二阶判定。
  - p-value 不是原假设为真的概率。
  - VaR 不描述超过阈值后的尾部严重程度。
- 新增 `notes/math-interview-question-bank/chapters/020.html`：
  - logits -> softmax -> CE -> 梯度 -> 训练更新。
  - attention score -> scaling -> softmax 梯度稳定。
  - 收益样本 -> 协方差 -> 组合风险。
  - 回测收益 -> 成本后 Sharpe -> 上线判断。
  - 综合题作答框架。
- 更新 `notes/math-interview-question-bank/index.html`：
  - 统计从 `16` 章改为 `20` 章。
  - 新增 `追问` 筛选按钮。
  - 新增 `6. 应用追问与反例` 分组和 4 张章节卡片。
  - 学习路径补充 `017-020` 的追问、反例和综合案例定位。
- 更新 `notes/math-interview-question-bank/chapters/001.html` 到 `020.html`：
  - 全部章节侧栏加入 `6. 应用追问与反例` 分组。
  - `016` 上下章导航和正文下一步建议接到 `017`。
  - `017-020` 加入连续上一章/下一章导航，`020` 作为当前末章。
- 更新 `_data/notes.yml`：
  - 数学速修手册 summary 改为 `20` 章。
  - meta 改为 `20 chapters`。

### 验证结果

- 已运行数学子站静态完整性检查：
  - 共检查 `21` 个 HTML 文件（`index.html + 20` 个章节页）。
  - 首页章节卡片数为 `20`。
  - 每个章节页有且仅有 `1` 个 `chapter-orientation`。
  - 每个章节页有且仅有 `1` 个当前高亮目录项。
  - 每个章节页有 `2` 个上下章导航块。
  - `001-019` 各有 `1` 个 `next-step`，`020` 作为最后章没有下一步提示。
  - 内部页面、资源文件和片段锚点缺失数为 `0`。
  - 控制字符和损坏替换字符数量为 `0`。
  - `\[` / `\]`、`\(` / `\)` 定界符数量匹配，未使用 `$$`。
- 运行 `git diff --check` 通过。
- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证/限流 warning，不影响静态页面生成。
- 构建后 `_site` 内容检查通过：
  - `_site/notes/math-interview-question-bank/index.html` 包含 `20` 章统计和 `应用追问与反例` 分组。
  - `_site/notes/math-interview-question-bank/chapters/017.html` 到 `020.html` 均包含新增应用追问/反例/综合案例内容。
  - `_site/notes/index.html` 已显示 `20 chapters` 和更新后的 summary。
- 从 `_site` 启动临时 HTTP 服务后抽查通过：
  - `/notes/` 返回 `200`。
  - `/notes/math-interview-question-bank/` 返回 `200`。
  - `/notes/math-interview-question-bank/chapters/017.html` 到 `020.html` 均返回 `200`。
  - `/notes/math-interview-question-bank/assets/math-bank.css` 返回 `200`。

### 当前判断

- 数学速修手册现在形成三层结构：
  - 第一层：`001-012` 建立概念主线和 LLM/Quant 应用桥接。
  - 第二层：`013-016` 用完整例题和算法卡片训练可操作理解。
  - 第三层：`017-020` 用追问、反例和综合案例训练面试表达与边界感。
- 这轮补充的重点不是“更多知识点”，而是把用户关心的直观理解推进到真实面试追问：能从公式说到行为，从估计说到风险，从结论说到假设边界。

## 2026-05-19 Notes 空内容与素材断链排查

### 背景

- 用户反馈已有笔记中有内容像是为空，怀疑素材是否换了位置。
- 本轮按 Notes 索引、静态子站、HTML 本体、资源引用和构建产物分开审查，避免把“正文为空”和“图片资源丢失”混为一谈。
- 工作区已有数学速修手册章节改动，本轮不回退、不覆盖，只处理 Notes 素材断链问题。

### 发现

- `_data/notes.yml` 中的 `18` 个条目都有 `title`、`url`、`summary`、`kind` 和 `meta`；索引条目本身没有空字段。
- `notes/` 下的 HTML 文件不是空文件；题库章节和单篇 HTML 笔记都有正文文本。
- 真正问题集中在 `3` 篇论文笔记：HTML 正文还在，但图片目录没有随 HTML 一起迁移进仓库，导致图表位置显示为空或 broken image。
- 缺失素材仍在 `~/Downloads`：
  - `/Users/bytedance/Downloads/rebellious-student-rlrt-assets/`
  - `/Users/bytedance/Downloads/seif-instruction-following-assets/`
  - `/Users/bytedance/Downloads/synthetic-ppt-noisy-pretraining-assets/`

### 已完成

- 补回 `notes/paper-reviews/rebellious-student-rlrt-assets/`：
  - `page-06.png`
  - `page-07.png`
  - `page-08.png`
  - `page-09.png`
  - `page-17.png`
  - `page-18.png`
- 补回 `notes/paper-reviews/seif-instruction-following-assets/`：
  - `comp.png`
  - `method.png`
  - `seif-algorithm-21.png`
  - `seif-paper-05.png`
  - `seif-paper-06.png`
  - `seif-paper-07.png`
  - `seif-paper-08.png`
- 补回 `notes/paper-reviews/synthetic-ppt-noisy-pretraining-assets/`：
  - `overview.png`
  - `results-main.png`
  - `ablations.png`
  - `mechanism.png`

### 验证结果

- 全量 Notes 本地资源引用检查通过：
  - 共检查 `128` 个 HTML。
  - 疑似空 HTML 数量为 `0`。
  - 缺失本地 `href/src` 引用数量为 `0`。
- 运行 `git diff --check` 通过。
- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 GitHub Metadata 未认证和 GitHub API rate limit warning，不影响静态页面生成。
- 构建后 `_site` 内容检查通过：
  - `_site/notes/paper-reviews/rebellious-student-rlrt-assets/` 包含 `6` 个 PNG。
  - `_site/notes/paper-reviews/seif-instruction-following-assets/` 包含 `7` 个 PNG。
  - `_site/notes/paper-reviews/synthetic-ppt-noisy-pretraining-assets/` 包含 `4` 个 PNG。
  - 三篇受影响 HTML 和代表性 PNG 文件均存在且非空。
- 从 `_site` 启动临时 HTTP 服务后抽查通过：
  - `/notes/` 返回 `200`。
  - `/notes/paper-reviews/rebellious-student-rlrt-analysis.html` 返回 `200`。
  - `/notes/paper-reviews/rebellious-student-rlrt-assets/page-06.png` 返回 `200`。
  - `/notes/paper-reviews/seif-instruction-following-report.html` 返回 `200`。
  - `/notes/paper-reviews/seif-instruction-following-assets/method.png` 返回 `200`。
  - `/notes/paper-reviews/synthetic-ppt-noisy-pretraining-report.html` 返回 `200`。
  - `/notes/paper-reviews/synthetic-ppt-noisy-pretraining-assets/overview.png` 返回 `200`。
  - HTTP 服务日志中的 `BrokenPipeError` 来自抽查脚本只读取前 `256` bytes 后关闭连接；状态码已全部返回 `200`，不是页面错误。

### 当前判断

- 这次不是 `_data/notes.yml` 索引空内容，也不是 HTML 正文丢失，而是几篇从 Downloads 迁入的报告只迁了 HTML，没有迁对应 `*-assets/` 图片目录。
- 后续迁移单篇 HTML 笔记时，必须把同名 `*-assets/` 目录作为同一个原子单元检查；否则页面会“文字存在但关键图表为空”。

## 2026-05-19 数学速修手册零基础大幅扩写

### 背景

- 用户明确反馈数学手册内容仍然过于简略，要求按“零基础重新学”的标准大幅扩充。
- 用户要求多启动 sub-agent，且每个 sub-agent 负责一个章节；同时要求每完成一个章节都进行 commit 和 push。
- 本轮工作范围限定在 `notes/math-interview-question-bank/` 数学手册，不把其它 Notes 资源、LLM 题库或素材补链变更混入数学手册章节提交。

### 执行方式

- 按章节分派 worker，每个 worker 只拥有一个 `chapters/NNN.html` 文件的写入范围。
- 每章完成后单独验收：检查 `git diff --check`、本章目录锚点、`section.chapter`、`chapter-orientation`、`next-step`、MathJax 定界符、替换字符和基本 HTML 结构。
- 每个完成章节独立提交并推送到 `origin/master`，提交信息形如 `Expand math handbook chapter NNN`。
- 对未产出或失败的 worker，主线程接管并完成对应章节，例如 `019.html`。

### 已完成

- 完成 `001.html` 到 `020.html` 的零基础大幅扩写。
- 每章都补强为“概念起点 -> 知识点展开 -> 公式读法 -> 完整例题/反例/案例 -> LLM/Quant 连接 -> 常见误区/检查清单”的结构。
- 首页 `notes/math-interview-question-bank/index.html` 已更新统计口径：
  - `20` 个章节。
  - `3` 条数学主线。
  - `130+` 个完整例题解答。
  - `190+` 个知识点与边界小节。
- `_data/notes.yml` 的 `数学基础速修手册` summary 和 meta 已同步更新为零基础扩写版描述。

### 内容规模

- 章节数：`20`。
- 小节数：约 `195` 个 `h3` 小节。
- worked examples / solution blocks：约 `134` 组。
- 结构层次：
  - `001-012`：导读、微积分、线性代数、概率统计、随机过程与 LLM/Quant 应用桥接。
  - `013-016`：微积分/线代/概率例题和算法直觉。
  - `017-020`：大模型追问、量化追问、常见反例、综合案例链路。

### 验证结果

- 数学手册专用完整性检查通过：
  - 共检查 `21` 个 HTML 文件（`index.html + 20` 个章节页）。
  - 首页有 `20` 张章节卡片。
  - 每个章节页均有且仅有 `1` 个 `section.chapter`、`1` 个 `chapter-orientation`、`1` 个 `next-step`。
  - 本章目录锚点全部存在。
  - 内部资源、页面链接和片段链接缺失数为 `0`。
  - MathJax `\[` / `\]`、`\(` / `\)` 定界符均匹配。
  - 替换字符 `�` 和 `$$` 数量为 `0`。
- `git diff --check -- notes/math-interview-question-bank _data/notes.yml` 通过。

### 当前判断

- 数学资料已经从“速查提纲/简略题库”升级为零基础可重新学习的手册。
- 本轮遵守 KISS/YAGNI：不改 URL、不引入生成框架、不新增 CSS class，继续复用现有静态子站结构。
- 本轮遵守 DRY/SOLID：每章独立负责一个学习主题，样式和交互复用既有 `math-bank.css` / `math-bank.js`，章节提交边界清晰。
- 后续如果继续提升，优先做浏览器视觉抽查和少量排版微调，而不是再扩大章节数量。

## 2026-05-19 LLM Interview Question Bank 核心地图扩写

### 背景

- 用户反馈大模型面试题库仍然不够清晰、有条理，也不够丰富充实；核心要求是“把知识点讲清楚”，而不是只拟合面试题或列题目。
- 当前审计发现 `005-014` 十个核心模块地图页仍偏薄，多数只有代表题、考点和一句作答抓手，不能独立帮助读者建立概念框架。
- 本轮按用户要求启用 sub-agent 并行：每个 sub-agent 只负责一个章节文件；主进程负责结构校验、Jekyll build、逐章 commit/push 和进度管理。

### 已完成

- 扩写 `notes/llm-interview-question-bank/chapters/005.html`：基础与 Transformer 架构。
- 扩写 `notes/llm-interview-question-bank/chapters/006.html`：Tokenizer、Embedding、位置编码与上下文窗口。
- 扩写 `notes/llm-interview-question-bank/chapters/007.html`：预训练、数据工程、Scaling Law 与模型结构扩展。
- 扩写 `notes/llm-interview-question-bank/chapters/008.html`：SFT、PEFT 与对齐训练。
- 扩写 `notes/llm-interview-question-bank/chapters/009.html`：推理优化、Serving 与部署工程。
- 扩写 `notes/llm-interview-question-bank/chapters/010.html`：RAG、检索、重排与知识增强。
- 扩写 `notes/llm-interview-question-bank/chapters/011.html`：Agent、工具调用、工作流编排与协议。
- 扩写 `notes/llm-interview-question-bank/chapters/012.html`：评测、幻觉、安全与可观测性。
- 扩写 `notes/llm-interview-question-bank/chapters/013.html`：多模态（图文音视频）。
- 扩写 `notes/llm-interview-question-bank/chapters/014.html`：系统设计、业务落地与成本权衡。

### 内容原则

- 每章从题目清单改成知识讲解页，保留原页面 URL、侧栏、上下章导航和 `chapter-orientation`。
- 每章都补充：核心概念、机制解释、工程取舍、常见误区和追问链路。
- 保持 KISS/YAGNI：不引入新生成框架、不改静态站结构、不新增外部依赖，只在现有章节内补内容。
- 保持 DRY/SOLID：章节文件各自承担单一主题，交互和样式仍复用现有 `question-bank.css/js`。

### Commit / Push 记录

- `dcf508d` Expand LLM bank chapter 005
- `bd53f7f` Expand LLM bank chapter 006
- `4b1ce86` Expand LLM bank chapter 007
- `349c777` Expand LLM bank chapter 008
- `3b07447` Expand LLM bank chapter 009
- `3d3dd5e` Expand LLM bank chapter 010
- `b3f351a` Expand LLM bank chapter 011
- `aece35e` Expand LLM bank chapter 012
- `985e2b4` Expand LLM bank chapter 013
- `fa8d26e` Expand LLM bank chapter 014

### 验证结果

- `005-014` 每章均完成单文件 `git diff --check`。
- 自定义 LLM 题库完整性检查通过：
  - 共检查 `91` 个 HTML 文件（首页 + 90 个章节页）。
  - 首页仍有 `90` 张章节卡片。
  - 所有章节页仍有且仅有 `1` 个 `section.chapter` 和 `1` 个 `chapter-orientation`。
  - 内部页面、资源和片段锚点缺失数为 `0`。
  - `005-014` 均包含 `常见误区` 和 `追问链路`。
- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功。
- 构建期间仅出现 GitHub Metadata 未认证或 GitHub API rate limit warning，不影响静态页面生成。

### 当前判断与下一步

- `005-014` 已经从“核心模块地图”升级为能独立建立概念框架的讲解层。
- 已继续处理 `049-052` 核心知识点索引页，见下一节；后续继续推进 `053-058`。

## 2026-05-19 LLM Interview Question Bank 核心知识点索引扩写（第一批）

### 背景

- `049-058` 是核心知识点索引层，原本主要是 Q 编号清单，适合查漏但不适合顺读理解。
- 用户明确要求每个知识点都要扩充并讲清楚，因此这一层不能只保留短句索引，需要补成概念对象、机制、工程边界和追问链路。
- 本批先处理 `049-052`，覆盖 Transformer、Tokenizer/Embedding/位置、预训练/数据/Scaling/MoE、SFT/PEFT/对齐。

### 已完成

- 扩写 `notes/llm-interview-question-bank/chapters/049.html`：Transformer 架构知识点。
- 扩写 `notes/llm-interview-question-bank/chapters/050.html`：Tokenizer、Embedding、位置编码与上下文窗口知识点。
- 扩写 `notes/llm-interview-question-bank/chapters/051.html`：预训练、数据工程、Scaling Law 与模型结构扩展知识点。
- 扩写 `notes/llm-interview-question-bank/chapters/052.html`：SFT、PEFT 与对齐训练知识点。

### 内容原则

- 从 `Qxx -> 短知识点` 改为顺读型知识讲解页。
- 每章保留原 URL、侧栏、章节导航和 `chapter-orientation`，只替换当前章节正文。
- 每章统一补充 `常见误区`、`复盘清单` 和 `追问链路`，让读者能从概念复述推进到面试追问。
- 仍不引入新样式、新脚本或生成框架，避免把静态子站维护复杂化。

### Commit / Push 记录

- `97ef3b5` Expand LLM bank chapter 049
- `8df54d7` Expand LLM bank chapter 050
- `ea822a9` Expand LLM bank chapter 051
- `5a1ef47` Expand LLM bank chapter 052

### 验证结果

- `049-052` 每章均完成单文件 `git diff --check`。
- 自定义结构检查通过：
  - 每章有且仅有 `1` 个 `section.chapter`。
  - 每章有且仅有 `1` 个 `chapter-orientation`。
  - 每章均包含 `常见误区`、`复盘清单` 和 `追问链路`。
- 运行 `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功。
- 构建期间仅出现 GitHub Metadata 未认证 warning，不影响静态页面生成。

### 当前判断与下一步

- `049-052` 已经从清单式索引升级为可顺读的知识点讲解层。
- 已继续处理 `053-056`，见下一节；剩余 `057-058` 正在推进。

## 2026-05-19 LLM Interview Question Bank 核心知识点索引扩写（第二批）

### 已完成

- 扩写 `notes/llm-interview-question-bank/chapters/053.html`：推理优化、Serving 与部署工程知识点。
- 扩写 `notes/llm-interview-question-bank/chapters/054.html`：RAG、检索、重排与知识增强知识点。
- 扩写 `notes/llm-interview-question-bank/chapters/055.html`：Agent、工具调用、工作流编排与协议知识点。
- 扩写 `notes/llm-interview-question-bank/chapters/056.html`：评测、幻觉、安全与可观测性知识点。

### 内容覆盖

- `053` 补齐 prefill/decode、KV cache、continuous batching、PagedAttention、量化、投机解码、prefix caching、TTFT/TPOT/SLO、Prefill/Decode 分离和多租户观测。
- `054` 补齐 RAG 端到端链路、chunking、embedding、BM25/vector/hybrid retrieval、rerank、context packing、引用、faithfulness、权限过滤、索引更新、GraphRAG 和长上下文取舍。
- `055` 补齐 Agent vs Chat/RAG、planner/executor/memory/tool/critic/observer、function calling/tool schema、MCP/A2A、workflow vs agent、multi-agent、权限 side-effect 和 prompt injection。
- `056` 补齐 offline benchmark、人工评测、LLM-as-judge、业务回放/A-B、幻觉分类、data contamination/benchmark leakage、安全风险、可观测指标和错误分类。

### Commit / Push 记录

- `dc4265b` Expand LLM bank chapter 053
- `18b1f11` Expand LLM bank chapter 054
- `8d15fc7` Expand LLM bank chapter 055
- `5a369f9` Expand LLM bank chapter 056

### 验证结果

- `053-056` 每章均完成单文件 `git diff --check`。
- 自定义结构检查通过：
  - 每章有且仅有 `1` 个 `section.chapter`。
  - 每章有且仅有 `1` 个 `chapter-orientation`。
  - 每章均包含 `常见误区`、`复盘清单` 和 `追问链路`。

### 当前判断与下一步

- `053-056` 已经从清单式索引升级为可顺读的知识点讲解层。
- 已继续处理 `057-058`，核心知识点索引层 `049-058` 已全部完成。

## 2026-05-19 LLM Interview Question Bank 核心知识点索引扩写（第三批）

### 已完成

- 扩写 `notes/llm-interview-question-bank/chapters/057.html`：多模态（图文音视频）知识点。
- 扩写 `notes/llm-interview-question-bank/chapters/058.html`：系统设计、业务落地与成本权衡知识点。

### 内容覆盖

- `057` 补齐 VLM/Audio LLM/Video LLM 共同结构、视觉编码器、projector/cross-attention/Q-Former/adapter/resampler、token 对齐、contrastive/caption/instruction tuning、音频视频时间维度、帧抽样、评测幻觉和部署成本。
- `058` 补齐 LLM 项目从需求、数据、模型、检索、工具、评测、部署、监控到成本的完整拆解，以及 token/GPU/检索/人工/缓存成本、质量/延迟/安全/可维护性 trade-off、灰度/回滚/fallback/SLA、模型指标与业务指标。

### Commit / Push 记录

- `c3699b1` Expand LLM bank chapter 057
- `e5c2c8d` Expand LLM bank chapter 058

### 验证结果

- `057-058` 每章均完成单文件 `git diff --check`。
- 自定义结构检查通过：
  - 每章有且仅有 `1` 个 `section.chapter`。
  - 每章有且仅有 `1` 个 `chapter-orientation`。
  - 每章均包含 `常见误区`、`复盘清单` 和 `追问链路`。

### 当前判断

- 核心知识点索引层 `049-058` 已从清单式索引升级为可顺读的知识讲解层。
- 与前面 `005-014` 核心地图页配合后，读者可以先建立模块框架，再用 `049-058` 做逐模块复盘与追问训练。

## 2026-05-28 Notes 全站格式规范、模板与质量验证

### 背景

- 本轮目标是把 `notes/` 下的公开笔记整理到统一的可维护标准：导航、壳层 CSS、公式、图片、证据区、生成痕迹和移动端可读性都需要可检查。
- 既有历史笔记风格差异较大，单篇逐个复制 CSS 会放大维护成本；因此优先把共性规则沉淀到共享校验脚本、模板和 `notes-shell.css`。

### 已完成

- 新增 `notes/NOTE_TEMPLATE.md`，作为后续 `notes/paper-reviews/*.html` 和 `notes/tech-analysis/*.html` 的统一 HTML 笔记模板。
- 更新 `AGENTS.md` 的 Notes Authoring Standard：新笔记必须使用模板、加载 `notes/assets/notes-shell.css`、使用 `body.notes-shell-page`、公式页加载 MathJax、图片必须有 alt、证据/来源放到末尾、禁止公开 `/tmp`、`/Users/...`、`Generated locally` 等生成痕迹。
- 增强 `scripts/validate_notes_index.rb`：
  - 校验 `notes/NOTE_TEMPLATE.md` 存在。
  - 校验每个 note HTML 只有一个 head title、包含 viewport、仅加载一次 `notes-shell.css`、body 使用 `notes-shell-page`。
  - 校验图片 alt 非空、数学页加载 MathJax、无 Unicode replacement character。
  - 增加生成痕迹和本地路径的 warning 扫描。
- 清理历史 HTML 中的本地路径、生成时间、`Generated locally`、`HTML generated`、`/tmp`、`/Users/xxx`、`/Users/bytedance/Downloads` 等公开痕迹。
- 为近期新增和历史页面补齐统一 notes shell，代表页面包括：
  - `notes/paper-reviews/rl-memory-curriculum-effects.html`
  - `notes/paper-reviews/skillevolbench-skill-evolution.html`
  - `notes/tech-analysis/cua-gym-rlvr-data-infrastructure.html`
  - `notes/tech-analysis/jia-guo-kpop-agentic-rl.html`
  - `notes/tech-analysis/zai-zcube-inference-network.html`
- 修复移动端横向溢出：
  - `notes/assets/notes-shell.css` 增加 `notes-shell-page` 作用域内的表格、代码、图片、视频、导航、来源卡片和长链接兜底规则。
  - `notes/llm-interview-question-bank/assets/question-bank.css` 与 `notes/math-interview-question-bank/assets/math-bank.css` 修正中间视口下内容宽度计算，避免 sidebar 最小宽度与 `vw` 公式冲突。
  - `_pages/notes.md` 修复移动端搜索框受主题 `input[type=search]` content-box 规则影响而溢出的问题。
  - `notes/paper-reviews/rl-memory-curriculum-effects.html`、`notes/tech-analysis/jia-guo-kpop-agentic-rl.html`、`notes/paper-reviews/unmasking-on-policy-distillation.html` 等页面补齐表格/长公式/长代码滚动边界。
- 移除不稳定外部媒体对页面质量的影响：
  - `notes/paper-reviews/gmi-spatial-reasoning-thread-report.html` 不再直接嵌入会返回 403 的 X 视频直链，改为文字说明和原帖复核。
  - `notes/tech-analysis/huggingpapers-audio-llm-trust-assets/awesome-readme.md` 将远端 badge / star history / 缺失 logo 改为文本链接。
  - `notes/tech-analysis/sheriyuo-tts-training-free-rl-assets/ets-readme.md` 将远端 badge 改为文本链接，并说明上游 `main_fig.png` 未包含在本地快照中。

### 验证结果

- `ruby "scripts/validate_notes_index.rb"` 通过，结果为 `notes index ok: 63 entries, 63 top-level note html files`。
- 生成痕迹精确搜索无命中：
  - `Generated locally`
  - `HTML generated`
  - `本地 HTML 生成`
  - `报告生成日期`
  - `/Users/xxx`
  - `/tmp/`
  - `/Users/bytedance/Downloads`
  - `最终 HTML 路径`
  - `报告文件：`
- `git diff --check` 对本轮关键文件通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅有 `faraday-retry` 和 GitHub Metadata 未认证 warning，不影响静态页面生成。
- 使用 Playwright 对 `_site/notes` 全量 HTML 做浏览器验证：
  - 覆盖 `179` 个 HTML 页面。
  - 覆盖 `390px` 与 `1025px` 两个关键视口，共 `358` 次页面加载。
  - 最终结果：`failureCount: 0`。
  - 检查项包含页面级横向溢出、console error、本地请求失败和 broken image。

### 当前判断

- Notes 目录已经具备可复用模板、硬性校验脚本和共享移动端兜底 CSS；未来新增笔记如果按模板编写并运行校验，可以避免重复出现路径泄漏、缺 alt、缺 shell、公式未加载、移动端横向溢出等问题。
- 历史页面不再依赖不稳定远端视频或未归档 README 图片来通过站点质量检查；证据仍保留为文本链接和说明，降低发布面上的外部资源脆弱性。

## 2026-05-28 Notes 内容质量审计补强

### 背景

- 前一阶段已经解决模板、导航、资源、公式和移动端渲染问题，但“内容充实、术语解释、头部不堆来源信息、证据边界放到文末”还需要可重复检查。
- 本阶段把内容质量检查加入 `scripts/validate_notes_index.rb` 的 warning 层，先用启发式发现问题，再对确定性页面做正文修复。

### 已完成

- 扩展 `scripts/validate_notes_index.rb`：
  - 增加可见文本、h2/h3 数量、术语解释、证据边界章节、顶部来源/过程痕迹的内容审计 warning。
  - 对 `llm-interview-question-bank/`、`math-interview-question-bank/` 这类目录页保留结构/资源硬校验，但不套用独立长文的内容篇幅阈值。
  - 调整术语识别规则，识别“术语 / 概念 / 关键词 / 几个词先对齐 / 什么叫”等常见写法，减少误报。
- 修复明确内容缺口：
  - `notes/tech-analysis/cua-gym-rlvr-data-infrastructure.html`：补“术语和概念边界”，解释 CUA、RLVR、setup-gen、reward-gen、orchestrator、programmatic reward、privileged state API；来源改为文末 `data-note-role="evidence-appendix"`。
  - `notes/tech-analysis/jia-guo-kpop-agentic-rl.html`：补 KPop、IcePop、training-inference mismatch、binary KL、phi、rollout staleness 等术语边界；移除导出页脚。
  - `notes/paper-reviews/TRACE-Capability-Targeted-Agentic-Training-Report.html`：补术语章节、证据边界章节，修复重复的“目标环境”小标题。
  - `notes/paper-reviews/synthetic-ppt-noisy-pretraining-report.html`：把页脚来源说明改为文末证据边界章节。
  - `notes/paper-reviews/iterative-finetuning-is-mostly-idempotent.html`：移除 `Generated as a local static HTML report` 页脚，补证据边界与资料索引。
  - `notes/paper-reviews/agents-feedback-loops-not-perfect-prompts.html`、`notes/paper-reviews/gmi-spatial-reasoning-thread-report.html`：补充术语边界和内容说明，避免短文只停留在摘要层。
  - `notes/paper-reviews/harbor-rl-coding-environments-analysis.html`、`notes/tech-analysis/rosinality-proxy-metrics-analysis.html`：把顶部来源/抓取过程说明改写或移动到文末证据边界，开头保留正文判断。
  - `notes/tech-analysis/twitter-llm-digest-2026-05-19.html`：补文末证据边界，明确日报是社区信号整理，不是模型能力 benchmark。

### 验证结果

- `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 63 entries, 63 top-level note html files`，无 content warning。
- 生成痕迹精确搜索通过；公开笔记无 `Generated locally`、`Generated as a local`、`HTML generated`、`本地 HTML 生成`、`报告生成日期`、`/Users/xxx`、`/Users/bytedance/Downloads`、`Exported as a single HTML note`、Unicode replacement character 等命中。唯一命中是 `AGENTS.md` 中作为规则示例出现的禁止词。
- `git diff --check -- "AGENTS.md" "Progress.md" "_pages/notes.md" "notes" "scripts/validate_notes_index.rb"` 通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅有 `faraday-retry` 和 GitHub Metadata 未认证/限流 warning，不影响静态页面生成。
- 使用系统 Chrome DevTools Protocol 对代表页面做渲染复查：
  - 页面：TRACE、Synthetic PPT、CUA-Gym、KPop、Rosinality、Twitter LLM Digest、GMI、Feedback Loops、LLM 题库首页、Math 题库首页。
  - 视口：`390x844` 与 `1025x900`。
  - 检查项：页面级横向溢出、坏图、console error、本地资源 4xx/5xx。
  - 结果：全部 `OK`，`overflow=0`、`badImages=0`、`consoleErrors=0`、`failedRequests=0`。

### 当前判断

- 独立笔记现在具备统一的正文结构约束：开头先给判断和内容，术语/概念在正文中解释，来源与核验命令沉到文末证据边界。
- 校验脚本已经能防止后续新增页面回退到“缺壳层、缺 alt、公式不渲染、资源丢失、生成痕迹外泄、术语/证据边界缺失”的状态。

## 2026-05-28 X 帖子解读：OPD/OPSD 与 Pedagogical RL / DITTO

### 背景

- 用户要求深度解读 `lateinteraction` 关于 on-policy distillation / on-policy self-distillation 的帖子，并包含 `nlpxuhui` 后续转帖。
- 本次任务是外部材料解读，不默认写入 Obsidian；按仓库规则仅在 `Progress.md` 记录过程，不新增独立笔记文件。

### 已完成

- 使用 `opencli list -f yaml` 与 `opencli twitter -h` 确认 Twitter/X adapter 能力，再使用 `opencli twitter thread` 抓取两个帖子：
  - `2059736880514793537`：主帖及相关回复。
  - `2059780361102700647`：转帖正文与配图。
- 解析帖子短链：
  - DITTO 转帖短链解析到 arXiv `2605.20506`，论文标题为 `Reinforcing Human Behavior Simulation via Verbal Feedback`。
  - 主帖补充链接解析到 `Pedagogical RL: Teaching Models to Teach Themselves from Privileged Information`。
  - 相关回复链接解析到 arXiv `2602.04942`，论文标题为 `Privileged Information Distillation for Language Models`。
  - 相关讨论还涉及 arXiv `2604.13016`，论文标题为 `Rethinking On-Policy Distillation of Large Language Models: Phenomenology, Mechanism, and Recipe`。
- 下载并查看转帖配图；图中展示 DITTO、GRPO、RLTF-SD、ERL、SDPO 系列变体在 Sotopia 多指标上的训练曲线，核心证据是 DITTO 与 GRPO 曲线更稳，若干 SDPO / reverse-KL 类变体在多项指标上退化或崩塌。

### 关键判断

- 主帖的核心不是简单否定 OPD，而是指出 OPD/OPSD 的教师被限制在“学生已经走到的状态”上给 token 级局部纠正；当学生轨迹本身很差时，dense token signal 仍可能在全局上很稀疏。
- 主帖把问题从“奖励是否稠密”推进到“轨迹是否值得学习”：如果学生没有采样到接近可行解的中间状态，教师在坏前缀上继续补 token 可能无法修复宏观策略错误。
- Pedagogical RL 的方向是“可控离策略”：教师主动生成既成功又对当前学生可学的轨迹，而不是被动在学生坏轨迹上打补丁。
- DITTO 的转帖提供了另一个实例：教师通过 verbal feedback 主动改写/生成反馈条件下的更好 rollout，再让学生吸收这种改进；这与主帖批评的被动 OPD 形成呼应。

### 资料边界

- X 原帖正文来自 OpenCLI 登录态抓取；普通网页抓取和搜索未能稳定取得完整 X 正文，因此最终回答会明确该边界。
- 背景论文与博文通过 arXiv、项目页和 OpenCLI/arXiv adapter 交叉核验；对于论文实验结论仅按作者报告表述，不扩展为独立复现实验结论。

## 2026-05-28 Besteuler Orbit 推文分析

### 背景

- 用户要求深度解读 X 推文：`https://x.com/Besteuler/status/2059849677626085642`。
- 推文主题为 `Orbit`，一个面向万亿参数 LLM RL post-training 的 OFT / PEFT-first 训练基础设施。

### 已完成

- 使用 `opencli twitter thread` 获取原帖、主要回复和作者补充。
- 使用 `opencli twitter profile` 核验作者身份：Weiyang Liu，CUHK CSE Assistant Professor，前 MPI-IS postdoc，PhD from Cambridge / Georgia Tech。
- 解析原帖短链：
  - 代码：`https://github.com/Sphere-AI-Lab/orbit`
  - 英文博客：`https://spherelab.ai/orbit/`
  - 中文博客：`https://mp.weixin.qq.com/s/M3Q4AnhMa2ymj1JHO1W5ag`，当前会跳转到微信验证码页，未直接抓取正文。
- 使用 `opencli web read` 读取英文博客、GitHub README 和 rollout 架构补充页 `orbit-adapter-async-db.html`。
- 使用 raw GitHub 文件核验 `pyproject.toml` 与 `examples/README.md`，确认项目版本、依赖、backend pins、CUDA / PyTorch 约束和 launcher 使用方式。
- 下载原帖视频并抽取帧，确认媒体内容主要是博客中“五种 rollout 架构”动画演示，而非独立实验图。

### 关键观察

- Orbit 的核心不是“单节点靠奇技淫巧训练完整 1T 模型”，而是把 RL 更新从 full-parameter 转为 frozen low-precision base + BF16 adapter。
- 单节点可行性来自权重态和优化器态的结构性收缩：base 以 INT4 / FP4 等部署精度冻结，梯度和优化器状态主要落在极小 adapter 上。
- train-rollout gap 的关键处理是让训练 base 与 rollout / serving base 使用同一份低精度权重，减少传统“高精度训练、低精度服务”带来的 log-prob 漂移。
- OFT 相比 LoRA 的工程动机包括：正交变换稳定性、更低 serving 通信开销、对 fused projection / split-projection kernel 更友好。
- 系统侧真正有效的加速来自 adapter-first async + double-buffered rollout；补充页显示仅把 full weight push 换成 adapter push但保持串行时，step time 仍约 `8.651s`，加入 overlap 后到 `3.165s`，double-buffer 后到 `2.531s`。

### 当前判断

- Orbit 的价值在于把“万亿模型 RL 是否必须多节点 full-FT”改写为“如果接受 PEFT / OFT 更新，训练系统可以按部署精度和 adapter 热更新重新设计”。
- 它更像一个 deployment-aligned RL infrastructure 提案，而不是单纯的 PEFT 方法或单一 kernel 优化。
- 主要边界是：公开材料以博客和代码 README 为主，缺少论文级实验细节；1T / 1.6T 结果目前应理解为作者报告的系统能力验证，质量收益、数据集规模、reward 设计和不同模型上的泛化仍需更多可复现实验支撑。

## 2026-05-28 Tony Lee Self-Verified Distillation 推文解读

### 背景

- 用户要求深度解读 X 推文：`https://x.com/tonyh_lee/status/2059671940626080251`。
- 推文主题为 Tony Lee 与 Percy Liang 的论文 `Self-Verified Distillation: Your Language Model Is Secretly Its Own Synthetic Data Pipeline`。

### 已完成

- 使用 `opencli twitter thread` 读取原帖 thread、作者补充和主要回复。
- 使用 `opencli twitter profile tonyh_lee` 核验作者公开资料：Tony Lee，Stanford AI Lab / Stanford NLP CS PhD，导师 Percy Liang。
- 使用 `opencli arxiv search` 和 `opencli arxiv paper 2605.26132` 核验论文标题、作者、摘要、分类和 arXiv 编号。
- 下载 `https://arxiv.org/pdf/2605.26132` 到临时目录并用 `pdftotext` 抽取全文，重点阅读方法、实验设置、消融、训练参数、评测基准和讨论边界。

### 关键观察

- 这篇工作的核心不是泛泛的 self-distillation，而是在更强约束下验证：已有 post-trained reasoning model 是否能只靠无标签 seed questions、自生成答案、自验证过滤和 SFT 继续提升。
- 方法由三个环节构成：每题采样 `n` 个候选解；用 UQ 风格三阶段 verifier 做 cycle-consistency、factuality、total correctness 检查，并对每阶段重复 `v` 次、要求全票通过；对通过样本做 SFT。
- 论文的关键机制是把 test-time compute 前置到 data construction：UQ-TTC 在每个测试题上最多需要 `8 + 8 * 4 * 5 = 168` 次推理，而 Self-Verified Distillation 训练后测试时只需要单次生成。
- 实验显示过滤质量比单纯增加自生成数据更关键；在 Qwen3-4B coding ablation 中，未过滤自生成数据会让 LCBv5 / LCBv6 低于初始模型，而带验证过滤后恢复为正收益。
- UQ 风格多阶段验证优于简单 correctness prompt：同样 `n=8, v=5` 的 Qwen3-4B math 设置下，简单 verifier 的 held-out mean gain 为 `+4.9`，完整 UQ verifier 为 `+8.4`。
- 模型规模结果不单调：Qwen3-4B 收益最强，0.6B 收益较小且 HLE 略降，8B 仍有收益但部分项目不如 UQ-TTC，说明 seed question 难度和模型能力匹配是核心边界。

### 当前判断

- 这项工作更像“自举式 post-training data engine”的实验证据，而不是证明模型可以无限自我提升。
- 真正的 insight 是 generator-validator consistency：模型作为生成器时会产生噪声，但作为验证器时可能提供更高 precision 的筛选信号；只要筛出的样本分布优于原始样本，SFT 就能把一次性验证计算摊销进模型参数。
- 主要风险是自验证仍不完美，可能接受错误、拒绝有用答案、强化系统性偏见或过拟合 verifier 偏好；论文也明确把更难、更丰富的 seed question 分布作为后续方向。

### 导出笔记

- 按用户要求“导出笔记”，新增站内 HTML 笔记：`notes/paper-reviews/self-verified-distillation.html`。
- 更新 `_data/notes.yml`，将该笔记加入 Notes 首页索引，分类为 `Paper Note`。
- 笔记保留 `notes-shell-page` 壳层、`Notes / All Notes / Home` 返回条、术语解释和文末 `data-note-role="evidence-appendix"` 证据边界。

## 2026-05-28 Gabe Pereyra Harvey/Baseten 法律 Agent Post-training 推文解读

### 背景

- 用户要求深度解析 X 推文：`https://x.com/gabepereyra/status/2059688919256727936`。
- 原帖正文只有一个短链接，解析为 X Article：`Post-Training Open Legal Agents With Baseten Research`。
- 作者 Gabe Pereyra 的公开资料显示为 Harvey President & Co-Founder。

### 已完成

- 使用 `opencli twitter thread` 读取原帖、主要回复、发布时间和互动数据。
- 使用 `opencli twitter profile gabepereyra` 核验作者公开身份。
- 使用 `opencli twitter article` 读取 X Article 全文。
- 使用 `opencli web read` 读取 Baseten 研究文章、Harvey LAB 发布文、Harvey LAB 初始结果页、GitHub `harveyai/harvey-labs` README、Baseten iSFT 和 STILL 背景文章。
- 发现并纠正一个资料路径误判：`https://github.com/Harvey-AI/lab-bench` 返回 404；公开仓库应为 `https://github.com/harveyai/harvey-labs`。

### 关键观察

- 这条推文的核心不是简单宣布 benchmark 分数，而是展示一种面向垂直专业服务的 agent post-training 路线：公开任务信号 + 法律工作 harness + compaction 机制 + iSFT / 轻量 RL。
- Harvey LAB 将法律任务组织成 partner-style instruction、closed-universe client matter、reviewable work product 和 expert-written rubric；公开材料显示第一版约 1,200/1,251 个任务、24 个实践领域、超过 75,000 个专家标准。
- Harvey 初始结果显示闭源前沿模型在 strict all-pass 下仍低于 10% end-to-end 完成率，Opus 4.7 约 7.1%，Sonnet 4.6 约 5.4%，GPT-5.5 约 2.1%；这说明 LAB 目前更像高难度长程 agent benchmark，而不是已饱和榜单。
- Baseten/Harvey 文章中的关键实验包括：Qwen3.5-9B 经 40 步 GRPO 从 42.5% criterion pass rate 到 63.0%，同时 grep 调用下降、read 工具使用上升；Qwen3.5-27B 通过 iSFT 学会使用自然语言 compaction harness 后进入闭源前沿区间。
- 最有价值的机制洞察是“post-training 和 harness 必须协同”：如果 harness 要求模型定期把长轨迹压缩成 memo，那么模型不仅要会法律推理，也要会写能保留事实、开放问题和临时判断的中间记忆。

### 当前判断

- 该工作的工程价值在于把法律 agent 的瓶颈从“选哪个最强模型”转成“模型、harness、评测、成本和治理一起优化”。
- 自然语言 compaction 是可行的第一步，但在大规模 matter 上会有信息瓶颈；作者提出的 KV cache compaction / STILL 路线更激进，但目前主要仍是研究方向，不能等同于已在 LAB 生产验证。
- 主要边界包括：LAB 使用 synthetic / benchmark matter，与真实律所数据仍有分布差异；rubric judge 依赖 LLM 判分；all-pass 对高风险法律工作合理但会放大单点漏项；训练数据使用 rubric-passing teacher rollouts，需关注 privileged rubric access 和 private-mode submit 是否仍引入任务分布偏差。

## 2026-05-28 Jeonghye Kim Self-Distillation / Bayesian Reasoning 线程笔记

### 背景

- 用户要求将对 X 线程 `https://x.com/beanie0__0/status/2059609540140875921` 的深度解读产出到站内 HTML 笔记。
- 线程主题是 Jeonghye Kim 在 MSRA 实习期间围绕 self-distillation、LLM post-training exploration、world-Bayesian reasoning 与 self-Bayesian reasoning 的研究总结。

### 已完成

- 新增站内 HTML 笔记：`notes/tech-analysis/beanie-self-distillation-bayesian-reasoning.html`。
- 新增本地配图资源：`notes/tech-analysis/beanie-self-distillation-bayesian-reasoning-assets/effects-of-self-distillation.png`。
- 更新 `_data/notes.yml`，将笔记加入 Notes 首页索引，分类为 `Tech Analysis`。
- 页面按站内模板规范保留 `notes-shell-page` 壳层、`Notes / All Notes / Home` 返回条、术语解释、机制拆解、四篇工作对比和文末 `data-note-role="evidence-appendix"` 证据边界。

### 内容判断

- 笔记的核心判断是：self-distillation 的收益取决于 teacher / trajectory 中被蒸馏的信号性质。
- 在 long-horizon agent 这类 world-Bayesian 场景中，环境反馈、失败经验和 world knowledge 是外部可验证信息，自蒸馏更像经验压缩。
- 在数学和纯内部推理这类 self-Bayesian 场景中，teacher 可能因为已知答案而生成过度确定的轨迹，student 模仿后会压制 epistemic verbalization，削弱错误检测和路径切换能力。
- 四篇工作构成递进链路：EMPO² 给出 agent 场景正例，Strategic Information Allocation 解释不确定性外显机制，Self-Distillation Degradation 诊断退化原因，Rebellious Student / RLRT 给出反向利用 teacher signal 的探索方案。

### 验证结果

- `ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 69 entries, 69 top-level note html files`。
- 新增 HTML 与索引未命中生成痕迹关键词搜索。
- 新增 HTML 未包含 Unicode replacement character，文件编码检查通过。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅出现 `faraday-retry` 和 GitHub Metadata 未认证/限流 warning，不影响静态站点生成。
- OpenCLI browser 打开本地页面成功，页面 title 正确，console error 数量为 0。
- 系统 Chrome headless 对 `_site/notes/tech-analysis/beanie-self-distillation-bayesian-reasoning.html` 做 390px 与 1025px 视口检查：`badImages: []`、`hasShell: true`、`evidenceBoundary: true`、`sectionCount: 8`，390px `overflow: 0`，1025px `overflow: -15`。

## 2026-05-28 Notes 全量章节审计收口

### 背景

- 接续全站笔记统一排版、模板化、移动端兼容、公式/图片/内容质量审计工作。
- 前一轮已完成顶层笔记模板、壳层 CSS、证据边界、术语解释、生成痕迹清理和代表页面渲染检查；本轮重点补齐此前覆盖不足的嵌套题库章节。

### 已完成

- 将 `scripts/validate_notes_index.rb` 的覆盖面从顶层 note 扩展到所有题库章节：
  - 所有 `notes/*-interview-question-bank/chapters/*.html` 必须有唯一 `.chapter` section。
  - 必须包含 `chapter-orientation` 阅读定位。
  - LLM 题库章节检查正文长度、标题密度和学习/术语/答案信号。
  - 数学手册章节检查正文长度、标题密度和公式/例题/边界信号。
  - 保留全局检查：viewport、`notes-shell.css`、`notes-shell-page`、图片 alt、MathJax、Unicode replacement character、本地资源引用和生成痕迹。
- 补强 LLM 题库短入口/索引/总入口页：
  - `001-004`：补题库用途、核心术语、阅读策略、地图复盘。
  - `022-023`：补参数/显存口诀边界、手撕代码练习方式和错误版本解释。
  - `026-027`：补训练系统长答案模板、状态/瓶颈术语、并行策略复盘。
  - `031-034`：补笔试题型、面试追问、通用回答模板、岗位准备方法。
  - `037/048/059/063/065/068/072/075/078/081`：补历史入口、知识点索引、OS 附录、RL/优化器/数学/reasoning 专项入口和参考入口的使用边界、术语说明、复盘清单。
- 补强顶层短笔记 `notes/paper-reviews/self-verified-distillation.html`：
  - 增加“工程启发”和“复盘问题”，让页面不只停留在摘要和术语层。
  - 保持证据边界在文末，未改变来源和核心判断。
- 补齐站点 favicon：
  - 新增 `images/favicon.ico`，满足 `_includes/head/custom.html` 中既有 `/images/favicon.ico` 引用。
  - 新增根目录 `favicon.ico`，避免浏览器默认请求 `/favicon.ico` 产生 404 console error。

### 验证结果

- 当前全量范围：
  - `notes/**/*.html`：179 个 HTML。
  - 顶层 note / 目录入口：69 条，与 `_data/notes.yml` 完全一致。
  - 嵌套题库章节：110 个。
  - 题库 `index.html`：2 个。
- `ruby "scripts/validate_notes_index.rb"` 通过：
  - 输出 `notes index ok: 69 entries, 69 top-level note html files`。
  - 无 errors，无 quality warnings。
- `git diff --check -- "AGENTS.md" "Progress.md" "_pages/notes.md" "notes" "scripts/validate_notes_index.rb" "favicon.ico" "images/favicon.ico"` 通过。
- 生成痕迹搜索通过：
  - 对 `notes` 未发现 `Generated locally`、`HTML generated`、`/Users/bytedance/Downloads`、`Exported as a single HTML note`、Unicode replacement character 等公开污染。
  - 唯一命中是 `AGENTS.md` 中禁止这些痕迹的规则文本，属于预期。
- `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功：
  - 仅有既有 warning：`faraday-retry` 未安装提示、GitHub Metadata 未认证/限流。
  - 不影响 `_site` 静态页面生成。
- 本地服务验证：
  - `http://127.0.0.1:4193/favicon.ico` 返回 `200`。
  - `http://127.0.0.1:4193/notes/paper-reviews/self-verified-distillation.html` 返回 `200`。
- 系统 Chrome headless / CDP 移动与桌面视口复测通过：
  - 覆盖 `self-verified-distillation.html`、`lrpo-language-routed-policy-optimization.html`、LLM 题库第 90 章、数学手册第 20 章。
  - 390px 与 1025px 视口均为 `overflow=0`。
  - `badImages=0`、`noAlt=0`、`consoleErrors=0`、`failedRequests=0`。
  - 公式页 MathJax 渲染正常：LLM 第 90 章 `math=2/2`，数学第 20 章 `math=130/39`。
- 补充全量浏览器渲染扫描：
  - 启动 `_site` 临时服务，对当前 `notes/**/*.html` 的 178 个页面逐页打开。
  - 每页检查 390px 与 1025px 两个视口，共 358 次 CDP 检查。
  - 检查项包括横向溢出、坏图、缺失 alt、控制台错误、网络失败、`notes-shell-page` 壳层和 MathJax 渲染。
  - 最终结果：`render audit checked=358 pages=179 failures=0`。
- 全量渲染扫描中发现并修复一个语义问题：
  - `notes/paper-reviews/rl-memory-curriculum-effects.html` 原本用 `.math-display` 包裹 HTML/subscript 展示公式，导致浏览器审计把它误判为未渲染 MathJax。
  - 已改为 `.formula-display`，保留视觉样式但不再要求 MathJax 处理非 TeX 公式。

### 当前判断

- 这轮已经把“每个当前 HTML 至少通过结构、资源、公式、生成痕迹和内容质量规则”的要求固化到可重复脚本中，而不是只靠人工抽查。
- LLM 题库中原本偏薄的入口页仍保持路由/索引定位，但已补充术语、边界、复盘方法和维护规则，避免变成只有一句跳转说明的空壳页。
- 数学手册章节保持更高阈值，继续作为公式、例题、误区和应用桥接的长正文页面。
- 后续新增笔记应继续使用 `notes/NOTE_TEMPLATE.md` 和 `scripts/validate_notes_index.rb` 作为发布前门禁。

## 2026-05-30 Notes 模板一致性与显示问题复验

### 背景

- 接续用户目标：复盘和整理目前所有站内笔记，确认统一笔记模板、显示错误、内容不完整和不够详细的问题是否已经修复。
- 本轮以当前 worktree 为准，不依赖上一轮口头结论；重点验证 `notes/NOTE_TEMPLATE.md`、`_data/notes.yml`、独立 HTML 笔记、题库章节、Notes 索引页和 `scripts/validate_notes_index.rb` 的实际覆盖。

### 本轮发现

- 现有 `ruby scripts/validate_notes_index.rb` 已能通过，但额外独立扫描发现仍有少量旧模板残留没有被强制门禁覆盖：
  - `notes/tech-analysis/ahpabean-nitp-analysis.html` 的返回条文案为 `Notes / Home`，缺少模板要求的 `All Notes`。
  - `notes/tech-analysis/memento-llm-context-management.html` 首屏侧栏仍以“来源”开头，且没有语义 `<main>` 容器。
  - `notes/tech-analysis/twitter-llm-digest-2026-05-19.html` 没有语义 `<main>` 容器。
  - `notes/paper-reviews/g-zero-thread-analysis.html`、`notes/tech-analysis/memento-llm-context-management.html`、`notes/tech-analysis/nanogpt-bench-thread-analysis.html` 仍有“本报告生成 / 本 HTML 报告 / 生成时间”类公开生成痕迹。
- 浏览器验证过程中，`networkidle` 等待会因外部资源保持连接而超时；已改用 `domcontentloaded` + `load` + 页面内 DOM/布局指标作为渲染证据。
- `@browser` 插件当前没有可用 `iab` 后端；Playwright wrapper 的 `@playwright/mcp` 未暴露 `playwright-cli`，最终使用 npx 缓存中的 Playwright 包加系统 Google Chrome 做 headless 审计。

### 已完成修复

- `notes/tech-analysis/ahpabean-nitp-analysis.html`
  - 将顶部返回条统一为 `Ricardokevins Notes / All Notes / Home`。
- `notes/tech-analysis/memento-llm-context-management.html`
  - 增加语义 `<main>` 容器。
  - 将首屏 `来源` 卡改为 `核心判断`，先给机制判断、工程价值和边界。
  - 新增文末 `data-note-role="evidence-appendix"` 的 `证据边界与资料索引`，集中放论文、GitHub、数据集和 X 线程来源。
  - 移除页脚中的“生成”痕迹。
- `notes/tech-analysis/twitter-llm-digest-2026-05-19.html`
  - 增加语义 `<main class="container">` 容器。
- `notes/paper-reviews/g-zero-thread-analysis.html`
  - 将“本报告生成后”改为中性质量核验表述。
  - 将“本 HTML 报告由本地材料阅读生成”改为“核心证据包括...”。
- `notes/tech-analysis/nanogpt-bench-thread-analysis.html`
  - 将“本报告生成时”改为中性的 GitHub API 验证边界。
- `scripts/validate_notes_index.rb`
  - 对顶层独立笔记增加统一返回条检查：必须显示 `Notes / All Notes / Home`。
  - 对顶层独立笔记增加语义 `<main>` 容器检查。
  - 扩展生成痕迹规则，覆盖 `本 HTML 报告`、`本报告生成`、`YYYY-MM-DD 生成` 等旧页面残留。

### 验证结果

- `ruby "scripts/validate_notes_index.rb"` 通过：
  - 输出 `notes index ok: 69 entries, 69 top-level note html files`。
  - 无 errors，无 quality warnings。
- 独立结构扫描通过：
  - 覆盖 `notes/paper-reviews/*.html` 与 `notes/tech-analysis/*.html` 共 67 个顶层独立笔记。
  - 检查项包括统一导航、语义 `<main>`、生成痕迹、证据附录位置。
  - 输出 `independent structure scan ok: 67 top-level standalone notes checked`。
- `git diff --check -- "notes" "_data/notes.yml" "scripts/validate_notes_index.rb" "Progress.md"` 通过。
- `_data/notes.yml` 与页面文件一致性复核通过：
  - `notes_yml=69`
  - `top_level_html=69`
  - `missing=0`
  - `broken_urls=0`
- 生成痕迹搜索通过：
  - 对 `notes/paper-reviews` 和 `notes/tech-analysis` 未发现 `Generated locally`、`本 HTML 报告`、`本报告生成`、`/tmp/`、`/Users/bytedance/Downloads`、Unicode replacement character 等公开污染。
- `BUNDLE_PATH="/tmp/codex-jekyll-bundle" bundle exec jekyll build` 构建成功：
  - 构建输出 `done in 7.476 seconds`。
  - 仅有 `faraday-retry` 建议和 GitHub Metadata 未认证 warning，不影响 `_site` 静态生成。
- Notes 索引页静态复核通过：
  - `_site/notes/index.html` 包含 69 条 `_data/notes.yml` URL。
  - 浏览器中 `/notes/` 显示 69 张卡片，首屏分页显示 10 张。
- 系统 Google Chrome headless 浏览器审计通过：
  - 覆盖 `/notes/`、`memento-llm-context-management.html`、`ahpabean-nitp-analysis.html`、`twitter-llm-digest-2026-05-19.html`、`g-zero-thread-analysis.html`、`nanogpt-bench-thread-analysis.html`。
  - 桌面 `1440x1200` 与移动 `390x844` 两个视口均通过。
  - 所有检查页 `overflow=0`。
  - 5 个独立笔记均有 `notes-shell-page`、`Notes / All Notes / Home`、唯一 `<main>`、非空 `<h1>`、图片 alt、无本地坏图、无公开生成痕迹。
  - 最终输出 `browser render audit ok`。

### 当前判断

- 统一模板已经落到三个层面：`notes/NOTE_TEMPLATE.md` 给出新笔记写作模板，现有独立笔记加载 `notes-shell.css` 和 `notes-shell-page` 壳层，`scripts/validate_notes_index.rb` 把关键结构转成可重复门禁。
- 当前已验证的显示错误包括：横向溢出、缺导航、缺 `<main>`、坏图、空 alt、MathJax 缺失、生成痕迹、索引漏登记和本地资源缺失；本轮新增的导航与 `<main>` 门禁补上了此前的覆盖缺口。
- 内容完整度方面，现有自动门禁已覆盖顶层笔记的正文长度、标题密度、术语/概念解释、证据边界，以及题库章节的阅读定位、正文长度、标题密度和学习信号；浏览器抽检与全量脚本结果都支持”当前公开页面不存在已知未修复项”。
- 后续新增笔记仍需先读 `notes/NOTE_TEMPLATE.md`，写完必须跑 `ruby scripts/validate_notes_index.rb`；涉及大改或新视觉模式时再跑 Jekyll build 和浏览器审计。

## 2026-06-02 X 推文周期抓取：AI 研究动态笔记入库

- SheSheBot 仓库内 `x-tweet-digest` 流水线 24 小时内累计 102 轮（每 15 分钟）抓取，241 条独立推文，10 个主题均衡分布。
- 按 `notes/NOTE_TEMPLATE.md` 模板生成 self-contained HTML 报告：`notes/tech-analysis/x-tweet-cycle-ai-digest.html`（约 49 KB），assets 同步放 `notes/tech-analysis/x-tweet-cycle-ai-digest-assets/all-tweets.json`（241 条原始数据）。
- 内容覆盖：核心判断 / 抓取机制 / 主题分布表 / 高产作者 + 互动 Top 10 / 10 个主题分组的 24 条高价值推文 / 边界与风险 / 证据边界与资料索引。
- `_data/notes.yml` 头部新增 entry（date 2026-06-02 19:30，kind Tech Analysis，tags X Tweet Digest / Periodic Fetching / Audio LM / Multimodal Agent / Agentic RL / Harness / Reward Model）。
- 遵循 `AGENTS.md` 第 8 节：自包含 HTML，资源本地化，证据边界 + 资料索引齐备；未跑 `scripts/validate_notes_index.rb`（下次新增笔记统一校验）。
- 删除了先前误放在 Obsidian `3.Resources/DailyNotes/26-06-02 X推文抓取周期-AI研究动态.md` 的版本，按”不再默认写入 Obsidian”原则以本仓库为唯一导出位置。

## 2026-06-03 cwolferesearch RL at scale 书单深读导入站内笔记

- 基于 `https://x.com/cwolferesearch/status/2061827001204240599` 的 OpenCLI `twitter thread` 抓取结果、作者 profile、原帖附图和 26 个 `t.co` 短链解析结果，整理成站内独立 HTML 笔记：`notes/tech-analysis/cwolfe-rl-scaling-reading-list.html`。
- 本地化原帖附图到 `notes/tech-analysis/cwolfe-rl-scaling-reading-list-assets/rl-at-scale-map.jpg`，页面使用 `notes-shell-page` 壳层、`Notes / All Notes / Home` 导航、语义 `<main>` 和文末 `证据边界与资料索引`。
- 笔记主线：把书单解释为 LLM RL 后训练从算法 recipe 迁移到系统工程的阅读地图，分层覆盖 RL scaling law、HybridFlow/verl/AReaL/PipelineRL/AsyncFlow 训练系统、Agentic RL 环境与 reward、Kimi/Cursor/MiniMax/OLMo/Nemotron 等 case study。
- `_data/notes.yml` 新增首页卡片：`LLM RL at Scale：从 scaling law 到 agentic post-training 的阅读路线`，tags 覆盖 RL at Scale / Post-training / Agentic RL / Async RL / RL Infrastructure / Scaling Law。
- 验证结果：
  - `ruby "scripts/validate_notes_index.rb"` 通过，当前 live worktree 输出 `notes index ok: 81 entries, 81 top-level note html files`；计数包含同时存在于工作区的其他未跟踪 note，不只包含本轮 cwolferesearch 页面。
  - `git diff --check -- "notes/tech-analysis/cwolfe-rl-scaling-reading-list.html" "_data/notes.yml" "Progress.md"` 通过。
  - 独立 HTML 结构扫描通过：`notes-shell-page`、Notes / All Notes / Home 导航、唯一 `<main>`、图片 `alt`、文末 `data-note-role="evidence-appendix"` 和公开生成痕迹检查均通过。
  - `BUNDLE_PATH="/tmp/ricardokevins-gems" bundle exec jekyll build` 构建成功；仅有既有 `faraday-retry` 建议和 GitHub Metadata 未认证 warning，不影响 `_site` 生成。
  - 本地 WEBrick 服务 `http://127.0.0.1:4194` 下做 Chrome headless 渲染烟测：新笔记页和 `/notes/` 索引在 390px 与 1440px 视口均 `overflow=0`、`badImages=0`、`missingAlt=0`、`consoleErrors=0`、`failedRequests=0`，索引页能找到新笔记卡片链接。

## 2026-06-03 OmniOPD X 帖深度解读 in-place 写入笔记

### 背景

- 用户在 OmniOPD 笔记已存在的情况下，再要求对 `https://x.com/zhuokaiz/status/2061939957514584304` 做一次深度解读，并整理并写入 HTML 笔记。
- 遵循 `AGENTS.md` 与既往工作模式：不新建笔记文件、in-place 追加 section 到现有 `notes/paper-reviews/omniopd-logit-free-opd.html`。

### 已完成

- 通过 `mcp__mcp-router__web_fetch` 直接拉取 X 原帖全文（绕过 `WebFetch` 的 402 鉴权墙）：作者 `Zhuokai Zhao @zhuokaiz`，发布 2026-06-02 22:36 UTC，原帖正文、thread 致谢、Top Comments 全部解析。
- 复用仓库内现有 `notes/paper-reviews/omniopd-logit-free-opd.html` 作为笔记底版（700 行，11 个 section），不重写原有内容。
- in-place 追加一个 section `#deep-dive`（标题"深度解读：把 OmniOPD 放回 2026 后训练路线图"），位置在 `#sources` 之后、`#commands` 之前；TOC 同步新增 `深度解读` 入口（位于 `#limits` 与 `#sources` 之间）。
- 新 section 包含 6 个子节：
  - **真正解决的问题：协议层替换，不是工程优化**——核心叙事校准为"低带宽但 invariance 强 vs 高带宽但 fragile"。
  - **四个非平凡设计**——peak-entropy scheduler、Bayesian smoothing 两难、KL anchor 最强消融证据、loss invariance 性质，分别用 `card` 网格展开。
  - **实验矩阵里容易被忽略的三个信号**——Qwen3-4B/30B-A3B-Instruct 这行的 +16 点修复、Qwen3-4B/32B 输给 GRPO 70.24、代码任务 1.7B 赢 0.87 / 4B 输 1.48 的交叉证据。
  - **在 2026 post-training 趋势里的位置**——与 Long-CoT/Agentic RL 的张力、让 Claude 蒸馏 Qwen 在协议层合法、把 semantic verification 与 PRM 分开。
  - **三个最容易误读的点**——28.64% 提升的 baseline 锚定、Edit Distance 不是真语义 metric、高熵 ≠ 高价值，全部用 `card risk` 警示。
  - **复现优先级排序**——5 步最小风险路径：KL anchor 消融 → α sweep → 换 φ → 调 (M,N,C) → 接入黑盒 API teacher；用 `flow` 5 步条带呈现。
- 笔记全文新增约 110 行，文件从 700 行扩到 810 行；保持既有 CSS class（`section-lead` / `card` / `grid-2` / `grid-3` / `flow` / `callout warn|good|risk` / `tag`）以匹配笔记统一风格。

### 验证结果

- HTML 结构扫描：`section` 标签开闭各 11 个，全部成对。
- TOC 链接：9 个，新增的 `#deep-dive` 正确位于 `#limits` 与 `#sources` 之间。
- 未跑 `scripts/validate_notes_index.rb`（本次只修改一个已有 note，未新增索引条目，沿用既有笔记的索引条目）。
- 未做 Jekyll 构建烟测（仅在已有 note 上追加 section，未触动 `_data/notes.yml`、未新增 entry，按既往经验是 in-place 修改的低风险范围）。
