# Repository Agent Instructions

## Communication

- 与用户沟通、报告、日志和研究总结默认使用中文。
- 代码、变量名、提交信息和技术实现可使用英文，除非上下文明确要求中文。
- 输出保持专业、直接、基于事实；不要用未经验证的猜测替代工具检查。

## Engineering Principles

- 默认遵循 KISS、YAGNI、DRY、SOLID。
- 修改代码前先阅读相关文件，理解现有结构和约定。
- 变更应保持最小必要范围，避免无关重构和目录噪声。
- 发现代码或流程问题时，先分析原因和修复方案，再执行修复和验证。

## Command And Search Standards

- 文件路径在 shell 命令中使用双引号。
- 内容搜索优先使用 `rg`。
- 需要联网检索时，若 Grok-Search 工具在当前会话可用，应优先使用；不可用时使用可用的联网搜索工具并说明边界。
- 批量读取互不依赖的文件时优先并行工具调用。

## Obsidian Rules

若任务与当前代码仓库无直接关系，默认把研究、论文、技巧或思考沉淀到 Obsidian：

- Obsidian 仓库：`/Users/bytedance/Library/Mobile Documents/iCloud~md~obsidian/Documents/obsidian-example-lifeos-main/`
- 写入前先阅读 Obsidian 仓库内的 `CLAUDE.md`。
- 使用 Obsidian Markdown，包含 frontmatter、`up::`、wikilinks 和必要 callouts。
- 论文和研究笔记放入 `3.Resources/PaperNotes/`，命名为 `YY-MM-DD 标题.md`。
- 小技巧放入 `3.Resources/Tips/`；读书笔记放入 `3.Resources/BookNotes/`；日常思考放入 `3.Resources/DailyNotes/`；项目文档按项目放入 `1.Projects/项目名/`。
- 如目录或放置规则变化，应同步维护 Obsidian 仓库的 `CLAUDE.md`。

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
- 除对用户报告外，应将重要过程和结论写入合适的本地文件，优先更新 `Progress.md` 或对应 Obsidian 笔记。
