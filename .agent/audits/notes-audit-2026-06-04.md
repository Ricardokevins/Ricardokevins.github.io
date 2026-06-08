# Notes 全量审计报告（2026-06-04）

## 审计口径

- 范围：`_data/notes.yml` 中 84 条入口，其中 82 篇独立 HTML 笔记、2 个题库索引页。
- 结构检查：`notes-shell.css`、`body.notes-shell-page`、顶部 Notes / All Notes / Home、`main`、图片 alt、章节数量。
- 内容检查：正文长度、机制/概念解释、边界/风险/证据章节、标题是否覆盖“为什么/机制/实验/失败/工程启发”等深入分析维度。
- 噪声检查：抓取命令、工具名、本地路径、results 目录、报告生成时间、本地文件说明等不服务读者理解的过程信息。
- 评分含义：A=基本达标；B=主体可读但仍可增强；C=需要内容/结构改进；D=优先修。自动评分只做 triage，内容事实仍需结合原始材料逐篇复核。

## 总览

- A: 61
- B: 19
- C: 1
- D: 1
- INDEX: 2

## 本轮规范化后的结论

1. 已新增 repo-local Notes authoring skill：`.agent/skills/notes-authoring/SKILL.md`。
2. 已更新 `notes/NOTE_TEMPLATE.md`，把结构、内容顺序、禁止项和验证命令写入模板。
3. 已加强 `scripts/validate_notes_index.rb` 对工具名、命令痕迹、本地路径、results/Downloads 等公开噪声的 warning。
4. 当前独立 Notes 页面在噪声扫描中无命中；剩余 C/D 主要是内容可继续扩写，不是结构或发布安全问题。

## 逐篇审计表

| # | 评级 | 笔记 | 字数 | H2 | 主要问题 | 建议 |
|---:|:---:|---|---:|---:|---|---|
| 1 | A | [LLM Infra 设计谱系：从 attention 到 MoE 再到 FP8](/notes/tech-analysis/llm-infra-design-patterns.html) | 10490 | 11 | content:depth-risk | 增加“为什么重要/失败边界/如何落地” |
| 2 | A | [Mid-training：预训练和后训练之间真正发生了什么](/notes/tech-analysis/mid-training-llm-training-pipeline.html) | 4885 | 7 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 3 | A | [LLM RL at Scale：从 scaling law 到 agentic post-training 的阅读路线](/notes/tech-analysis/cwolfe-rl-scaling-reading-list.html) | 7739 | 10 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 4 | A | [OmniOPD：用语义 chunk 验证绕开 teacher logits](/notes/paper-reviews/omniopd-logit-free-opd.html) | 11536 | 10 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 5 | A | [MAI-Thinking-1：微软如何把模型研发做成 Hill-Climbing Machine](/notes/tech-analysis/mai-thinking-1-hill-climbing-machine.html) | 14869 | 14 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 6 | A | [CAST：给 GRPO 补上 verifier-grounded 的 token 级信用分配](/notes/paper-reviews/cast-grpo-self-teaching.html) | 6357 | 9 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 7 | A | [Speculative Decoding：投机解码的真实收益、校正采样与生产边界](/notes/tech-analysis/speculative-decoding-inference.html) | 6153 | 9 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 8 | A | [The Thinking Pixel：把 test-time compute 放进扩散模型 latent 层](/notes/paper-reviews/thinking-pixel-recursive-sparse-reasoning.html) | 5550 | 8 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 9 | A | [LongTraceRL：用搜索轨迹和实体级 rubric 训练 128K 长上下文推理](/notes/paper-reviews/longtracerl-long-context-reasoning.html) | 6383 | 8 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 10 | B | [RHELM：长期记忆评测为什么必须超越静态对话](/notes/paper-reviews/rhelm-long-horizon-memory.html) | 5771 | 10 | noise:process-at-top | 可作为合格样式参考或低优先级复核 |
| 11 | A | [A-Evolve：把 Agent Harness 变成可演化的工程对象](/notes/tech-analysis/a-evolve-self-evolving-agents.html) | 9711 | 9 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 12 | A | [Agentic RL 的 rollout 层：从 Agent Loop 到 Agent Environment](/notes/tech-analysis/agentic-rl-rollout-environments.html) | 6065 | 9 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 13 | A | [TRB：把 OPD 的早期采样问题改写成受约束的教师引导](/notes/paper-reviews/trb-opd-warmup.html) | 5413 | 8 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 14 | A | [X 推文周期抓取：AI 研究动态 102 轮选 24 条](/notes/tech-analysis/x-tweet-cycle-ai-digest.html) | 26664 | 16 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 15 | A | [Async RL 是否已解决：policy lag、IS 偏差与后训练系统边界](/notes/tech-analysis/frontier-async-rl-solved.html) | 5769 | 8 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 16 | A | [BES：把搜索从同分布采样推进到目标反推与轨迹重组](/notes/paper-reviews/bes-bidirectional-evolutionary-search.html) | 6860 | 9 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 17 | B | [Self-Verified Distillation：模型如何把自验证变成后训练数据引擎](/notes/paper-reviews/self-verified-distillation.html) | 4232 | 7 | content:short | 补核心机制、代表实验、反例和工程启发 |
| 18 | B | [LRPO：把语言选择变成多语言后训练的可学习变量](/notes/paper-reviews/lrpo-language-routed-policy-optimization.html) | 4319 | 8 | content:short | 补核心机制、代表实验、反例和工程启发 |
| 19 | A | [Self-Distillation 的两面性：World-Bayesian 与 Self-Bayesian 推理](/notes/tech-analysis/beanie-self-distillation-bayesian-reasoning.html) | 5957 | 8 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 20 | B | [Harvey/Baseten：开放法律 Agent 后训练路线](/notes/tech-analysis/harvey-baseten-open-legal-agents.html) | 4493 | 7 | content:short | 补核心机制、代表实验、反例和工程启发 |
| 21 | A | [Orbit：把万亿模型 RL 后训练改写成部署一致性问题](/notes/tech-analysis/orbit-rl-infrastructure-analysis.html) | 5585 | 8 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 22 | A | [CUA-Gym：Computer-Use Agent 的 RLVR 数据基础设施](/notes/tech-analysis/cua-gym-rlvr-data-infrastructure.html) | 4714 | 8 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 23 | B | [KPop：用自适应 Mask 稳住 Agentic RL 的训练-推理错配](/notes/tech-analysis/jia-guo-kpop-agentic-rl.html) | 4961 | 8 | noise:command-section | 可作为合格样式参考或低优先级复核 |
| 24 | C | [Cracks in the Foundation：长上下文扩展为什么会被小架构选择击穿](/notes/paper-reviews/cracks-foundation-long-context.html) | 3679 | 7 | content:short, content:depth-risk | 补核心机制、代表实验、反例和工程启发；增加“为什么重要/失败边界/如何落地” |
| 25 | B | [SkillEvolBench 深度解读：从一次性经验到可复用程序性技能](/notes/paper-reviews/skillevolbench-skill-evolution.html) | 7181 | 8 | content:terms-weak, content:depth-risk | 首次出现专有名词时补一句定义；增加“为什么重要/失败边界/如何落地” |
| 26 | A | [ZEDA：后训练 MoE 如何跳过一半专家计算](/notes/tech-analysis/rohanpaul-zeda-moe-analysis.html) | 6874 | 8 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 27 | A | [Hwcoder 算法笔记体系读书笔记](/notes/tech-analysis/hwcoder-algorithm-notes-reading.html) | 9403 | 7 | content:depth-risk | 增加“为什么重要/失败边界/如何落地” |
| 28 | A | [Agentic Systems as Boosting Weak Reasoning Models 深度解读](/notes/tech-analysis/che-shr-cat-agentic-boosting.html) | 9092 | 8 | content:terms-weak | 首次出现专有名词时补一句定义 |
| 29 | A | [Shannon Scaling Law 与 Token Noise 极限解读](/notes/tech-analysis/rosinality-shannon-scaling-law.html) | 6921 | 9 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 30 | A | [VPO：为什么多样性训练会改善测试时搜索](/notes/tech-analysis/ryanboldi-vpo-test-time-search.html) | 7895 | 8 | content:terms-weak | 首次出现专有名词时补一句定义 |
| 31 | A | [Applied Compute RMSD：把 OOD 企业行为拉回模型分布内](/notes/tech-analysis/appliedcompute-rmsd-thread-analysis.html) | 5658 | 8 | content:depth-risk | 增加“为什么重要/失败边界/如何落地” |
| 32 | A | [Grok V9、Cursor 数据与 Mid-training 深度解读](/notes/tech-analysis/eliebakouch-grok-v9-midtraining.html) | 7898 | 9 | content:terms-weak | 首次出现专有名词时补一句定义 |
| 33 | A | [EqR 与 Neural Attractors：从 Feedforward 到 Iterative Reasoner](/notes/tech-analysis/eqr-attractor-reasoners-analysis.html) | 7924 | 8 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 34 | A | [可信 Audio LLM Survey 深度解读](/notes/tech-analysis/huggingpapers-audio-llm-trust.html) | 7875 | 9 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 35 | A | [SaaS-Bench 解读：Computer-Use Agent 为什么还不是可靠的 SaaS 工作者](/notes/tech-analysis/saas-bench-cua-analysis.html) | 7985 | 9 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 36 | B | [RL Memory Agent 训练数据效应：Curriculum 如何塑造外部记忆问答能力](/notes/paper-reviews/rl-memory-curriculum-effects.html) | 6750 | 8 | content:terms-weak, content:depth-risk | 首次出现专有名词时补一句定义；增加“为什么重要/失败边界/如何落地” |
| 37 | A | [ZCube 推理网络架构解读：KV Cache 流量如何改变数据中心拓扑](/notes/tech-analysis/zai-zcube-inference-network.html) | 11371 | 10 | content:terms-weak | 首次出现专有名词时补一句定义 |
| 38 | A | [Test-Time Scaling 与 Training-Free RL 深度解读](/notes/tech-analysis/sheriyuo-tts-training-free-rl.html) | 7772 | 9 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 39 | B | [NITP：Next Implicit Token Prediction 技术解读](/notes/tech-analysis/ahpabean-nitp-analysis.html) | 10283 | 8 | noise:command-section | 可作为合格样式参考或低优先级复核 |
| 40 | A | [手撕经典算法 #1 Attention 篇整理](/notes/tech-analysis/manual-coding-attention.html) | 8936 | 9 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 41 | INDEX | [数学基础速修手册](/notes/math-interview-question-bank/) | 2362 | 1 | 题库索引页，不按单篇笔记口径评分 | 保持导航和搜索可用；章节质量另按题库章节审计 |
| 42 | INDEX | [大模型面试题库](/notes/llm-interview-question-bank/) | 6845 | 1 | 题库索引页，不按单篇笔记口径评分 | 保持导航和搜索可用；章节质量另按题库章节审计 |
| 43 | A | [推特大模型动态日报 | 2026-05-19](/notes/tech-analysis/twitter-llm-digest-2026-05-19.html) | 4534 | 7 | content:depth-risk | 增加“为什么重要/失败边界/如何落地” |
| 44 | A | [NanoGPT-Bench X 线程解读：Coding Agent 能做研究吗？](/notes/tech-analysis/nanogpt-bench-thread-analysis.html) | 5236 | 8 | content:terms-weak | 首次出现专有名词时补一句定义 |
| 45 | B | [ECHO: Terminal Agents Learn World Models for Free](/notes/tech-analysis/echo-terminal-world-models.html) | 7628 | 8 | content:terms-weak, content:depth-risk | 首次出现专有名词时补一句定义；增加“为什么重要/失败边界/如何落地” |
| 46 | A | [GRPO 之后：Dense Credit Assignment 的下一步](/notes/tech-analysis/nrehiew-grpo-credit-assignment-analysis.html) | 6144 | 6 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 47 | A | [Delegation Intelligence：Agent 时代该如何重新理解评测](/notes/tech-analysis/delegation-intelligence-agent-eval.html) | 4627 | 7 | content:depth-risk | 增加“为什么重要/失败边界/如何落地” |
| 48 | A | [rosinality X 帖与 Proxy Metrics 论文深读](/notes/tech-analysis/rosinality-proxy-metrics-analysis.html) | 6221 | 8 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 49 | A | [大模型测试的下半场：Agent 时代评测该测什么](/notes/tech-analysis/zhihu-frontier-llm-eval-second-half.html) | 5842 | 9 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 50 | B | [Mid-training/RL 数据重叠会伤害 RL 吗？](/notes/tech-analysis/eliebakouch-rl-overlap-analysis.html) | 4675 | 6 | content:terms-weak, content:depth-risk | 首次出现专有名词时补一句定义；增加“为什么重要/失败边界/如何落地” |
| 51 | A | [Lilian Weng: System Accidents 解读](/notes/tech-analysis/lilianweng-system-accidents-analysis.html) | 7893 | 10 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 52 | A | [Memento / KV Cache X 帖深度解读](/notes/tech-analysis/memento-kv-cache-x-analysis.html) | 6184 | 8 | content:depth-risk | 增加“为什么重要/失败边界/如何落地” |
| 53 | A | [MEMENTO 深度解读：教 LLM 管理自己的上下文](/notes/tech-analysis/memento-llm-context-management.html) | 7019 | 9 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 54 | A | [长周期 Agent、None-Person Company 与自我进化](/notes/tech-analysis/jietang-long-horizon-agent-analysis.html) | 6311 | 7 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 55 | A | [Artificial Analysis 语音 Agent 评测解读](/notes/tech-analysis/artificial-analysis-tau-voice-report.html) | 5459 | 7 | content:terms-weak | 首次出现专有名词时补一句定义 |
| 56 | B | [Nitrobrew 推文与技术解读](/notes/tech-analysis/26-05-12-nitrobrew-tweet-analysis.html) | 6770 | 9 | content:terms-weak, content:depth-risk | 首次出现专有名词时补一句定义；增加“为什么重要/失败边界/如何落地” |
| 57 | A | [SEIF 论文与 X 帖深度分析](/notes/paper-reviews/seif-instruction-following-report.html) | 9769 | 11 | content:terms-weak | 首次出现专有名词时补一句定义 |
| 58 | A | [168X / Herman Jin 半导体访谈深读](/notes/paper-reviews/168x-intel-semiconductor-analysis.html) | 6026 | 9 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 59 | A | [ACuRL X 线程与论文解读：Computer-use Agent 的自主持续学习](/notes/paper-reviews/acurl-computer-use-agents-analysis.html) | 6173 | 8 | content:terms-weak | 首次出现专有名词时补一句定义 |
| 60 | D | [Agents Need Feedback Loops 阅读分析](/notes/paper-reviews/agents-feedback-loops-not-perfect-prompts.html) | 4462 | 7 | content:short, content:terms-weak, content:depth-risk | 补核心机制、代表实验、反例和工程启发；首次出现专有名词时补一句定义；增加“为什么重要/失败边界/如何落地” |
| 61 | A | [Dr. Post-Training 推文与论文深读](/notes/paper-reviews/dr-post-training-analysis.html) | 7784 | 8 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 62 | B | [Fast-Slow Training X Thread Analysis](/notes/paper-reviews/fast-slow-training-analysis.html) | 8053 | 8 | content:terms-weak, content:depth-risk | 首次出现专有名词时补一句定义；增加“为什么重要/失败边界/如何落地” |
| 63 | A | [G-Zero X 线程与论文深读](/notes/paper-reviews/g-zero-thread-analysis.html) | 7934 | 9 | content:terms-weak | 首次出现专有名词时补一句定义 |
| 64 | A | [GMI Cloud 足球踢球动画 Thread 梳理](/notes/paper-reviews/gmi-spatial-reasoning-thread-report.html) | 4618 | 10 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 65 | A | [Harbor 与 RL Coding Environments 长文梳理](/notes/paper-reviews/harbor-rl-coding-environments-analysis.html) | 5399 | 8 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 66 | A | [Lighthouse Attention X 帖与论文深读](/notes/paper-reviews/lighthouse-attention-x-analysis.html) | 8746 | 8 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 67 | B | [LongMemEval-V2 深度解读：Agent Memory 如何走向有经验的同事](/notes/paper-reviews/longmemeval-v2-agent-memory-report.html) | 7698 | 8 | content:terms-weak, content:depth-risk | 首次出现专有名词时补一句定义；增加“为什么重要/失败边界/如何落地” |
| 68 | B | [MMProLong / LongPT 深度解读](/notes/paper-reviews/mmprolong-long-context-lvlm-analysis.html) | 6231 | 9 | content:terms-weak, content:depth-risk | 首次出现专有名词时补一句定义；增加“为什么重要/失败边界/如何落地” |
| 69 | A | [AVB OPD / OPSD 资源帖深度解读](/notes/paper-reviews/neural-avb-opd-resources-report.html) | 9522 | 10 | content:depth-risk | 增加“为什么重要/失败边界/如何落地” |
| 70 | B | [Prime Intellect autonomous nanoGPT speedrun 解读](/notes/paper-reviews/primeintellect-autonomous-nanogpt-analysis.html) | 6768 | 7 | content:terms-weak, content:depth-risk | 首次出现专有名词时补一句定义；增加“为什么重要/失败边界/如何落地” |
| 71 | A | [KLieret X 线程解读：GPT 5.5 首次解出 ProgramBench 实例](/notes/paper-reviews/programbench-gpt55-analysis.html) | 5187 | 8 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 72 | A | [RELEX / Minimal RLVR Training 深度解读](/notes/paper-reviews/relex-rlvr-thread-analysis.html) | 6857 | 8 | content:terms-weak | 首次出现专有名词时补一句定义 |
| 73 | A | [RESD X 线程与论文解读](/notes/paper-reviews/resd-x-analysis.html) | 7645 | 7 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 74 | A | [Reward Hacking in Rubric-Based RL：X 线程与论文深读](/notes/paper-reviews/reward-hacking-rubric-rl-analysis.html) | 8950 | 9 | content:depth-risk | 增加“为什么重要/失败边界/如何落地” |
| 75 | B | [SWE-ZERO-12M Trajectories X 帖深度解读](/notes/paper-reviews/swe-zero-12m-thread-analysis.html) | 7473 | 8 | content:terms-weak, content:depth-risk | 首次出现专有名词时补一句定义；增加“为什么重要/失败边界/如何落地” |
| 76 | B | [TencentDB Agent Memory 推文与开源项目分析](/notes/paper-reviews/tencent-agent-memory-report.html) | 5870 | 6 | content:terms-weak, content:depth-risk | 首次出现专有名词时补一句定义；增加“为什么重要/失败边界/如何落地” |
| 77 | A | [Iterative Finetuning is Mostly Idempotent](/notes/paper-reviews/iterative-finetuning-is-mostly-idempotent.html) | 6408 | 10 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 78 | A | [LCO-Embedding 论文深读报告](/notes/paper-reviews/lco-embedding-paper-analysis.html) | 8857 | 10 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 79 | A | [OnlineRubrics 论文深读与 Insight](/notes/paper-reviews/onlinerubrics-paper-analysis.html) | 6924 | 8 | content:depth-risk | 增加“为什么重要/失败边界/如何落地” |
| 80 | B | [Rebellious Student / RLRT 论文深读报告](/notes/paper-reviews/rebellious-student-rlrt-analysis.html) | 7710 | 10 | noise:command-section | 可作为合格样式参考或低优先级复核 |
| 81 | A | [Synthetic Pre-Pre-Training Improves LM Robustness](/notes/paper-reviews/synthetic-ppt-noisy-pretraining-report.html) | 7897 | 12 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 82 | A | [TRACE: Capability-Targeted Agentic Training](/notes/paper-reviews/TRACE-Capability-Targeted-Agentic-Training-Report.html) | 6621 | 11 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 83 | A | [Unmasking On-Policy Distillation](/notes/paper-reviews/unmasking-on-policy-distillation.html) | 9430 | 12 | 未发现明显结构/噪声问题 | 可作为合格样式参考或低优先级复核 |
| 84 | B | [Visual Generation Unlocks Human-Like Reasoning](/notes/paper-reviews/visual-generation-world-models.html) | 5444 | 10 | content:terms-weak, content:depth-risk | 首次出现专有名词时补一句定义；增加“为什么重要/失败边界/如何落地” |
