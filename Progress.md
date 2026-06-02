# Ricardokevins.github.io Progress

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
- 精确 staged snapshot 检查通过后已 commit/push。

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
- 在干净提交 worktree 中，`ruby "scripts/validate_notes_index.rb"` 通过，输出 `notes index ok: 62 entries, 62 top-level note html files`。
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
