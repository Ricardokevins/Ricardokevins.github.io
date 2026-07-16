# Repository Agent Instructions

## Communication

- 与用户沟通、报告、日志和研究总结默认使用中文。
- 代码、变量名、提交信息和技术实现可使用英文，除非上下文明确要求中文。
- 输出保持专业、直接、基于事实；不要用未经验证的猜测替代工具检查。

## Codex Experience Profile

- 后续 Codex 会话应读取并遵循经验档案：`/Users/bytedance/Documents/Ricardokevins.github.io/.agent/codex-experience-profile.md`。
- 该档案沉淀了历史 Codex 会话与执行日志中的执行教训、用户偏好、UI/产品理念和可复用规则。
- 当前用户直接指令和当前仓库更近目录的 `AGENTS.md` 优先级更高；若冲突，以更具体、更近、更近期的指令为准。

## Engineering Principles

- 默认遵循 KISS、YAGNI、DRY、SOLID。
- 修改代码前先阅读相关文件，理解现有结构和约定。
- 变更应保持最小必要范围，避免无关重构和目录噪声。
- 发现代码或流程问题时，先分析原因和修复方案，再执行修复和验证。

## Command And Search Standards

- 文件路径在 shell 命令中使用双引号。
- 内容搜索优先使用 `rg`。
- 需要读取具体网站、社媒线程、论文页面、公开网页或执行网页交互时，优先使用 `opencli`；若目标站点有 adapter，先查看 `opencli <site> --help -f yaml` 再调用对应命令。
- 需要开放式联网检索且没有明确目标站点时，若 Grok-Search 工具在当前会话可用，应优先使用；不可用时使用可用的联网搜索工具并说明边界。
- 批量读取互不依赖的文件时优先并行工具调用。

## Web Retrieval Defaults

- `web_search` 默认带 `workflow: "none"`，**不要**在弹窗里 Review summary draft；直接用工具返回的合成答案 + 引用来源。
- `fetch_content` 默认不弹 curator，直接拿到正文即可。
- 用户用浏览器时禁止打开 curator / preview / approve 这类阻塞对话框；研究任务默认后台拉取 + 一次性回报。

## OpenCLI Usage

- `opencli` 是默认优先的网站 CLI 和浏览器自动化入口，适用于把公开网站、论文站点、社媒平台、搜索结果页和 Web App 操作转换为可复现的命令行流程。
- 常见外部资料抓取优先考虑对应 adapter，例如 `opencli arxiv`、`opencli hf`、`opencli twitter`、`opencli github`、`opencli youtube`、`opencli zhihu`、`opencli xiaohongshu`、`opencli web`。
- 不确定有哪些命令时使用 `opencli list`；不确定某个站点参数时使用 `opencli <site> --help -f yaml`。
- 浏览器桥接连接状态先用 `opencli daemon status` 检查；不要把 `opencli doctor` 当作例行预检，因为其 `__doctor__` live probe 会创建 owned browser session，并可能新建或聚焦 OpenCLI Chrome 标签组。只有真实浏览器命令失败、且用户明确允许占用 Chrome 时才运行 doctor。
- 用户的前台 Chrome 是正在使用的工作浏览器，默认禁止 bind、导航、聚焦、附加调试器或以其他方式驱动。只有用户明确把某个标签交给当前任务时，才使用 OpenCLI 1.8.6 的位置参数语法 `opencli browser <name> bind`，后续执行 `opencli browser <name> ...`，结束后立即 `opencli browser <name> unbind`。
- 用户不希望 OpenCLI 自动创建的 Chrome 标签组干扰日常标签管理。优先使用无浏览器 adapter、专用 connector、内置浏览器或其他不侵入用户 Chrome 的工具；默认不创建 owned browser session。确实无法绕过时，先说明会创建 `OpenCLI Browser` 标签组并获得用户明确许可。
- 若 `opencli` 对目标站点失败、没有 adapter、或返回信息不足，再切换到 Grok-Search、Tavily、WebFetch、专用 MCP 或浏览器自动化工具，并在结果中说明降级原因。
- `opencli` 不替代本地仓库文件操作；本地文件搜索仍优先使用 Glob/Grep/Read，代码编辑仍使用 `apply_patch`。

## Material Analysis Notes

- 不再默认写入 Obsidian。
- 当任务是阅读、解读、调研或分析外部材料，并且需要沉淀成文件时，在当前仓库目录内新建或更新合适的本地文档。
- 普通问答、轻量解释、临时结论和不需要沉淀的分析，直接在终端对用户回答，不新建文档。
- 保持仓库目录简洁；只有材料分析确有沉淀价值或用户明确要求时，才新建文档。

## Deep Reading Trigger

- 当用户给出论文、推文或 X thread、博客、技术报告、访谈等材料，并说“帮我读一下”“好好读一下”“深度解读”“梳理这篇”或同义表达时，默认读取并遵循 repo-local skill：`.agent/skills/deep-read-to-notes/SKILL.md`。
- 除非用户明确缩小范围，上述触发默认授权完整流程：读取原文、追踪会影响核心判断的关键内链与参考资料、交叉核验、深度分析、在对话中用中文直接讲解、沉淀站内笔记、更新索引与 `Progress.md`、验证、只提交本任务改动并 push。
- 用户明确要求只做摘要、暂不写笔记、不提交或不推送时，以本次限制为准。

## Notes Authoring Standard

- 新建、导入、清理或审计站内笔记时，先读取并遵循 repo-local skill：`.agent/skills/notes-authoring/SKILL.md`。
- 新建站内笔记前先读取并复用 `notes/NOTE_TEMPLATE.md`，不要从旧报告随意复制过时头尾。
- 独立 HTML 笔记必须加载 `notes/assets/notes-shell.css`，`body` 必须包含 `notes-shell-page`，页面顶部必须有 `Notes / All Notes / Home` 返回条。
- 笔记正文开头应直接进入主题判断、问题背景、核心机制和结论，不把抓取命令、生成时间、本地路径、材料从哪里来等信息放在头部。
- 来源和材料边界统一放在文末“证据边界与资料索引”一类章节，并使用 `data-note-role="evidence-appendix"`；不要出现 `/tmp/`、`/Users/xxx`、`Downloads`、`results/`、`Generated locally`、`HTML generated`、`OpenCLI/opencli` 等生成痕迹或工具痕迹。
- 公式页必须加载 MathJax；长公式容器需要横向滚动以兼容手机；所有图片必须使用本地资源并写清晰 `alt`。
- 新增或修改笔记后运行 `ruby scripts/validate_notes_index.rb`，必要时再运行 Jekyll build 或浏览器截图检查。

## Progress Tracking

- 在仓库根目录维护 `Progress.md`，记录正在做的工作、完成的变更、验证结果和关键判断。
- 保持仓库目录简洁；修改文档尽量 in-place，不为同一内容反复创建版本文件。
- 如非必要或用户明确要求，不随意新建文档。

## Autonomous Work Mode

当用户说“我要去睡觉”或表达同等授权时，进入自主工作模式：

- 自主拆解并执行所有子任务，不因普通不确定性停止询问。
- 分阶段完成，每阶段后运行适当测试或验证。
- 持续迭代、检查日志、修复问题，直到代码清晰可运行且日志无异常。
- 维护 todo / plan，记录每轮检查、修复和验证结果。
- 遇到不确定技术细节，先查上下文文档；仍不确定再联网检索。

## Research And Exploratory Work

- 做论文解读、算法改进、实验分析时，主动分析结果、日志、性能和有效性。
- 除对用户报告外，若需要沉淀重要过程和结论，应写入当前仓库内合适的本地文件；仓库研发过程优先更新 `Progress.md`。
