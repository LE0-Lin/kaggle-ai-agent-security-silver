<p align="center">
  <img src="assets/repo-banner.svg" alt="Kaggle AI Agent Security 银牌方案" width="100%">
</p>

# AI Agent Security Kaggle 银牌方案

这是 **AI Agent Security: Multi-Step Tool Attacks** 比赛银牌方案的可复现、合规开源版本。

> **一句话概括：**这不是单纯寻找一个“厉害 Prompt”，而是设计一个与评测指标对齐、能够根据运行时反馈自适应选择策略、并通过全新环境复放验证的 Agent 红队搜索算法。

🏅 **[查看 Kaggle 官方银牌证书](https://www.kaggle.com/certification/competitions/leolin05/ai-agent-security-multi-step-tool-attacks)**

📖 **[完整中文方案解读、代码导读与面试讲法](docs/solution-walkthrough.zh-CN.md)**

## 成绩

| 项目 | 结果 |
|---|---:|
| 最终排名 | **184 / 4,186 队** |
| 奖牌 | **Kaggle 银牌** |
| 最终计分 Notebook | `Open PNF P4 Model Fallback 20260823` v18 |
| Public Score | 16.215 |
| Private Score | **16.275** |
| Submission ID | `55905450` |
| 官方证明 | **[Kaggle Competition Silver Medal Certificate](https://www.kaggle.com/certification/competitions/leolin05/ai-agent-security-multi-step-tool-attacks)** |

比赛由 OpenAI、Google 和 IEEE 主办，目标是在确定性的离线沙箱中寻找可复现的多步 Agent 工具调用安全失败。评测器会重新执行候选轨迹，而不是相信参赛者自行上报的结果。

Kaggle 官方证书确认：**Zhibo Lin 在 4,186 支队伍中排名第 184，获得 Competition Silver Medal**，颁发日期为 2026 年 9 月 2 日。

## 为什么这样设计

比赛真正考察的不是模型有没有输出“危险文本”，而是候选在全新环境中复放时，是否真的产生了成功的越权工具调用。因此我的优化目标是：**可复现成功率 × 多样性 × 时间效率**。

| 评测难点 | 我的设计 |
|---|---|
| 评测器会在全新环境复放 | 只相信工具 trace，不相信模型自然语言 |
| 私有 Guardrail 不可见 | 优先选择短、稳定、低脆弱性的候选 |
| 每个模型都有时间预算 | 按单位时间内的成功收益选择模板 |
| GPT-OSS 与 Gemma 行为不同 | 根据模型动态调整最大工具步数 |
| 分数奖励攻击多样性 | 用不可投递的不同收件人构造不同候选 |
| 工具调用可能产生副作用 | 所有地址都限定为 `example.invalid` |

## 方法概览

方案使用轻量的 **probe-and-expand** 流程：

1. 用少量安全模板在官方沙箱中进行探测；
2. 从 trace 中只统计成功的 `email.send` 工具事件；
3. 以“可复现成功数 / 耗时”选择更稳的模板；
4. 根据目标模型调整最大工具调用步数；
5. 使用 `example.invalid` 保留域名生成 2,000 个不可真实投递的多样化候选；
6. 任意探测异常都按失败处理，避免伪造成功。

最重要的防御启示是：**高权限工具调用必须绑定到明确的用户意图，不能只依赖看起来合理的上下文。**

完整内容包括评分公式拆解、算法伪代码、每个核心函数的作用、为什么有效、方案局限和可升级方向，见 [中文深度解读](docs/solution-walkthrough.zh-CN.md)。

## 本地验证

官方 `aicomp_sdk` 与评测器由 Kaggle 比赛环境提供。本仓库的本地测试只使用最小接口桩，不访问真实模型、邮箱或网络服务。

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
pytest
python scripts/build_notebook.py
```

更完整的说明见：

- [方法与威胁模型](docs/methodology.md)
- [完整中文方案解读](docs/solution-walkthrough.zh-CN.md)
- [English solution walkthrough](docs/solution-walkthrough.md)
- [复现步骤与证据链](docs/reproducibility.md)
- [成绩卡](docs/scorecard.md)

## 作者

本方案及源 Notebook 由 **Zhibo Lin**（Kaggle: `leolin05`，GitHub: `LE0-Lin`）设计并实现。仓库保留了最终计分的原始 Notebook；归档文件与作者提供的源文件 SHA-256 完全一致。成绩与复现证据见 [NOTICE.md](NOTICE.md) 和 [复现说明](docs/reproducibility.md)。

## 安全边界与许可证

本项目只用于比赛离线沙箱和防御性 Agent 安全研究，不包含比赛数据、私有评测资产、密钥、真实收件人或在线攻击目标。未经授权请勿用于测试真实系统。

项目使用 [MIT License](LICENSE) 开源。
