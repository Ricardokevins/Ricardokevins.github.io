# Ricardokevins.github.io Progress

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
